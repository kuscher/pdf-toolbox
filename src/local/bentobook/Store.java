package local.bentobook;

import android.content.Context;
import android.content.SharedPreferences;

/** The app's few settings, in private storage. */
final class Store {
  /** BentoPDF's page background (Tailwind gray-900) until the page reports its own. */
  static final int DEFAULT_THEME = 0xFF111827;

  private final SharedPreferences prefs;

  Store(Context context) {
    prefs = context.getSharedPreferences("bentobook", Context.MODE_PRIVATE);
  }

  /** The page's last top colour, so the window opens in it. */
  int theme() { return prefs.getInt("theme", DEFAULT_THEME); }
  void setTheme(int color) { prefs.edit().putInt("theme", color).apply(); }

  boolean devtools() { return prefs.getBoolean("devtools", false); }
  void setDevtools(boolean on) { prefs.edit().putBoolean("devtools", on).apply(); }
}
