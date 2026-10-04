# MPCI-Bench project page

Redirect and asset archive for **MPCI-Bench: A Benchmark for Multimodal Pairwise Contextual Integrity Evaluation of Language Model Agents**. The active project website is now part of Shouju Wang’s personal site.

- Website: https://shouju-wang.github.io/mpci-bench/
- Active source: https://github.com/shouju-wang/shouju-wang.github.io/tree/master/mpci-bench
- Paper: https://arxiv.org/abs/2601.08235
- Benchmark code: https://github.com/hpzhang94/MPCI-Bench
- Dataset: https://huggingface.co/datasets/Soojuu/mpci-bench

## Template

This site directly adapts the [Privasis project page](https://github.com/privasis/privasis.github.io), based on [Nerfies](https://github.com/nerfies/nerfies.github.io). It reuses Privasis's Bulma stylesheet and original `index.css`, hero structure, resource buttons, article layout, sidebar, and footer attribution. Paper content, tables, and figures are replaced with MPCI-Bench material. The reading order is overview with the three-tier example figure, construction figure, illustrated paired examples, then results. A More Research menu links related work. Short explanations introduce contextual integrity, the three tiers, and the evaluation metrics. The action chart and numeric table appear side by side on desktop and stack on smaller screens. Examples show the actual VISPR image and two short context summaries; original Seed/Story/Trace fields are available on demand. No analytics or build dependencies are included.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [LICENSE](LICENSE) for upstream licenses and attribution.

## Preview this redirect locally

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory dist
```

Open http://localhost:8765.

## Edit and publish the project website

Make future website changes in [`shouju-wang/shouju-wang.github.io`, `mpci-bench/`](https://github.com/shouju-wang/shouju-wang.github.io/tree/master/mpci-bench). The project’s `index.html`, `static/`, and `assets/` are under that directory. Preview the personal-site repository root, then publish by pushing its `master` branch; GitHub Pages serves that branch’s root.

This repository now maintains the old address and direct asset access. `dist/index.html` redirects to the new website, preserving query parameters and section anchors when JavaScript is available. A no-JavaScript refresh and visible link provide fallbacks. The existing `dist/assets/`, `dist/static/`, licenses, and Git history remain available, so previously shared PDF, image, and data URLs continue to work. Pushing this repository’s `main` branch publishes only this redirect/archive through `.github/workflows/pages.yml`.

The reproduction resources are retained here:

- `scripts/figure-data.json`: exact Table 4/5 values and source links.
- `scripts/render_figures.py`: reproduce plots with Python and Matplotlib. It writes to this repository’s retained asset directory; review and copy updated outputs into the active source before publishing them.
- `scripts/embed_examples.py`: original helper for embedding benchmark examples, preserved for historical reproduction. Run it against a historical checkout containing the full landing page, not the current redirect.
- `dist/static/data/examples.json`: paired benchmark excerpts, exact fields, editorial annotations, and provenance.
- `dist/assets/examples/attributions.json`: source-photo credits and hashes.

## Paper version

Figures, affiliations, and results come from [arXiv v3, January 26, 2026](https://arxiv.org/html/2601.08235v3). Results reproduce Tables 4 and 5, which differ from some accompanying prose. The NeurIPS 2026 ED Track acceptance is supplied by the author. The citation uses verified arXiv metadata; no proceedings metadata has been invented. VISPR source images are obtained separately following the benchmark repository instructions. This site includes three original Flickr photos referenced by VISPR training annotations, each licensed CC BY 2.0 and individually credited. The source photos are unchanged. See `dist/assets/examples/attributions.json` for original URLs and hashes. The site also includes paper figures and plots redrawn from the result tables. Three example pairs are drawn from the released benchmark at commit `bd85c6ec5c7aef81570da73081bdcbbe3af97893`. Original seed, story, and trace fields remain verbatim; category titles and short explanations are editorial additions. Positive/negative labels refer specifically to image sharing. The traces are synthetic evaluation inputs, not evaluated model outputs.
