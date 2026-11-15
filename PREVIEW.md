# Preview the website

On this Mac, double-click **Preview website.command** in the repository folder. It opens the website in your browser and keeps the local preview running in Terminal. Close that Terminal window when finished.

If working with Codex, ask **"Preview PR #1"**. Codex should fetch the PR, start the preview, open it in the app, and give you a clickable URL without requiring terminal work.

For focused review, use <http://127.0.0.1:8765/?highlight=1> for yellow highlights and <http://127.0.0.1:8765/__changes__> for the before/after table. Highlights are added only by the local preview server; published pages keep their original formatting.

## One-command alternative

```sh
python3 scripts/preview.py
```

The script renders the updated pages if Quarto is installed. Otherwise it serves the rendered HTML included with the PR. It uses only Python's standard library and binds to `127.0.0.1`, so it does not publish the draft or expose it to the network.

The default link is <http://127.0.0.1:8765/>; if that port is busy, the script prints the available port it selected. The preview is available only on the computer running the script, while it is running.

For automation: `python3 scripts/preview.py --skip-render --no-open` serves the committed HTML without opening an external browser.

Quarto's [post-render hook](https://quarto.org/docs/projects/scripts.html#pre-and-post-render) runs `scripts/version_styles.py`. Rendered pages reference a content-hashed copy of the custom CSS so browsers load approved style updates instead of an older cached file. The source remains `styles.css`; prior hashed assets are retained for cached pages. Run `python3 -m unittest discover -s scripts -p 'test_*.py'` to check this behavior.
