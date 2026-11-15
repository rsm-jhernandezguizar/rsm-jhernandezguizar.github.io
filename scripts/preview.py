"""Render the portfolio when Quarto is available, then open a private local preview."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil
import subprocess
import threading
import webbrowser


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
            subprocess.run([shutil.which("python3") or "python3", "scripts/render_profile.py"], cwd=root, check=True)
            for page in ("index.qmd", "Resume.qmd", "portfolio/crea-circuitos-youtube/index.qmd"):
                subprocess.run([quarto, "render", page, "--no-execute"], cwd=root, check=True)
        else:
            print("Quarto is not installed; showing the rendered HTML committed with this PR.", flush=True)
    directory = root / "docs"
    if not (directory / "index.html").is_file():
        parser.error("No rendered website found. Install Quarto and run the preview again.")
    handler = partial(SimpleHTTPRequestHandler, directory=str(directory))
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
