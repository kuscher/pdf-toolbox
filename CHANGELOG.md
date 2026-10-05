# What's new in PDF Toolbox

PDF Toolbox was called BentoBook up to version 0.5.

## 0.7.2 (2026-10-05)

- **About & licenses** names Fika Labs, the name PDF Toolbox is published
  under, links to the privacy policy, and says where to report a problem.
- **Updates:** About says that Google Play keeps PDF Toolbox up to date when
  it was installed from there. The APK on GitHub and the one from Google Play
  have the same signature, so either updates the other.

## 0.7.1 (2026-10-01)

- **On Google Play, PDF Toolbox is for Googlebooks only.** Play offers it to
  devices that report themselves as a PC and run Android 14 or newer, which are
  the Googlebooks. Nothing changes in the app, and the APK from GitHub still
  installs anywhere.

## 0.7 (2026-09-30)

- **Export PDF in the Markdown editor** brings the sidebar back as soon as the
  print dialog closes. On a Googlebook it stayed hidden until the next click.
- **A permanent package name, `io.github.kuscher.pdftoolbox`**, in place of the
  placeholder `local.pdftoolbox`, so PDF Toolbox can go to the Play Store. To
  Android it is a new app: this version installs next to 0.6.1 instead of
  updating it. Once it works, uninstall the old PDF Toolbox (files you made stay
  in your Download folder).
- **Open with and Share while PDF Toolbox is open** no longer drop the file into
  the tool on screen. The bar says the file is waiting, as when the app starts,
  and the next tool you open takes it; **Use here** puts it into the open tool.

## 0.6.1 (2026-09-28)

- **About & licenses** now says what PDF Toolbox is: a personal passion
  project, not affiliated with my employer, made on a Googlebook in its Linux
  Terminal.

## 0.6 (2026-09-27)

- **BentoBook is now PDF Toolbox.** It installs as a new app next to BentoBook:
  once PDF Toolbox works, uninstall BentoBook.
- **A sidebar with every tool**, by category, with search (**Ctrl+K**) and your
  recent tools. A tool opens in the full-height pane next to it, so you can go
  from one tool to the next without going back to the tool list.
- **Ctrl+B** folds the sidebar into a row of icons, where each category's icon
  opens its tools; in a narrow window it folds by itself and opens over the tool.
- **More room for the tools:** BentoPDF's top bar, its breadcrumbs, the tools'
  Back to Tools links and the PDF Multi Tool's header make way for the pane,
  and full-page tools such as the PDF Multi Tool and the Workflow Builder fill
  it.
- PDF Toolbox's name and icon replace BentoPDF's logo inside the tools, through
  BentoPDF's own branding option; About & licenses credits BentoPDF.

## 0.5 (2026-09-27)

- **Every Googlebook, one APK.** BentoBook has no native code: the same APK runs
  on Intel (x86_64) and Arm (Snapdragon, MediaTek) Googlebooks. It is tested on
  an Arm Googlebook, and its engines on x86_64 in Google's Android emulator.
- **New icon** in the Material 3 Expressive style, with a monochrome version
  for themed icons.
- **About & licenses**, at the top right of every page: BentoBook's version,
  its license, where its source is, and every component the app contains with
  its license text.
- **Downloads on GitHub:** each release carries the APK, its checksum and the
  complete source.
- **New signing key.** If you have BentoBook 0.4 or older, uninstall it before
  installing 0.5: Android won't update an app signed with a different key.
  From 0.5 on, updates install over each other as usual.
- BentoBook's own code is now under the MIT License.

## 0.4 (2026-09-26)

- **Live window resizing** (optional): with one adb command, the page follows
  the window edge while you drag it, instead of hiding behind a veil until you
  let go. See [Live window resizing](README.md#live-window-resizing).

## 0.3 (2026-09-26)

- **A compact tool header:** once your file is in, a tool's title and drop
  area fold into a slim bar (← Tools, the tool, your file, Change file,
  Details), and viewers such as Sign, PDF Editor and Crop fill the window.
- Fixed, offline: text in Sign's viewer was invisible for PDFs without embedded
  fonts, and the PDF Editor's pages stayed blank.

## 0.2 (2026-09-26)

- A tool's workspace moves to the top of the window once a file is in.

## 0.1 (2026-09-26)

- First version: BentoPDF 2.8.8's PDF tools in an offline Android app, with the
  file picker, downloads to your Download folder, Open with and Share, printing
  and a desktop window. Office to PDF (LibreOffice) runs in the app.
