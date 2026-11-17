#!/usr/bin/env python3
"""Build every homework (or a subset) and report / compare results.

Each homework is built from its root files (assignments/<Semester>/<HWxx>/<Semester>_<HWxx>_<mode>.tex),
in a temporary copy of the project. Uses Tectonic from .tools/tectonic/ or PATH.

Examples
    python tools/build_all.py                          # all homeworks, both modes
    python tools/build_all.py --mode solutions --only "Fall 2026/HW07"
    python tools/build_all.py --save baseline.json     # record results
    python tools/build_all.py --compare baseline.json  # rebuild and diff against a recording
    python tools/build_all.py --pdf-dir pdfs           # also keep every PDF

Unless --only is given, main_questionbank_solutions.tex (every version of every question) is built too.

Recorded per build: success, page count, the totals written to the .aux file, the set of image
files loaded (normalized paths), and LaTeX warnings.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IGNORE = shutil.ignore_patterns('.git', '.tools', 'build', 'out.pdf', '__pycache__')


def find_tectonic():
    local = ROOT / '.tools' / 'tectonic' / ('tectonic.exe' if os.name == 'nt' else 'tectonic')
    if local.exists():
        return str(local)
    found = shutil.which('tectonic')
    if not found:
        sys.exit('Tectonic not found: run "build.ps1 -Install" or put tectonic on PATH.')
    return found


def assignments(repo, only):
    for sem in sorted(p for p in (repo / 'assignments').iterdir() if p.is_dir()):
        for hw in sorted(p for p in sem.iterdir() if p.is_dir()):
            name = f'{sem.name}/{hw.name}'
            if not only or name in only:
                yield sem.name, hw.name


def unwrap_log(log_text, width=79):
    """TeX hard-wraps log lines at 79 characters; join them back together."""
    out, buf = [], ''
    for line in log_text.splitlines():
        buf += line
        if len(line) != width:
            out.append(buf)
            buf = ''
    if buf:
        out.append(buf)
    return '\n'.join(out)


def parse_results(log_text, aux_text):
    log_text = unwrap_log(log_text)
    pages = re.search(r'Output written on .*?\((\d+) pages?', log_text)
    totals = dict(re.findall(r'\\gdef\s*\\(\w+)\s*\{([^}]*)\}', aux_text))
    graphics = sorted({os.path.normpath(g).replace('\\', '/')
                       for g in re.findall(r'^File: (.+?) Graphic file', log_text, re.M)})
    warnings = []
    for m in re.finditer(r'^((?:LaTeX|Package \w+) Warning:.*(?:\n(?!\n).*)*)', log_text, re.M):
        w = ' '.join(m.group(1).split())
        if 'Rerun' not in w and 'PageLabels' not in w:
            warnings.append(w)
    return int(pages.group(1)) if pages else None, totals, graphics, warnings


def root_file(sem, hw, mode):
    """Path (relative to the project root) of the root file to compile."""
    if mode == 'questionbank':
        return 'main_questionbank_solutions.tex'
    return f'assignments/{sem}/{hw}/{sem.replace(" ", "")}_{hw}_{mode}.tex'


def compile_root(tectonic, work, root, outdir):
    """Compile one root file from the project root. -Z search-path=. makes \\input and
    \\includegraphics resolve from the project root, as Overleaf does, even for root files in
    subfolders."""
    return subprocess.run([tectonic, root, '--outdir', str(outdir), '--keep-logs', '--keep-intermediates',
                           '-Z', 'search-path=.'],
                          cwd=work, capture_output=True, text=True, encoding='utf-8', errors='replace')


def build(tectonic, work, sem, hw, mode, pdf_dir):
    out = work / '_out'
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir()
    root = root_file(sem, hw, mode)
    stem = Path(root).stem
    proc = compile_root(tectonic, work, root, out)
    log = (out / f'{stem}.log')
    aux = (out / f'{stem}.aux')
    log_text = log.read_text(encoding='utf-8', errors='replace') if log.exists() else ''
    aux_text = aux.read_text(encoding='utf-8', errors='replace') if aux.exists() else ''
    ok = proc.returncode == 0 and (out / f'{stem}.pdf').exists()
    pages, totals, graphics, warnings = parse_results(log_text, aux_text)
    errors = [] if ok else [l for l in (proc.stdout + proc.stderr).splitlines()
                            if l.startswith('error') or l.startswith('!')][:5] + \
        re.findall(r'^!.*$', log_text, re.M)[:3]
    if ok and pdf_dir:
        pdf_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(out / f'{stem}.pdf', pdf_dir / f'{stem}.pdf')
    return {'ok': ok, 'pages': pages, 'totals': totals, 'graphics': graphics,
            'warnings': warnings, 'errors': errors}


def compare(old, new):
    diffs = []
    for key in sorted(set(old) | set(new)):
        a, b = old.get(key), new.get(key)
        if a is None or b is None:
            diffs.append(f'{key}: only in {"new" if a is None else "baseline"}')
            continue
        for field in ('ok', 'pages', 'totals', 'warnings'):
            if a[field] != b[field]:
                diffs.append(f'{key}: {field} {a[field]!r} -> {b[field]!r}')
        if a['graphics'] != b['graphics']:
            gone = sorted(set(a['graphics']) - set(b['graphics']))
            added = sorted(set(b['graphics']) - set(a['graphics']))
            diffs.append(f'{key}: graphics removed {gone} added {added}')
    return diffs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--mode', choices=['both', 'solutions', 'student'], default='both')
    ap.add_argument('--only', nargs='*', help='e.g. "Fall 2026/HW07"')
    ap.add_argument('--save', type=Path, help='write results JSON here')
    ap.add_argument('--compare', type=Path, help='baseline JSON to diff against')
    ap.add_argument('--pdf-dir', type=Path, help='copy every PDF here')
    ap.add_argument('--no-questionbank', action='store_true',
                    help='skip the question bank catalog (built by default unless --only is given)')
    args = ap.parse_args()

    tectonic = find_tectonic()
    modes = ['solutions', 'student'] if args.mode == 'both' else [args.mode]
    results = {}
    with tempfile.TemporaryDirectory(prefix='hwbuild_') as tmp:
        work = Path(tmp) / 'repo'
        shutil.copytree(ROOT, work, ignore=IGNORE)
        for sem, hw in assignments(work, args.only):
            for mode in modes:
                key = f'{sem}/{hw} [{mode}]'
                r = build(tectonic, work, sem, hw, mode, args.pdf_dir)
                results[key] = r
                status = 'OK  ' if r['ok'] else 'FAIL'
                print(f'{status} {key:<32} pages={r["pages"]} total={r["totals"].get("AssignmentTotal", "-")}'
                      f' warnings={len(r["warnings"])}', flush=True)
                for line in r['errors'] + r['warnings']:
                    print(f'       {line}')
        if not args.only and not args.no_questionbank:
            # The question bank catalog compiles every version of every question, used or not.
            key = 'Question bank [questionbank]'
            r = build(tectonic, work, '', '', 'questionbank', args.pdf_dir)
            results[key] = r
            print(f'{"OK  " if r["ok"] else "FAIL"} {key:<32} pages={r["pages"]} warnings={len(r["warnings"])}', flush=True)
            for line in r['errors'] + r['warnings']:
                print(f'       {line}')

    failed = [k for k, r in results.items() if not r['ok']]
    print(f'\n{len(results) - len(failed)}/{len(results)} builds succeeded.')
    if args.save:
        args.save.write_text(json.dumps(results, indent=1), encoding='utf-8')
        print(f'Saved results to {args.save}')
    if args.compare:
        diffs = compare(json.loads(args.compare.read_text(encoding='utf-8')), results)
        print(f'\nComparison with {args.compare}: {"no differences" if not diffs else f"{len(diffs)} difference(s)"}')
        for d in diffs:
            print('  ' + d)
        if diffs:
            return 1
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
