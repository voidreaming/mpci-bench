# Third-party notices

## Privasis website

Source: https://github.com/privasis/privasis.github.io
Reference commit: d1226b766025060418654d81da3ce3913ef649db

Copyright (c) 2026 Hyunwoo Kim. The upstream MIT license is preserved verbatim in LICENSE. `dist/static/css/index.css` is copied from this source. The page structure, resource button styling, sidebar rules, and footer are adapted from its HTML. The benchmark text, figures, and tables are replaced; scripts are rewritten for the features used here. No upstream analytics are included.

## Nerfies template

Source: https://github.com/nerfies/nerfies.github.io

Privasis credits Nerfies and retains its Creative Commons Attribution-ShareAlike 4.0 notice. We preserve both attributions and release our adapted website template under the same CC BY-SA 4.0 terms: https://creativecommons.org/licenses/by-sa/4.0/ (legal text: https://creativecommons.org/licenses/by-sa/4.0/legalcode). The MIT permissions applying to upstream files remain in place. This template notice does not relicense the paper, its figures, or third-party datasets.

## Bulma 0.9.1

Source: https://github.com/jgthms/bulma/tree/0.9.1
`dist/static/css/bulma.min.css` is distributed under the MIT license. Its embedded license header is preserved. See LICENSES/Bulma-MIT.txt for the full upstream notice.

## Research content

Paper and figures: Shouju Wang and Haopeng Zhang, MPCI-Bench, arXiv:2601.08235v3. Included at the author's request. Source images in the paper originate from VISPR. Benchmark, code, and source-image terms remain those of their respective releases.

## Benchmark example excerpts

Six records (three pairs: `2017_89386002`, `2017_50310123`, `2017_99670226`) are reproduced from MPCI-Bench by Shouju Wang and Haopeng Zhang. Source: https://github.com/hpzhang94/MPCI-Bench/blob/bd85c6ec5c7aef81570da73081bdcbbe3af97893/dataset/mpci_bench.json.

The repository identifies the dataset license as CC BY 4.0: https://creativecommons.org/licenses/by/4.0/. The selected fields are preserved verbatim; only formatting, category labels, titles, and explanatory summaries are adapted for display. The excerpt contains synthetic stories and tool histories, not redistributed VISPR source images. Field-level provenance is included in `dist/static/data/examples.json`.

## Redrawn result figures

The scientific plots in `dist/assets/results/` are generated from Tables 4 and 5 of the author's paper. Exact plotted values and source links are included in `scripts/figure-data.json`; `scripts/render_figures.py` reproduces desktop and mobile versions.
