# MPCI-Bench project page

Academic project website for **MPCI-Bench: A Benchmark for Multimodal Pairwise Contextual Integrity Evaluation of Language Model Agents**.

- Website: https://voidreaming.github.io/mpci-bench/
- Paper: https://arxiv.org/abs/2601.08235
- Benchmark code: https://github.com/hpzhang94/MPCI-Bench
- Dataset: https://huggingface.co/datasets/Soojuu/mpci-bench

## Template

This site directly adapts the [Privasis project page](https://github.com/privasis/privasis.github.io), based on [Nerfies](https://github.com/nerfies/nerfies.github.io). It reuses Privasis's Bulma stylesheet and original `index.css`, hero structure, resource buttons, article layout, sidebar, and footer attribution. Paper content, tables, and figures are replaced with MPCI-Bench material. The reading order is overview, construction figure, illustrated paired examples, then results. Examples show the actual VISPR image and two short context summaries; original Seed/Story/Trace fields are available on demand. No analytics or build dependencies are included.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [LICENSE](LICENSE) for upstream licenses and attribution.

## Preview locally

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory dist
```

Open http://localhost:8765.

## Edit and publish

- `dist/index.html`: title, authors, venue, sections, results, links, and citation.
- `dist/static/css/mpci.css`: small responsive and accessibility adaptations.
- `dist/static/css/index.css` and `bulma.min.css`: original upstream styles.
- `dist/static/js/mpci.js`: navigation, lightbox, citation copying.
- `dist/static/js/examples.js`: domain tabs and Seed/Story/Trace pair views.
- `dist/static/data/examples.json`: three paired benchmark excerpts, exact fields, editorial annotations, and pinned provenance. After editing, run `python3 scripts/embed_examples.py` to synchronize the inline data.
- `dist/assets/`: original paper figures; `results/` contains desktop/mobile SVG and PNG result plots. `examples/` contains the three unmodified source photos and their attribution manifest.
- `scripts/figure-data.json`: exact Table 4/5 values and source links.
- `scripts/render_figures.py`: reproduce the plots with Python and Matplotlib (`python3 scripts/render_figures.py`). This is optional; the website serves the committed assets without a build.

GitHub Pages publishes `dist/` on pushes to `main` via `.github/workflows/pages.yml`. In repository Settings → Pages, use **GitHub Actions** as the source.

All local asset paths are relative, so the site supports both a project URL such as `voidreaming.github.io/mpci-bench/` and an organization root such as `mpci-bench.github.io`. The latter requires an organization/account named `mpci-bench` and a repository named `mpci-bench.github.io`. Update the website/source links when moving.

## Paper version

Figures, affiliations, and results come from [arXiv v3, January 26, 2026](https://arxiv.org/html/2601.08235v3). Results reproduce Tables 4 and 5, which differ from some accompanying prose. The NeurIPS 2026 ED Track acceptance is supplied by the author. The citation uses verified arXiv metadata; no proceedings metadata has been invented. VISPR source images are obtained separately following the benchmark repository instructions. This site includes three original Flickr photos referenced by VISPR training annotations, each licensed CC BY 2.0 and individually credited. The source photos are unchanged. See `dist/assets/examples/attributions.json` for original URLs and hashes. The site also includes paper figures and plots redrawn from the result tables. Three example pairs are drawn from the released benchmark at commit `bd85c6ec5c7aef81570da73081bdcbbe3af97893`. Original seed, story, and trace fields remain verbatim; category titles and short explanations are editorial additions. Positive/negative labels refer specifically to image sharing. The traces are synthetic evaluation inputs, not evaluated model outputs.
