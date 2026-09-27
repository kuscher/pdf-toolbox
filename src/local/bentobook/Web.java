// SPDX-License-Identifier: MIT
package local.bentobook;

import android.content.Context;
import android.content.res.AssetManager;
import android.net.Uri;
import android.util.Log;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import androidx.webkit.JavaScriptReplyProxy;
import androidx.webkit.Profile;
import androidx.webkit.ProfileStore;
import androidx.webkit.WebMessageCompat;
import androidx.webkit.WebSettingsCompat;
import androidx.webkit.WebViewCompat;
import androidx.webkit.WebViewFeature;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;

/**
 * BentoPDF's web app, served from the APK's assets (assets/web) on a private
 * https origin, with the page shim and its message channel.
 */
final class Web {
  static final String TAG = "BentoBook";
  static final String HOST = "appassets.androidplatform.net";
  static final String ORIGIN = "https://" + HOST;
  static final String HOME = ORIGIN + "/";
  private static final String ROOT = "web";

  interface Listener {
    void onMessage(WebMessageCompat message, JavaScriptReplyProxy reply);
  }

  private Web() {}

  static void configure(WebView web, Context context, Listener listener) {
    WebSettings s = web.getSettings();
    s.setJavaScriptEnabled(true);
    s.setDomStorageEnabled(true);
    s.setAllowFileAccess(false);
    s.setAllowContentAccess(false);
    s.setSupportZoom(false);
    s.setBuiltInZoomControls(false);
    s.setTextZoom(100); // the system font size would otherwise scale only the text
    s.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
    s.setSupportMultipleWindows(false);
    if (WebViewFeature.isFeatureSupported(WebViewFeature.ALGORITHMIC_DARKENING)) {
      WebSettingsCompat.setAlgorithmicDarkeningAllowed(s, false); // BentoPDF has its own dark UI
    }
    Set<String> origin = Set.of(ORIGIN);
    // The channel object comes first so the shim finds it at document start.
    WebViewCompat.addWebMessageListener(web, "bentobook", origin,
        (view, message, source, mainFrame, reply) -> {
          if (mainFrame) listener.onMessage(message, reply);
        });
    WebViewCompat.addDocumentStartJavaScript(web, asset(context, "shell/page_shim.js"), origin);
  }

  /**
   * Turns on SharedArrayBuffer and the other cross-origin-isolated APIs for
   * the app's own origin. LibreOffice's WASM (Office to PDF) runs threads and
   * needs them. WebView keeps them off by default because it runs every page
   * in one renderer process; this origin only ever serves the APK's assets.
   * Pages also need the Document-Isolation-Policy header, see respond().
   */
  static boolean isolate() {
    if (!WebViewFeature.isFeatureSupported(WebViewFeature.MULTI_PROFILE)
        || !WebViewFeature.isFeatureSupported(WebViewFeature.CROSS_ORIGIN_ISOLATED_ALLOWLIST)) {
      return false;
    }
    Profile profile = ProfileStore.getInstance().getOrCreateProfile(Profile.DEFAULT_PROFILE_NAME);
    profile.setCrossOriginIsolatedAllowlist(Set.of(ORIGIN));
    return true;
  }

  static boolean isApp(Uri uri) {
    return uri != null && "https".equals(uri.getScheme()) && HOST.equals(uri.getHost());
  }

  /**
   * The site's files, the way BentoPDF's nginx and serve.json serve them:
   * clean URLs (/merge-pdf is merge-pdf.html), directory indexes, and the
   * app's index page for anything else. The service worker is left out: the
   * files are local already, and WebView would not route its fetches here.
   */
  static WebResourceResponse serve(Context context, Uri url) {
    String path = url.getPath();
    if (path == null || path.isEmpty()) path = "/";
    if (path.contains("..") || path.equals("/sw.js")) return notFound();
    // Ghostscript is laid out for BentoPDF (gs.js and gs.wasm at the top);
    // PyMuPDF asks for the npm package's assets/ folder. Same files.
    if (path.startsWith("/wasm/gs/assets/")) path = "/wasm/gs/" + path.substring(16);
    // Sign's viewer (pdfjs-viewer/sign-viewer.html) asks for pdf.js's data at
    // ../web/, where the pdf.js distribution keeps it; BentoPDF ships it in
    // pdfjs-viewer/. On a desktop the 404 goes unnoticed (pdf.js falls back
    // to system Helvetica/Arial); in WebView text in PDFs without embedded
    // fonts would not render at all.
    for (String dir : new String[] {"standard_fonts/", "cmaps/", "iccs/"}) {
      if (path.startsWith("/web/" + dir)) path = "/pdfjs-viewer/" + path.substring(5);
    }
    AssetManager assets = context.getAssets();
    List<String> candidates = path.endsWith("/")
        ? List.of(path + "index.html")
        : List.of(path, path + ".html", path + "/index.html");
    for (String candidate : candidates) {
      try {
        InputStream in = assets.open(ROOT + candidate, AssetManager.ACCESS_STREAMING);
        return respond(200, "OK", mime(candidate), in);
      } catch (FileNotFoundException e) {
        // next candidate
      } catch (IOException e) {
        Log.w(TAG, "can't read " + candidate, e);
      }
    }
    Log.d(TAG, "not in the app: " + path);
    return notFound();
  }

  private static WebResourceResponse notFound() {
    return respond(404, "Not Found", "text/plain",
        new ByteArrayInputStream("Not found".getBytes(StandardCharsets.UTF_8)));
  }

  private static WebResourceResponse respond(int status, String reason, String mime, InputStream in) {
    Map<String, String> headers = new HashMap<>();
    // Document-Isolation-Policy (with the allowlist from isolate()) is what
    // makes WebView cross-origin isolated. bentopdf.com's COOP/COEP headers
    // don't: WebView applies their restrictions but grants nothing.
    headers.put("Document-Isolation-Policy", "isolate-and-credentialless");
    headers.put("Cross-Origin-Resource-Policy", "same-origin");
    headers.put("X-Content-Type-Options", "nosniff");
    headers.put("Cache-Control", "no-cache");
    boolean text = mime.startsWith("text/") || mime.endsWith("javascript") || mime.endsWith("json")
        || mime.endsWith("xml");
    return new WebResourceResponse(mime, text ? "utf-8" : null, status, reason, headers, in);
  }

  private static final Map<String, String> TYPES = Map.ofEntries(
      Map.entry("html", "text/html"), Map.entry("htm", "text/html"),
      Map.entry("js", "text/javascript"), Map.entry("mjs", "text/javascript"),
      Map.entry("css", "text/css"), Map.entry("json", "application/json"),
      Map.entry("map", "application/json"), Map.entry("webmanifest", "application/manifest+json"),
      Map.entry("wasm", "application/wasm"), Map.entry("svg", "image/svg+xml"),
      Map.entry("png", "image/png"), Map.entry("jpg", "image/jpeg"), Map.entry("jpeg", "image/jpeg"),
      Map.entry("gif", "image/gif"), Map.entry("webp", "image/webp"), Map.entry("avif", "image/avif"),
      Map.entry("ico", "image/x-icon"), Map.entry("bmp", "image/bmp"),
      Map.entry("woff", "font/woff"), Map.entry("woff2", "font/woff2"), Map.entry("ttf", "font/ttf"),
      Map.entry("otf", "font/otf"), Map.entry("txt", "text/plain"), Map.entry("md", "text/markdown"),
      Map.entry("xml", "application/xml"), Map.entry("pdf", "application/pdf"),
      Map.entry("icc", "application/vnd.iccprofile"), Map.entry("bcmap", "application/octet-stream"),
      Map.entry("pfb", "application/octet-stream"), Map.entry("data", "application/octet-stream"),
      Map.entry("zip", "application/zip"), Map.entry("whl", "application/zip"),
      Map.entry("gz", "application/octet-stream"), Map.entry("tar", "application/x-tar"),
      Map.entry("py", "text/x-python"), Map.entry("traineddata", "application/octet-stream"));

  static String mime(String path) {
    String name = path.substring(path.lastIndexOf('/') + 1);
    int dot = name.lastIndexOf('.');
    String ext = dot < 0 ? "" : name.substring(dot + 1).toLowerCase(Locale.ROOT);
    String type = TYPES.get(ext);
    return type != null ? type : "application/octet-stream";
  }

  static String asset(Context context, String name) {
    try (InputStream in = context.getAssets().open(name)) {
      ByteArrayOutputStream out = new ByteArrayOutputStream();
      byte[] buf = new byte[8192];
      for (int n; (n = in.read(buf)) > 0; ) out.write(buf, 0, n);
      return out.toString(StandardCharsets.UTF_8);
    } catch (IOException e) {
      throw new IllegalStateException("missing asset " + name, e);
    }
  }
}
