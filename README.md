# MPCI-Bench paper website

A standalone static website inspired by the academic layout of Privasis. No build or JavaScript framework required.

## Local preview

```sh
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. For GitHub Pages or another static host, publish the contents of `dist/`.

## Editing

- `dist/index.html`: paper content, authors, venue, resource links, citation.
- `dist/style.css`: responsive styling.
- `dist/app.js`: tier tabs, model-family filter, Table 4 values, citation copying.
- `dist/assets/`: original paper figures and a site favicon.

## Content provenance

Paper: https://arxiv.org/html/2601.08235v3 (January 26, 2026).
GitHub: https://github.com/hpzhang94/MPCI-Bench
Dataset: https://huggingface.co/datasets/Soojuu/mpci-bench

Acceptance wording comes from the author’s instruction: NeurIPS 2026 ED Track. Affiliations, figures, and results come from arXiv v3, not a supplied camera-ready version. Results use Tables 4 and 5 because some accompanying prose gives conflicting numbers. Citation remains the verified arXiv citation rather than inventing proceedings metadata. Source VISPR images are not redistributed, apart from their appearance in the author's supplied paper figure. Fonts load from Google Fonts with local sans-serif fallbacks.
