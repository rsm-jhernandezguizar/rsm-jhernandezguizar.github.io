"""Render the portfolio when Quarto is available, then open a private local preview."""
import argparse
import html
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil
import subprocess
import threading
import webbrowser
from urllib.parse import parse_qs, urlsplit


class ReviewHandler(SimpleHTTPRequestHandler):
    """Add opt-in review highlights without changing production HTML."""

    def do_GET(self):
        root = Path(__file__).resolve().parents[1]
        changes = json.loads((root / "review-changes.json").read_text(encoding="utf-8"))
        url = urlsplit(self.path)
        if url.path == "/__changes__":
            rows = "".join(
                f'<tr><td>{html.escape(c["page"])}</td>'
                f'<td><del>{html.escape(c["before"])}</del></td>'
                f'<td><mark>{html.escape(c["after"])}</mark></td>'
                f'<td>{html.escape(c["reason"])}</td></tr>' for c in changes
            )
            text = ('<!doctype html><html lang="en"><meta charset="utf-8">'
                    '<meta name="viewport" content="width=device-width,initial-scale=1">'
                    '<title>PR #1 — Targeted changes</title><style>'
                    'body{font:16px/1.5 system-ui;margin:32px;color:#182b40}'
                    'table{border-collapse:collapse}td,th{padding:12px;border:1px solid #ccc;text-align:left}'
                    'mark{background:#fff2a8}a{color:#1846d6}</style>'
                    '<h1>PR #1 — Targeted changes</h1>'
                    '<p>Original layout restored. Only the corrections below remain.</p>'
                    '<p><a href="/?highlight=1">Highlighted homepage</a> · '
                    '<a href="/Resume.html?highlight=1">Highlighted résumé</a> · '
                    '<a href="/">Clean preview</a></p>'
                    '<table><tr><th>Page</th><th>Before</th><th>After</th><th>Reason</th></tr>'
                    + rows + '</table></html>')
        elif parse_qs(url.query).get("highlight") == ["1"] and url.path in ("/", "/index.html", "/Resume.html"):
            page = "index.html" if url.path in ("/", "/index.html") else "Resume.html"
            text = (root / "docs" / page).read_text(encoding="utf-8")
            for change in changes:
                if change["page"] == page:
                    marked = ('<mark style="background:#fff2a8;color:inherit;padding:0;" '
                              f'title="Previously: {html.escape(change["before"], quote=True)}">'
                              + html.escape(change["after"]) + '</mark>')
                    text = text.replace(html.escape(change["after"]), marked)
            banner = ('<aside style="position:fixed;bottom:12px;right:12px;z-index:99999;'
                      'background:#172b45;color:white;padding:12px;border-radius:8px;max-width:90vw;'
                      'font:14px system-ui;box-shadow:0 3px 14px #0004">'
                      'Review only: yellow marks show changed text. '
                      '<a style="color:#fff2a8" href="/__changes__">Before / after</a> · '
                      f'<a style="color:#fff2a8" href="/{page}">Clean preview</a></aside>')
            text = text.replace('</body>', banner + '</body>')
        else:
            return super().do_GET()
        body = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-render", action="store_true", help="Use the committed HTML preview")
    parser.add_argument("--no-open", action="store_true", help="Print the URL without opening a browser")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if not args.skip_render:
        quarto = shutil.which("quarto")
        if quarto:
            for page in ("index.qmd", "Resume.qmd"):
                subprocess.run([quarto, "render", page, "--no-execute"], cwd=root, check=True)
        else:
            print("Quarto is not installed; showing the rendered HTML committed with this PR.", flush=True)
    directory = root / "docs"
    if not (directory / "index.html").is_file():
        parser.error("No rendered website found. Install Quarto and run the preview again.")
    handler = partial(ReviewHandler, directory=str(directory))
    for port in range(args.port, min(args.port + 20, 65536)):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", port), handler)
            break
        except PermissionError:
            parser.error("This environment blocked the local server. Allow local network access and retry.")
        except OSError:
            continue
    else:
        parser.error("No local preview port is available. Try --port 9000.")
    url = f"http://127.0.0.1:{server.server_port}/"
    print(f"\nWebsite preview: {url}", flush=True)
    print(f"Resume: {url}Resume.html", flush=True)
    print(f"Highlighted changes: {url}?highlight=1", flush=True)
    print(f"Before / after: {url}__changes__", flush=True)
    print("Only available on this computer. Press Ctrl+C to stop.\n", flush=True)
    if not args.no_open:
        threading.Timer(0.5, webbrowser.open, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
