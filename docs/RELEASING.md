# Releasing PDF Toolbox

A release is a pushed tag. GitHub Actions builds the app, signs it with the
release key and publishes it, so nobody needs the key on their machine.

## Steps

1. In `AndroidManifest.xml`, raise `android:versionCode` by one and set
   `android:versionName` (Google Play takes each version code once).
2. Add a `## <version> (<date>)` section at the top of `CHANGELOG.md`. It becomes
   the GitHub release's notes.
3. Write Google Play's "What's new" in
   `store-submission/listing/en-US/release-notes.txt`: plain text, at most 500
   characters.
4. Build and test: `./build.sh`, then `./ptb smoke` on a Googlebook. A build
   signed with the test key is fine for this.
   The build rewrites `THIRD_PARTY_NOTICES.md` and
   `licenses/javascript-packages.txt` with the new version: commit them too, or
   the release run stops at "commit first" (it wants a clean checkout).
5. Commit and push to `main`. The x86_64 workflow builds that commit and runs
   the smoke test in the emulator: wait for it.
6. Tag the commit and push the tag:

   ```sh
   git tag v0.8 && git push origin v0.8
   ```

## What the tag does

The tag starts the Release workflow (`.github/workflows/release.yml`), which
takes about five minutes:

- It checks that `CHANGELOG.md` has a section for the version, that
  `versionName` in `AndroidManifest.xml` is the tag's version, and that the
  "What's new" text has at most 500 characters.
- It builds the APK (`./build.sh`) and the bundle for Google Play
  (`tools/aab.sh`) from scratch, without a cache, signed with the release key.
- It checks the certificate of both against the release key's fingerprint, and
  stops if either is signed with anything else (the test key, for one).
- It makes the release files with `tools/release.sh` and publishes them as the
  GitHub release "PDF Toolbox <version>": `PDFToolbox.apk` (the README's
  download link depends on this name), `PDFToolbox-<version>-source.tar.gz`,
  `PDFToolbox-<version>-third-party-sources.tar` and `SHA256SUMS`.
- It puts the bundle on Google Play's closed-testing track as a **draft**, with
  the "What's new" text (`tools/play-upload.mjs`). What is live there stays. If
  that version code is on Play already, it uploads nothing.

A draft is not served to anyone and not reviewed. Someone still opens the Play
Console and presses **Send for review**: nothing goes to review automatically.

The bundle is about 188 MB, and Google Play's limit for the app is a 200 MB
download. The workflow prints the bundle's size and warns when it reaches
200 MB.

## A dry run

On the Actions tab, choose **Release**, then **Run workflow** on `main` (or
`gh workflow run release.yml --ref main`). It does the same signed build and the
same checks, makes the release files, and publishes nothing: no GitHub release,
and on Google Play it only checks that the Play key works. Do this after
changing the workflow or the build scripts.

## The key

The release key (alias `pdftoolbox`, certificate SHA-256
`01:ED:3C:81:45:A8:CB:8B:F8:99:59:79:4F:53:BD:74:01:E5:07:CF:6D:80:C0:C3:D2:D9:B6:EB:EF:AF:62:3E`)
is the same for the APK on GitHub and for Google Play, where it is the app
signing key and the upload key. It is never in the repository:

- GitHub has it as secrets of the environment `release`
  (`SIGNING_KEYSTORE_B64`, `SIGNING_KEYSTORE_PASS`). The Play key is the secret
  `PLAY_SERVICE_ACCOUNT_JSON` of the environment `play`. Both environments only
  serve `main` and `v*` tags, so pull requests and forks never get them.
- The maintainer has a backup in a private folder.

Agents and contributors never need the key file. The job that holds the key
runs only GitHub's own actions, pinned to exact commits, and removes the key
when it ends.

## By hand

On a machine that has the key in `~/.config/pdf-toolbox` (`keystore.jks`,
`keystore.pass`), the local route still works:

```sh
./build.sh && ./ptb release --publish   # tags, pushes the tag, makes the GitHub release
tools/aab.sh                            # build/PDFToolbox.aab, to upload in the Play Console
```

The tag it pushes starts the Release workflow too. That run leaves the release
you made as it is, and still builds the bundle and puts it on Google Play as a
draft.

## If a run fails

- **Before "Publish on GitHub":** nothing is published. Fix it on `main`, delete
  the tag (`git push origin :v0.8`, `git tag -d v0.8`) and tag again.
- **In the Google Play job:** the GitHub release is out and the bundle is the
  run's `bundle` artifact (kept for 30 days). Choose **Re-run failed jobs**,
  which uploads that same bundle, or download the artifact and add it to the
  closed-testing track in the Play Console.
