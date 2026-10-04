#!/usr/bin/env python3
"""Embed the downloadable example snapshot for a self-contained browser explorer."""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
page = root / 'dist/index.html'
data = json.loads((root / 'dist/static/data/examples.json').read_text())
payload = json.dumps(data, ensure_ascii=False).replace('<', r'\u003c').replace('>', r'\u003e').replace('&', r'\u0026')
pattern = r'(<script type="application/json" id="example-data">).*?(</script>)'
updated, count = re.subn(pattern, lambda match: match[1] + payload + match[2], page.read_text(), flags=re.S)
if count != 1:
    raise SystemExit('Expected exactly one example-data script block')
page.write_text(updated)
