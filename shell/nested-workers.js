// SPDX-License-Identifier: MIT
// (build.sh prepends it to a file of the LibreOffice converter, which is
// MPL-2.0; the MIT License lets it go out under the MPL as part of that file.)
// PDF Toolbox, prepended by build.sh to worker scripts that start workers of
// their own (LibreOffice's converter starts four Emscripten thread workers).
// WebView never answers the script request of a worker started from inside
// another worker: it can't route it to the app's asset server, and the
// worker waits forever. So such workers start from a Blob of their script,
// fetched here, where requests do reach the app.
(() => {
  const RealWorker = self.Worker;
  if (!RealWorker || typeof WorkerGlobalScope === 'undefined') return;
  const blobs = new Map();
  const local = (url) => {
    try {
      const abs = new URL(url, self.location.href);
      return abs.origin === self.location.origin && abs.protocol === 'https:' ? abs.href : null;
    } catch {
      return null;
    }
  };
  function Worker(url, options) {
    const abs = (typeof url === 'string' || url instanceof URL) ? local(url) : null;
    if (abs) {
      let blobUrl = blobs.get(abs);
      if (!blobUrl) {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', abs, false);
        xhr.send();
        if (xhr.status === 200) {
          blobUrl = URL.createObjectURL(new Blob([xhr.responseText], { type: 'text/javascript' }));
          blobs.set(abs, blobUrl);
        }
      }
      if (blobUrl) return new RealWorker(blobUrl, options);
    }
    return new RealWorker(url, options);
  }
  Worker.prototype = RealWorker.prototype;
  self.Worker = Worker;
})();
