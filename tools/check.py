#!/usr/bin/env python3
"""Static checks for the homework project (no LaTeX needed).

    python tools/check.py               # report errors and warnings (exit 1 on errors)
    python tools/check.py --strict      # treat warnings as errors too
    python tools/check.py --fix-index   # regenerate questionbank/index.tex from the folder tree
    python tools/check.py --catalog     # (re)write questionbank/README.md, the question catalog

What is checked
  index      every \\RegisterQuestion id = its folder name, folder exists, every question folder
             is registered, no duplicates
  manifests  every \\UseQuestion id/version exists; its points list names exactly the parts of the
             source; values are whole numbers (optionally "extra"); no question or question key
             used twice in one homework; "% Problem N - ... (X points)" comments match the sum;
             no leftover \\Point / \\MarkExtraCredit / \\input
  sources    one mainquestion, unique part keys, no preamble commands, figures exist (exact case,
             as on Overleaf), no root-relative "questionbank/..." paths, no .wmf, every \\cref to
             prob:<key>:<part> resolves, no text-mode \\it{..}/\\bf{..}, no $$
  bank       question keys unique across different questions; no spaces in file names
  metadata   course.tex per semester; \\HomeworkNumber matches HWxx; \\DueDate year matches semester
"""
import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QB = ROOT / 'questionbank'
ASSIGN = ROOT / 'assignments'
INDEX = QB / 'index.tex'
CATALOG = QB / 'README.md'
VERSION_RE = re.compile(r'v\d+')

errors, warnings = [], []


def rel(p):
    return Path(p).relative_to(ROOT).as_posix()


def err(where, msg):
    errors.append(f'{where}: {msg}')


def warn(where, msg):
    warnings.append(f'{where}: {msg}')


def read(p):
    return Path(p).read_text(encoding='utf-8', errors='replace')


def strip_comments(text):
    """Remove TeX comments (unescaped % to end of line), keeping line structure."""
    return '\n'.join(re.sub(r'(?<!\\)%.*', '', line) for line in text.split('\n'))


def braced(text, start):
    """text[start] must be '{'. Return (content, index after closing brace)."""
    assert text[start] == '{'
    depth = 0
    for i in range(start, len(text)):
        c = text[i]
        if c == '\\':
            continue
        if c == '{' and (i == 0 or text[i - 1] != '\\'):
            depth += 1
        elif c == '}' and text[i - 1] != '\\':
            depth -= 1
            if depth == 0:
                return text[start + 1:i], i + 1
    raise ValueError('unbalanced braces')


def exists_exact_case(path):
    """Path.exists() that is case-sensitive even on Windows (Overleaf is case-sensitive)."""
    path = Path(path)
    if not path.exists():
        return False
    cur = path.resolve()
    parts = []
    while cur != cur.parent:
        parts.append(cur)
        cur = cur.parent
    for p in parts:
        if p.parent.exists() and p.name not in {c.name for c in p.parent.iterdir()}:
            return False
    return True


# ---------------------------------------------------------------- question bank model

def question_dirs():
    """Folders that contain at least one vN/source.tex."""
    out = []
    for d in sorted(QB.rglob('*')):
        if d.is_dir() and 'originals' not in d.parts and any(
                VERSION_RE.fullmatch(c.name) and (c / 'source.tex').exists() for c in d.iterdir() if c.is_dir()):
            out.append(d)
    return out


def parse_source(src):
    text = read(src)
    code = strip_comments(text)
    info = {'key': None, 'title': None, 'parts': [], 'refs': [], 'graphics': [], 'inputs': []}
    mains = list(re.finditer(r'\\begin\{mainquestion\}\s*', code))
    where = rel(src)
    if len(mains) != 1:
        err(where, f'expected exactly one \\begin{{mainquestion}}, found {len(mains)}')
    if mains:
        i = mains[0].end()
        try:
            info['key'], i = braced(code, i)
            j = code.index('{', i)
            info['title'], _ = braced(code, j)
            info['title'] = ' '.join(info['title'].split())
        except (ValueError, AssertionError):
            err(where, 'could not parse \\begin{mainquestion}{key}{title}')
    info['parts'] = re.findall(r'\\begin\{partquestion\}\s*\{([^}]*)\}', code)
    for k in {p for p in info['parts'] if info['parts'].count(p) > 1}:
        err(where, f'part key "{k}" used more than once')
    info['refs'] = re.findall(r'\\[cC]ref\{(prob:[^}]*)\}', code)
    info['graphics'] = [g.strip() for g in re.findall(r'\\includegraphics\s*(?:\[[^\]]*\])?\s*\{([^}]*)\}', code)]
    info['inputs'] = [g.strip() for g in re.findall(r'\\(?:verbatiminput|lstinputlisting(?:\[[^\]]*\])?|input)\s*\{([^}]*)\}', code)]
    for cmd in ('documentclass', 'usepackage', 'begin{document}'):
        if '\\' + cmd in code:
            err(where, f'\\{cmd} is not allowed in a question source')
    if re.search(r'(?<![A-Za-z\\])\\(it|bf|rm|tt|sc|sf)\s*\{', code) and not re.search(r'\$[^$]*\\(it|bf)\{', code):
        warn(where, 'text-mode \\it{...}/\\bf{...} found; use \\textit{...}/\\textbf{...}')
    if '$$' in code:
        warn(where, 'use \\[ ... \\] instead of $$ ... $$')
    for path in info['graphics'] + info['inputs']:
        if path.startswith('questionbank/'):
            err(where, f'root-relative path "{path}"; paths are relative to the version folder now')
            continue
        if path.lower().endswith('.wmf'):
            err(where, f'"{path}": .wmf images cannot be compiled; convert to PNG')
            continue
        target = src.parent / path
        candidates = [target] if target.suffix else [target.with_suffix(s) for s in ('.png', '.pdf', '.jpg', '.jpeg', '.tex')]
        if not any(exists_exact_case(c) for c in candidates):
            err(where, f'file "{path}" not found (paths are case-sensitive on Overleaf)')
        elif path.startswith('../../'):
            warn(where, f'"{path}" reaches into another question; copy the file into this question instead')
    return info


def check_index_and_bank():
    qdirs = question_dirs()
    by_id = {}
    for d in qdirs:
        if d.name in by_id:
            err(rel(d), f'question folder name "{d.name}" is also used by {rel(by_id[d.name])}; ids must be unique')
        by_id[d.name] = d
    registered = {}
    if not INDEX.exists():
        err('questionbank/index.tex', 'missing (run tools/check.py --fix-index)')
    else:
        for n, line in enumerate(read(INDEX).splitlines(), 1):
            line = re.sub(r'(?<!\\)%.*', '', line)
            for qid, path in re.findall(r'\\RegisterQuestion\{([^}]*)\}\{([^}]*)\}', line):
                where = f'questionbank/index.tex:{n}'
                if qid in registered:
                    err(where, f'id "{qid}" registered twice')
                registered[qid] = path
                d = QB / path
                if not d.is_dir():
                    err(where, f'"{path}" does not exist (folder moved? run --fix-index)')
                elif d.name != qid:
                    err(where, f'id "{qid}" does not match folder name "{d.name}"')
        for qid, d in by_id.items():
            if qid not in registered:
                err(rel(d), f'question folder not registered in questionbank/index.tex (run --fix-index)')

    sources = {}  # (qid, version) -> info
    for qid, d in by_id.items():
        for v in sorted(c for c in d.iterdir() if c.is_dir() and VERSION_RE.fullmatch(c.name)):
            src = v / 'source.tex'
            if not src.exists():
                warn(rel(v), 'version folder without source.tex')
                continue
            sources[(qid, v.name)] = parse_source(src)
            for extra in v.glob('*.tex'):
                if extra.name != 'source.tex':
                    warn(rel(extra), 'extra .tex file in a version folder (move standalone originals to <question>/originals/)')
    # bank-wide key uniqueness and \cref resolution
    key_owners = defaultdict(set)
    labels = set()
    for (qid, v), info in sources.items():
        if info['key']:
            key_owners[info['key']].add(qid)
            labels.update(f'prob:{info["key"]}:{p}' for p in info['parts'])
    for key, owners in key_owners.items():
        if len(owners) > 1:
            warn('questionbank', f'question key "{key}" is used by different questions {sorted(owners)}; '
                                 'they can never be in the same homework')
    for (qid, v), info in sources.items():
        for r in info['refs']:
            if r not in labels:
                err(f'{rel(by_id[qid])}/{v}/source.tex', f'\\cref{{{r}}} does not match any part')
            elif info['key'] and not r.startswith(f'prob:{info["key"]}:'):
                warn(f'{rel(by_id[qid])}/{v}/source.tex', f'\\cref{{{r}}} points into another question')
    for p in QB.rglob('*'):
        if ' ' in p.name:
            warn(rel(p), 'space in file/folder name')
    return registered, by_id, sources


def check_assignments(registered, sources):
    usage = defaultdict(list)  # (qid, v) -> ["Fall 2026 HW07", ...]
    for sem in sorted(p for p in ASSIGN.iterdir() if p.is_dir()):
        course = sem / 'course.tex'
        if not course.exists():
            err(rel(sem), 'missing course.tex')
        else:
            c = read(course)
            for macro in ('CourseCode', 'CourseTitle', 'Instructor'):
                if f'\\newcommand{{\\{macro}}}' not in c:
                    err(rel(course), f'does not define \\{macro}')
        sem_year = re.search(r'(\d{4})', sem.name)
        for hw in sorted(p for p in sem.iterdir() if p.is_dir()):
            meta, man = hw / 'metadata.tex', hw / 'questions.tex'
            label = f'{sem.name} {hw.name}'
            if not meta.exists() or not man.exists():
                err(rel(hw), 'needs metadata.tex and questions.tex')
                continue
            m = strip_comments(read(meta))
            num = re.search(r'\\HomeworkNumber\}\{(\d+)\}', m)
            hw_num = re.search(r'(\d+)', hw.name)
            if not num:
                err(rel(meta), 'no \\HomeworkNumber')
            elif hw_num and int(num.group(1)) != int(hw_num.group(1)):
                err(rel(meta), f'\\HomeworkNumber is {num.group(1)} but the folder is {hw.name}')
            due = re.search(r'\\DueDate\}\{([^}]*)\}', m)
            if not due:
                err(rel(meta), 'no \\DueDate')
            elif sem_year and sem_year.group(1) not in due.group(1):
                err(rel(meta), f'\\DueDate "{due.group(1)}" is not in {sem_year.group(1)}')
            check_manifest(man, label, registered, sources, usage)
    return usage


def check_manifest(man, label, registered, sources, usage):
    where = rel(man)
    raw = read(man)
    code = strip_comments(raw)
    for bad in ('\\Point', '\\MarkExtraCredit', '\\input'):
        if bad in code:
            err(where, f'{bad} is not used in manifests any more; use \\UseQuestion')
    used_ids, used_keys = set(), {}
    prev_line = 0
    # problem comments, to compare stated totals: "% Problem N - Title (X points)".
    # Positions are compared as line numbers (code has comments stripped, so offsets differ).
    comment_totals = [(raw.count('\n', 0, m.start()), int(m.group(1))) for m in
                      re.finditer(r'^%\s*Problem\s+\d+.*?\((\d+)\s*points?', raw, re.M)]
    for m in re.finditer(r'\\UseQuestion\s*\{([^}]*)\}\s*\{([^}]*)\}\s*(?=\{)', code):
        qid, ver = m.group(1).strip(), m.group(2).strip()
        try:
            body, _ = braced(code, m.end())
        except (ValueError, AssertionError):
            err(where, f'\\UseQuestion{{{qid}}}: unbalanced points list')
            continue
        if qid not in registered:
            err(where, f'unknown question id "{qid}"')
            continue
        if qid in used_ids:
            err(where, f'question "{qid}" used twice')
        used_ids.add(qid)
        info = sources.get((qid, ver))
        if info is None:
            err(where, f'"{qid}" has no version {ver}')
            continue
        usage[(qid, ver)].append(label)
        if info['key'] in used_keys:
            err(where, f'"{qid}" and "{used_keys[info["key"]]}" share the question key "{info["key"]}"')
        used_keys[info['key']] = qid
        points, total = {}, 0
        for item in (s.strip() for s in body.split(',')):
            if not item:
                continue
            if '=' not in item:
                err(where, f'{qid}: "{item}" has no "= points"')
                continue
            k, v = (s.strip() for s in item.split('=', 1))
            pm = re.fullmatch(r'(\d+)\s*(extra)?', v)
            if not pm:
                err(where, f'{qid}: invalid points "{v}" for part "{k}"')
                continue
            if k in points:
                err(where, f'{qid}: part "{k}" listed twice')
            points[k] = v
            if not pm.group(2):
                total += int(pm.group(1))
        for p in info['parts']:
            if p not in points:
                err(where, f'{qid}: part "{p}" has no points (it would count as 0)')
        for p in points:
            if p not in info['parts']:
                err(where, f'{qid}: points given for "{p}", which is not a part of {qid}/{ver}')
        # nearest preceding problem comment, if it is after the previous \UseQuestion
        line = code.count('\n', 0, m.start())
        stated = [t for pos, t in comment_totals if prev_line <= pos < line]
        prev_line = line
        if stated and stated[-1] != total:
            warn(where, f'{qid}: comment says {stated[-1]} points but the parts sum to {total} (excluding extra credit)')


def write_index(by_id):
    lines = ['% Question index: question id (= folder name) -> folder below questionbank/.',
             "% This is the ONLY place a question's location is written. After moving or renaming a",
             '% question folder, update its line here (tools/check.py --fix-index regenerates this file).',
             '']
    topic = None
    for qid, d in sorted(by_id.items(), key=lambda kv: kv[1].relative_to(QB).as_posix()):
        path = d.relative_to(QB).as_posix()
        t = path.split('/')[0]
        if t != topic:
            lines.append(f'% --- {t}')
            topic = t
        lines.append(f'\\RegisterQuestion{{{qid}}}{{{path}}}')
    INDEX.write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
    print(f'Wrote {rel(INDEX)} ({len(by_id)} questions)')


def write_catalog(by_id, sources, usage):
    def sem_key(label):  # "Summer 2025 HW04" -> sortable
        season = {'Winter': 0, 'Spring': 1, 'Summer': 2, 'Fall': 3}
        m = re.match(r'(\w+) (\d{4}) (\S+)', label)
        return (int(m.group(2)), season.get(m.group(1), 9), m.group(3)) if m else (0, 0, label)

    out = ['# Question catalog', '',
           'Generated by `python tools/check.py --catalog` — do not edit by hand.', '',
           'Each question is loaded in a manifest with `\\UseQuestion{<id>}{<version>}{...}`.', '']
    topic = None
    for qid, d in sorted(by_id.items(), key=lambda kv: kv[1].relative_to(QB).as_posix()):
        path = d.relative_to(QB).as_posix()
        t = path.split('/')[0]
        if t != topic:
            out += ['', f'## {t}', '', '| ID | Title | Key | Version | Parts | Used in |', '|---|---|---|---|---|---|']
            topic = t
        versions = sorted((v for (q, v) in sources if q == qid), key=lambda v: int(v[1:]))
        for i, v in enumerate(versions):
            info = sources[(qid, v)]
            used = ', '.join(sorted(usage.get((qid, v), []), key=sem_key)) or '—'
            title = (info['title'] or '').replace('|', '\\|')
            first = (f'[`{qid}`]({path})', title, f'`{info["key"]}`') if i == 0 else ('', title if title != sources[(qid, versions[0])]['title'] else '', '')
            out.append(f'| {first[0]} | {first[1]} | {first[2]} | {v} | {len(info["parts"])} | {used} |')
    CATALOG.write_text('\n'.join(out).lstrip('\n') + '\n', encoding='utf-8', newline='\n')
    print(f'Wrote {rel(CATALOG)}')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--strict', action='store_true', help='treat warnings as errors')
    ap.add_argument('--fix-index', action='store_true', help='regenerate questionbank/index.tex')
    ap.add_argument('--catalog', action='store_true', help='write questionbank/README.md')
    args = ap.parse_args()

    if args.fix_index:
        write_index({d.name: d for d in question_dirs()})
    registered, by_id, sources = check_index_and_bank()
    usage = check_assignments(registered, sources)
    if args.catalog:
        write_catalog(by_id, sources, usage)

    for w in warnings:
        print(f'WARNING  {w}')
    for e in errors:
        print(f'ERROR    {e}')
    print(f'\n{len(errors)} error(s), {len(warnings)} warning(s); '
          f'{len(by_id)} questions, {len(sources)} versions, '
          f'{sum(1 for s in ASSIGN.iterdir() if s.is_dir() for h in s.iterdir() if h.is_dir())} homeworks.')
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == '__main__':
    sys.exit(main())
