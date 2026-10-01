# Data safety (Play Console › Policy › App content › Data safety)

Google's definition: data is "collected" when it leaves the device. Data handled only on the device isn't collected.

1. **Does your app collect or share any of the required user data types?** No.
   - Network: none. The manifest declares no permissions at all, `INTERNET` included (checked in the 0.7 (8) bundle with
     `bundletool dump manifest`). BentoPDF's pages and engines are served from the APK to the app's WebView through
     `shouldInterceptRequest`, which isn't a network load; WebView blocks real network loads. Nothing can be sent anywhere.
     Links to websites open in the user's browser, which is a separate app.
   - No analytics, crash reporting, ads or other SDKs. The only library is androidx.webkit.
   - On the device only: the files the user picks (Android's file picker, Open with, Share) are read through the
     content URIs Android hands over for those files, processed in the app, and the results written to Download
     through MediaStore, which needs no permission for files the app creates. Settings (recent tools, sidebar
     layout, window colour) stay in the app's private storage; `android:allowBackup="false"` keeps them out of
     Android backups, and uninstalling deletes them.
2. The security questions (encryption in transit, deletion requests) don't apply when nothing is collected.

Resulting label: **No data collected. No data shared with third parties.**
