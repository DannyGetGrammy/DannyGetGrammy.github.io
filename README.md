# Xinzichen Li — Personal Academic Website (V3)

An Academic Minimal research-first website for GitHub Pages. Uses only HTML, CSS, and a small navigation script (no npm or build step).

## Site structure

- `index.html` — homepage (About, Research, Publications, Selected Projects, Experience, Music & Creative Computing, Contact)
- `research/crona.html` and `research/mapl.html` — research detail pages
- `projects/soundbridge.html`, `projects/sarcasm.html`, `projects/strategy.html` — project detail pages
- `assets/style.css`, `assets/script.js` — shared styles and mobile navigation
- `assets/danny-li-logo.png`, `assets/favicon.png` — derived *only by transparent trimming/resizing* from the supplied personal logo

**There is no CV attachment or CV link in this version.** All placeholder imagery uses the text `Insert Picture`.

## Publish to GitHub Pages

1. Create a public repository named `<your-username>.github.io`, for example `DannyGetGrammy.github.io` for the GitHub account used by the SoundBridge repo.
2. Upload the **contents of this folder** (not the ZIP itself) to the repository root, keeping `assets/`, `research/`, and `projects/` intact.
3. In **Settings → Pages**, select **Deploy from a branch → main → /(root)**.
4. Open the URL shown under Pages after deployment completes.

Alternatively, keep the site in a normal repo and enable Pages; internal relative links also work in a repo subpath.

## Preview locally

From the unpacked folder run `python3 -m http.server 8000`, then visit `http://localhost:8000/`.

## Before publishing

- Confirm disclosure/anonymity policy for the CRONA paper during double-blind peer review.
- Check the research credit and project wording against what you want to disclose publicly.
- Replace `Insert Picture` with approved figures/portrait/demo screenshots. Avoid adding unpublished/identifying materials contrary to conference guidelines.
- Add a public SoundBridge demo URL only when you have actually deployed it.



## Chinese version

The original pages are English; `zh/` contains their Simplified Chinese counterparts.
The header language link opens the matching page and keeps the current section.
Both versions work as static GitHub Pages pages, including without JavaScript.

After editing English page text, update the matching entries in
`translations/zh-CN.json`, then regenerate Chinese pages from the repository root:

```bash
python3 tools/build_zh.py
```

The generator uses only the Python standard library. It rejects new text without
a translation entry. Names, project names, and technical identifiers intentionally
retain their original spelling. Commit the generated `zh/` pages along with the
English pages and translation changes.
