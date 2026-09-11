"""Read-only evidence extraction. Never recalculate or save the original files."""
from pathlib import Path
import hashlib
import json
import zipfile
import xml.etree.ElementTree as ET
import openpyxl

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / 'OneDrive_2026-09-11'
OUT = ROOT / 'docs' / 'evidence'
OUT.mkdir(exist_ok=True)
manifest = {}
for path in sorted(CORPUS.rglob('*')):
    if not path.is_file():
        continue
    relative = path.relative_to(ROOT).as_posix()
    manifest[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    if path.suffix == '.xlsx' and not any(x in path.name for x in ['Notas', 'CRONOGRAMA']):
        values = openpyxl.load_workbook(path, data_only=True)
        formulas = openpyxl.load_workbook(path, data_only=False)
        result = {'source': relative, 'sha256': manifest[relative], 'sheets': {}}
        lines = []
        for sheet in values:
            cells = {}
            lines.append('\nSHEET ' + sheet.title)
            for row in sheet:
                parts = []
                for cell in row:
                    formula = formulas[sheet.title][cell.coordinate].value
                    if cell.value is not None or formula is not None:
                        cells[cell.coordinate] = {'value': cell.value, 'formula': formula if isinstance(formula, str) and formula.startswith('=') else None}
                        parts.append(f'{cell.coordinate}: {cell.value}' + (f' [{formula}]' if cells[cell.coordinate]['formula'] else ''))
                if parts:
                    lines.append(' | '.join(parts))
            result['sheets'][sheet.title] = cells
        (OUT / (path.stem + '.json')).write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
        (OUT / (path.stem + '.txt')).write_text('\n'.join(lines), encoding='utf-8')
    elif path.suffix == '.docx':
        with zipfile.ZipFile(path) as z:
            root = ET.fromstring(z.read('word/document.xml'))
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            lines = [''.join(p.itertext()) for p in []]
            lines = [''.join(t.text or '' for t in p.findall('.//w:t', ns)) for p in root.findall('.//w:p', ns)]
            (OUT / (path.stem + '.txt')).write_text('\n'.join(lines), encoding='utf-8')
(OUT / 'source_hashes.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Extracted evidence; hashed {len(manifest)} originals.')
