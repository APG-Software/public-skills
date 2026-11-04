"""Turn a rendered HTML page into a PDF.

Uses headless Chrome (or Chromium/Edge), which is already on every machine here,
needs no install, and honours the same print CSS the browser preview shows. About
three seconds a page. Falls back to WeasyPrint where it happens to be installed.

Deliberately does NOT pass --user-data-dir. Pointing Chrome at a scratch profile
makes it hang for a minute or more on a managed macOS install; letting it use the
default profile location keeps a render at ~3s.

Never claims a PDF was produced when it was not. The caller reports what came back.
"""
from __future__ import annotations

import glob
import os
import shutil
import subprocess
import sys
from pathlib import Path

CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "google-chrome", "chromium", "chromium-browser", "microsoft-edge",
)

# Sandboxed Linux workspaces (Cowork, CI) often ship a Playwright Chromium that is not on PATH.
PLAYWRIGHT_GLOBS = (
    "/opt/pw-browsers/chromium*/chrome-linux*/chrome",
    os.path.expanduser("~/.cache/ms-playwright/chromium*/chrome-linux*/chrome"),
    "/ms-playwright/chromium*/chrome-linux*/chrome",
)


def find_chrome():
    for candidate in CHROME_CANDIDATES:
        if "/" in candidate and Path(candidate).exists():
            return candidate
        found = shutil.which(candidate)
        if found:
            return found
    for pattern in PLAYWRIGHT_GLOBS:
        hits = sorted(glob.glob(pattern))
        if hits:
            return hits[-1]
    return None


def html_to_pdf(html_path, pdf_path, timeout=60):
    """Render html_path to pdf_path. Returns (ok, message)."""
    html_path, pdf_path = Path(html_path).resolve(), Path(pdf_path)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    if pdf_path.exists():
        pdf_path.unlink()

    chrome = find_chrome()
    if chrome:
        command = [
            chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
            "--virtual-time-budget=5000",
            f"--print-to-pdf={pdf_path.resolve()}",
            html_path.as_uri(),
        ]
        if sys.platform.startswith("linux"):
            # Containers usually cannot use Chrome's sandbox or a large /dev/shm.
            command[1:1] = ["--no-sandbox", "--disable-dev-shm-usage"]
        try:
            subprocess.run(command, capture_output=True, timeout=timeout, check=False)
        except subprocess.TimeoutExpired:
            return False, (f"PDF: NOT PRODUCED - {Path(chrome).name} timed out after "
                           f"{timeout}s. The HTML is complete; print it from the browser.")
        if pdf_path.exists() and pdf_path.stat().st_size > 0:
            return True, f"PDF: {pdf_path}"

    try:
        from weasyprint import HTML
    except ImportError:
        if chrome:
            return False, ("PDF: NOT PRODUCED - headless Chrome ran but wrote nothing, and "
                           "WeasyPrint is not installed. The HTML is complete.")
        return False, ("PDF: NOT PRODUCED - no Chrome, Chromium or Edge found, and "
                       "WeasyPrint is not installed. The HTML is complete.")
    HTML(filename=str(html_path), base_url=str(html_path.parent)).write_pdf(str(pdf_path))
    return True, f"PDF: {pdf_path} (WeasyPrint)"
