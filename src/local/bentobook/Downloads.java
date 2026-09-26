package local.bentobook;

import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Context;
import android.net.Uri;
import android.provider.MediaStore;
import java.io.IOException;
import java.io.OutputStream;

/**
 * One file BentoPDF saves, written to Android's Download folder as its bytes
 * arrive from the page (in chunks, so a big PDF never sits in one message).
 * MediaStore needs no permission for files the app creates.
 */
final class Downloads {
  final String name;
  final long size;
  private final ContentResolver resolver;
  private Uri uri;
  private OutputStream out;
  private long written;

  Downloads(Context context, String name, String mime, long size) throws IOException {
    this.name = name;
    this.size = size;
    resolver = context.getContentResolver();
    ContentValues values = new ContentValues();
    values.put(MediaStore.Downloads.DISPLAY_NAME, name);
    values.put(MediaStore.Downloads.MIME_TYPE, mime == null || mime.isEmpty() ? "application/octet-stream" : mime);
    values.put(MediaStore.Downloads.IS_PENDING, 1);
    uri = resolver.insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, values);
    if (uri == null) throw new IOException("MediaStore refused " + name);
    out = resolver.openOutputStream(uri, "w");
    if (out == null) {
      abort();
      throw new IOException("can't write " + uri);
    }
  }

  void write(byte[] chunk) throws IOException {
    out.write(chunk);
    written += chunk.length;
  }

  /** Publishes the file; returns its content URI. */
  Uri finish() throws IOException {
    out.close();
    if (size >= 0 && written != size) {
      abort();
      throw new IOException(name + ": got " + written + " of " + size + " bytes");
    }
    ContentValues values = new ContentValues();
    values.put(MediaStore.Downloads.IS_PENDING, 0);
    resolver.update(uri, values, null, null);
    return uri;
  }

  void abort() {
    try {
      if (out != null) out.close();
    } catch (IOException ignored) {
      // deleting it anyway
    }
    if (uri != null) resolver.delete(uri, null, null);
    uri = null;
  }

  /** The name Download/ shows for it: MediaStore adds " (1)" and so on to duplicates. */
  static String displayName(Context context, Uri uri, String fallback) {
    try (android.database.Cursor c = context.getContentResolver().query(uri,
        new String[] {MediaStore.Downloads.DISPLAY_NAME}, null, null, null)) {
      if (c != null && c.moveToFirst()) return c.getString(0);
    } catch (RuntimeException ignored) {
      // fall back
    }
    return fallback;
  }
}
