package local.bentobook;

import android.app.Activity;
import android.app.ActivityManager;
import android.app.DownloadManager;
import android.content.ActivityNotFoundException;
import android.content.BroadcastReceiver;
import android.content.ClipData;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.database.Cursor;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.GradientDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.print.PrintManager;
import android.provider.OpenableColumns;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowInsetsController;
import android.webkit.ConsoleMessage;
import android.webkit.PermissionRequest;
import android.webkit.RenderProcessGoneDetail;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;
import android.window.OnBackInvokedCallback;
import android.window.OnBackInvokedDispatcher;
import androidx.webkit.JavaScriptReplyProxy;
import androidx.webkit.WebMessageCompat;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import org.json.JSONException;
import org.json.JSONObject;

/** The BentoBook window: BentoPDF in a WebView, with Android's files, downloads and printing. */
public class MainActivity extends Activity {
  static final String TAG = Web.TAG;
  private static final int REQ_FILES = 1;
  private static final int CHUNK = 4 << 20;

  private final Handler main = new Handler(Looper.getMainLooper());
  /** Downloads and incoming files, in order, off the main thread. */
  private final ExecutorService io = Executors.newSingleThreadExecutor();
  private Store store;
  private FrameLayout root;
  private WebView web;
  private boolean isolated;
  private ValueCallback<Uri[]> pendingFiles;
  /** The file being saved; only touched on the io thread. */
  private Downloads download;
  private final List<Uri> incoming = new ArrayList<>();
  private BroadcastReceiver debug;
  private View savedBar;
  private final OnBackInvokedCallback back = () -> {
    if (web != null && web.canGoBack()) web.goBack();
  };
  private boolean backRegistered;

  @Override
  protected void onCreate(Bundle saved) {
    super.onCreate(saved);
    store = new Store(this);
    WebView.setWebContentsDebuggingEnabled(store.devtools());
    isolated = Web.isolate();
    Log.i(TAG, "cross-origin isolation allowlist: " + (isolated ? "set" : "not supported by this WebView"));

    root = new FrameLayout(this);
    setContentView(root);
    // Keep the page out from under the caption bar: its buttons would cover
    // whatever a tool puts at the top. The caption shows root's colour, which
    // follows the page's top edge (applyWindowColors).
    root.setOnApplyWindowInsetsListener((v, insets) -> {
      android.graphics.Insets bars = insets.getInsets(android.view.WindowInsets.Type.systemBars()
          | android.view.WindowInsets.Type.captionBar() | android.view.WindowInsets.Type.displayCutout());
      v.setPadding(bars.left, bars.top, bars.right, bars.bottom);
      return android.view.WindowInsets.CONSUMED;
    });
    createWebView();
    applyWindowColors(store.theme());
    registerDebugCommands();
    takeIncoming(getIntent());
    if (saved == null || web.restoreState(saved) == null) web.loadUrl(Web.HOME);
  }

  private void createWebView() {
    web = new WebView(this);
    Web.configure(web, this, this::onPageMessage);
    web.setWebViewClient(new Client());
    web.setWebChromeClient(new Chrome());
    web.setBackgroundColor(store.theme());
    root.addView(web, 0, new FrameLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
  }

  @Override
  protected void onNewIntent(Intent intent) {
    super.onNewIntent(intent);
    setIntent(intent);
    takeIncoming(intent);
    web.evaluateJavascript("window.bentobook && window.bentobook.postMessage("
        + "JSON.stringify({type:'ready'}))", null);
  }

  @Override
  protected void onSaveInstanceState(Bundle out) {
    super.onSaveInstanceState(out);
    web.saveState(out);
  }

  @Override
  protected void onDestroy() {
    if (debug != null) unregisterReceiver(debug);
    io.execute(this::abortDownload);
    io.shutdown();
    web.destroy();
    super.onDestroy();
  }

  // ---- Files from "Open with" and "Share" ----

  /** Keeps the files of a VIEW or SEND intent for the next tool that asks for files. */
  private void takeIncoming(Intent intent) {
    List<Uri> uris = new ArrayList<>();
    String action = intent == null ? null : intent.getAction();
    if (Intent.ACTION_VIEW.equals(action) && intent.getData() != null) {
      uris.add(intent.getData());
    } else if (Intent.ACTION_SEND.equals(action) || Intent.ACTION_SEND_MULTIPLE.equals(action)) {
      ClipData clip = intent.getClipData();
      if (clip != null) {
        for (int i = 0; i < clip.getItemCount(); i++) {
          Uri u = clip.getItemAt(i).getUri();
          if (u != null) uris.add(u);
        }
      }
      if (uris.isEmpty() && intent.getParcelableExtra(Intent.EXTRA_STREAM, Uri.class) != null) {
        uris.add(intent.getParcelableExtra(Intent.EXTRA_STREAM, Uri.class));
      }
    }
    uris.removeIf(u -> !"content".equals(u.getScheme()));
    if (uris.isEmpty()) return;
    incoming.clear();
    incoming.addAll(uris);
    Log.i(TAG, "incoming: " + uris.size() + " file(s)");
  }

  /** Streams the waiting files to the page that just loaded. */
  private void offerIncoming(JavaScriptReplyProxy reply) {
    if (incoming.isEmpty()) return;
    List<Uri> uris = new ArrayList<>(incoming);
    reply.postMessage(json("type", "incoming.begin"));
    io.execute(() -> {
      for (Uri uri : uris) {
        String name = "file";
        String mime = getContentResolver().getType(uri);
        try (Cursor c = getContentResolver().query(uri,
            new String[] {OpenableColumns.DISPLAY_NAME}, null, null, null)) {
          if (c != null && c.moveToFirst() && c.getString(0) != null) name = c.getString(0);
        } catch (RuntimeException e) {
          Log.w(TAG, "no name for " + uri, e);
        }
        String header = json("type", "incoming.file", "name", name, "mime", mime == null ? "" : mime);
        main.post(() -> reply.postMessage(header));
        try (InputStream in = getContentResolver().openInputStream(uri)) {
          if (in == null) throw new IOException("no stream");
          byte[] buf = new byte[CHUNK];
          for (int n; (n = in.readNBytes(buf, 0, CHUNK)) > 0; ) {
            byte[] chunk = n == CHUNK ? buf.clone() : java.util.Arrays.copyOf(buf, n);
            main.post(() -> reply.postMessage(chunk));
          }
        } catch (IOException | SecurityException e) {
          Log.w(TAG, "can't read " + uri, e);
          main.post(() -> toast(getString(R.string.cant_read)));
        }
      }
      main.post(() -> reply.postMessage(json("type", "incoming.end")));
    });
  }

  // ---- Messages from the page ----

  private void onPageMessage(WebMessageCompat message, JavaScriptReplyProxy reply) {
    if (message.getType() == WebMessageCompat.TYPE_ARRAY_BUFFER) {
      byte[] chunk = message.getArrayBuffer();
      io.execute(() -> {
        if (download == null) return;
        try {
          download.write(chunk);
        } catch (IOException e) {
          Log.w(TAG, "download failed", e);
          String name = download.name;
          abortDownload();
          main.post(() -> toast(getString(R.string.save_failed, name)));
        }
      });
      return;
    }
    String data = message.getData();
    if (data == null) return;
    JSONObject m;
    try {
      m = new JSONObject(data);
    } catch (JSONException e) {
      return;
    }
    switch (m.optString("type")) {
      case "download" -> startDownload(m.optString("name", "download"), m.optString("mime"), m.optLong("size", -1));
      case "download.end" -> finishDownload();
      case "download.failed" -> toast(getString(R.string.save_failed, m.optString("name")));
      case "theme" -> {
        try {
          int color = Color.parseColor(m.optString("color"));
          store.setTheme(color);
          applyWindowColors(color);
        } catch (IllegalArgumentException ignored) {
          // not a colour
        }
      }
      case "ready" -> {
        if (m.has("isolated")) {
          Log.i(TAG, "page ready: crossOriginIsolated=" + m.optBoolean("isolated")
              + " SharedArrayBuffer=" + m.optBoolean("sab"));
        }
        offerIncoming(reply);
      }
      case "incoming.used" -> incoming.clear();
      case "print" -> print(m.optString("title", "BentoPDF"));
      default -> { }
    }
  }

  // The page sends a download as a header, its chunks and an end marker. The
  // main thread queues all three in arrival order on the single io thread.
  private void startDownload(String name, String mime, long size) {
    io.execute(() -> {
      abortDownload();
      try {
        download = new Downloads(this, name, mime, size);
      } catch (IOException e) {
        Log.w(TAG, "can't create " + name, e);
        main.post(() -> toast(getString(R.string.save_failed, name)));
      }
    });
  }

  private void finishDownload() {
    io.execute(() -> {
      Downloads d = download;
      download = null;
      if (d == null) return;
      try {
        Uri uri = d.finish();
        String shown = Downloads.displayName(this, uri, d.name);
        main.post(() -> showSaved(shown, uri));
      } catch (IOException e) {
        Log.w(TAG, "download failed", e);
        main.post(() -> toast(getString(R.string.save_failed, d.name)));
      }
    });
  }

  private void abortDownload() {
    if (download != null) download.abort();
    download = null;
  }

  /** A bar at the bottom of the window: the saved file, with Open and Show. */
  private void showSaved(String name, Uri uri) {
    if (savedBar != null) root.removeView(savedBar);
    LinearLayout bar = new LinearLayout(this);
    bar.setGravity(Gravity.CENTER_VERTICAL);
    int pad = dp(12);
    bar.setPadding(pad, dp(6), dp(6), dp(6));
    GradientDrawable bg = new GradientDrawable();
    bg.setColor(0xF0202124);
    bg.setCornerRadius(dp(10));
    bar.setBackground(bg);
    bar.setElevation(dp(6));
    TextView text = new TextView(this);
    text.setText(getString(R.string.saved, name));
    text.setTextColor(0xFFF1F3F4);
    text.setTextSize(14);
    text.setMaxLines(2);
    bar.addView(text, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1));
    bar.addView(button(R.string.open, v -> {
      Intent view = new Intent(Intent.ACTION_VIEW).setDataAndType(uri, getContentResolver().getType(uri))
          .addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
      try {
        startActivity(view);
      } catch (ActivityNotFoundException e) {
        toast(getString(R.string.no_app));
      }
    }));
    bar.addView(button(R.string.show, v -> {
      try {
        startActivity(new Intent(DownloadManager.ACTION_VIEW_DOWNLOADS));
      } catch (ActivityNotFoundException e) {
        toast(getString(R.string.no_app));
      }
    }));
    FrameLayout.LayoutParams lp = new FrameLayout.LayoutParams(
        Math.min(dp(560), root.getWidth() - dp(32)), ViewGroup.LayoutParams.WRAP_CONTENT,
        Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL);
    lp.bottomMargin = dp(16);
    root.addView(bar, lp);
    savedBar = bar;
    main.postDelayed(() -> {
      if (savedBar == bar) {
        root.removeView(bar);
        savedBar = null;
      }
    }, 12000);
  }

  private TextView button(int label, View.OnClickListener click) {
    TextView b = new TextView(this);
    b.setText(label);
    b.setTextColor(0xFF8AB4F8);
    b.setTextSize(14);
    b.setAllCaps(false);
    b.setPadding(dp(12), dp(8), dp(12), dp(8));
    b.setOnClickListener(click);
    b.setFocusable(true);
    b.setBackgroundResource(android.R.drawable.list_selector_background);
    return b;
  }

  private void print(String title) {
    PrintManager pm = getSystemService(PrintManager.class);
    pm.print(title, web.createPrintDocumentAdapter(title), null);
  }

  // ---- WebView clients ----

  private final class Client extends WebViewClient {
    @Override
    public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
      Uri url = request.getUrl();
      return Web.isApp(url) ? Web.serve(MainActivity.this, url) : null;
    }

    @Override
    public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
      Uri url = request.getUrl();
      if (Web.isApp(url)) return false;
      // Links out of the app (GitHub, docs, mail) go to the browser.
      try {
        startActivity(new Intent(Intent.ACTION_VIEW, url).addCategory(Intent.CATEGORY_BROWSABLE));
      } catch (ActivityNotFoundException e) {
        toast(getString(R.string.no_app));
      }
      return true;
    }

    @Override
    public void doUpdateVisitedHistory(WebView view, String url, boolean reload) {
      updateBack();
    }

    @Override
    public void onPageFinished(WebView view, String url) {
      String title = view.getTitle();
      if (title != null && !title.isEmpty() && !title.startsWith("http")) setTitle(title);
    }

    @Override
    public boolean onRenderProcessGone(WebView view, RenderProcessGoneDetail detail) {
      // A huge PDF or a big WASM engine can push the renderer out of memory.
      // Replace the WebView instead of letting the whole app die with it.
      Log.w(TAG, "renderer gone, crashed=" + detail.didCrash());
      root.removeView(web);
      web.destroy();
      io.execute(MainActivity.this::abortDownload);
      createWebView();
      web.loadUrl(Web.HOME);
      toast(getString(R.string.renderer_gone));
      return true;
    }
  }

  private final class Chrome extends WebChromeClient {
    @Override
    public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> callback, FileChooserParams params) {
      if (pendingFiles != null) pendingFiles.onReceiveValue(null);
      pendingFiles = callback;
      try {
        // At targetSdk 37 this is ACTION_OPEN_DOCUMENT (or CREATE_DOCUMENT for
        // showSaveFilePicker) with the page's accept types.
        startActivityForResult(params.createIntent(), REQ_FILES);
      } catch (ActivityNotFoundException e) {
        pendingFiles = null;
        callback.onReceiveValue(null);
      }
      return true;
    }

    @Override
    public void onPermissionRequest(PermissionRequest request) {
      request.deny(); // no camera or microphone
    }

    @Override
    public void onReceivedTitle(WebView view, String title) {
      if (title != null && !title.isEmpty() && !title.startsWith("http")) setTitle(title);
    }

    @Override
    public boolean onConsoleMessage(ConsoleMessage message) {
      if (store.devtools()) Log.d(TAG, "console: " + message.message());
      return true;
    }
  }

  @Override
  protected void onActivityResult(int request, int result, Intent data) {
    if (request != REQ_FILES || pendingFiles == null) {
      super.onActivityResult(request, result, data);
      return;
    }
    Uri[] uris = null;
    if (result == RESULT_OK && data != null) {
      ClipData clip = data.getClipData();
      if (clip != null) {
        uris = new Uri[clip.getItemCount()];
        for (int i = 0; i < uris.length; i++) uris[i] = clip.getItemAt(i).getUri();
      } else if (data.getData() != null) {
        uris = new Uri[] {data.getData()};
      }
    }
    pendingFiles.onReceiveValue(uris);
    pendingFiles = null;
  }

  // ---- Window ----

  private void updateBack() {
    boolean can = web.canGoBack();
    if (can == backRegistered) return;
    if (can) {
      getOnBackInvokedDispatcher().registerOnBackInvokedCallback(OnBackInvokedDispatcher.PRIORITY_DEFAULT, back);
    } else {
      getOnBackInvokedDispatcher().unregisterOnBackInvokedCallback(back);
    }
    backRegistered = can;
  }

  /** The caption bar takes the colour of the page's top edge. */
  private void applyWindowColors(int color) {
    root.setBackgroundColor(color);
    getWindow().setBackgroundDrawable(new ColorDrawable(color));
    setTaskDescription(new ActivityManager.TaskDescription.Builder()
        .setPrimaryColor(color)
        .setBackgroundColor(color)
        .setStatusBarColor(color)
        .setNavigationBarColor(color)
        .build());
    WindowInsetsController insets = getWindow().getInsetsController();
    if (insets != null) {
      boolean light = Color.luminance(color) > 0.5f;
      int lightBars = WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS
          | WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS
          | WindowInsetsController.APPEARANCE_LIGHT_CAPTION_BARS;
      int transparent = WindowInsetsController.APPEARANCE_TRANSPARENT_CAPTION_BAR_BACKGROUND;
      insets.setSystemBarsAppearance((light ? lightBars : 0) | transparent, lightBars | transparent);
    }
  }

  private int dp(int v) {
    return Math.round(v * getResources().getDisplayMetrics().density);
  }

  private void toast(String text) {
    Toast.makeText(this, text, Toast.LENGTH_LONG).show();
  }

  private static String json(String... kv) {
    JSONObject o = new JSONObject();
    try {
      for (int i = 0; i + 1 < kv.length; i += 2) o.put(kv[i], kv[i + 1]);
    } catch (JSONException e) {
      throw new IllegalStateException(e);
    }
    return o.toString();
  }

  // ---- Debug commands, for testing over adb ----

  /**
   * adb shell am broadcast -a local.bentobook.DEBUG -p local.bentobook --es cmd ...
   * Only the shell can send these: the receiver requires android.permission.DUMP,
   * which apps can't hold. ./bb wraps them.
   */
  private void registerDebugCommands() {
    debug = new BroadcastReceiver() {
      @Override
      public void onReceive(Context context, Intent intent) {
        String cmd = intent.getStringExtra("cmd");
        if (cmd == null) return;
        switch (cmd) {
          case "devtools" -> {
            boolean on = intent.getBooleanExtra("on", true);
            store.setDevtools(on);
            WebView.setWebContentsDebuggingEnabled(on);
            Log.i(TAG, "devtools " + on);
          }
          case "reload" -> web.reload();
          case "open" -> web.loadUrl(Web.ORIGIN + intent.getStringExtra("path"));
          case "dump" -> Log.i(TAG, "state url=" + web.getUrl() + " title=" + web.getTitle()
              + " isolationAllowlist=" + isolated + " incoming=" + incoming.size());
          case "crash" -> web.loadUrl("chrome://crash");
          case "incoming" -> {
            // Test files, as if shared to BentoBook: saved to Download (the
            // shell can't grant this app another user's files), then offered.
            String name = intent.getStringExtra("name");
            byte[] bytes = android.util.Base64.decode(intent.getStringExtra("b64"), android.util.Base64.DEFAULT);
            if (!intent.getBooleanExtra("append", false)) incoming.clear();
            io.execute(() -> {
              try {
                String ext = name.substring(name.lastIndexOf('.') + 1).toLowerCase(java.util.Locale.ROOT);
                String mime = android.webkit.MimeTypeMap.getSingleton().getMimeTypeFromExtension(ext);
                Downloads d = new Downloads(MainActivity.this, name, mime, bytes.length);
                d.write(bytes);
                Uri uri = d.finish();
                main.post(() -> {
                  incoming.add(uri);
                  Log.i(TAG, "incoming test file " + name + " -> " + uri);
                  web.evaluateJavascript("window.bentobook && window.bentobook.postMessage("
                      + "JSON.stringify({type:'ready'}))", null);
                });
              } catch (IOException e) {
                Log.w(TAG, "incoming test file failed", e);
              }
            });
          }
          default -> Log.w(TAG, "unknown debug command " + cmd);
        }
      }
    };
    registerReceiver(debug, new IntentFilter("local.bentobook.DEBUG"),
        android.Manifest.permission.DUMP, null, Context.RECEIVER_EXPORTED);
  }
}
