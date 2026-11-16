# EE101A homework project — structure, conventions, and import guide

This document describes how the EE101A homework project is built and how to add or import homework
assignments into it. It is written for an LLM assistant (or a new collaborator) doing an import.

**Always verify against the workspace.** This document was last reconciled with the project on
2026-11-16. If the files disagree with this document, the files win — then update this document.

---

## 0. Where the project lives and how changes flow

- The **live project is a shared Overleaf project**. Instructors and TAs edit and compile there.
- A **local git repository** mirrors the Overleaf project and is where scripted work (imports, bulk
  fixes, checks) is done. Work happens on a branch, is reviewed as a diff, and is then copied into
  Overleaf by hand (upload the changed/new files, delete/rename the moved ones).
- Because changes are transferred manually, **keep every change set small and explicit**:
  - At the end of an import, list every file that was **added**, **modified**, **renamed/moved**, or
    **deleted**, so the user can mirror exactly those changes in Overleaf.
  - Avoid renaming or moving existing files unless asked — each rename is an extra manual step in
    Overleaf, and an incomplete mirror leaves broken paths.
  - Before starting, ask the user whether the local repo is up to date with Overleaf (edits made in
    Overleaf since the last sync must be brought into git first, or they will be overwritten).
- Line endings: `.gitattributes` forces LF. Keep it that way; Overleaf uses LF.
- **Local compile** (git copy only): `build.ps1` compiles the assignment selected in
  `config/current_assignment.tex` with Tectonic (XeTeX engine, automatic reruns) to `out.pdf` in
  the repo root. One-time setup: `powershell -ExecutionPolicy Bypass -File build.ps1 -Install`.
  Then `powershell -ExecutionPolicy Bypass -File build.ps1 [-Mode student|solutions]`
  (default: solutions), or Ctrl+Shift+B in VS Code. `build/`, `out.pdf`, and `.tools/` are
  git-ignored. Overleaf remains the reference build; Tectonic's package snapshot can differ slightly.

---

## 1. Build chain

```
main_student.tex / main_solutions.tex
 ├─ config/student_mode.tex | config/solutions_mode.tex   → defines \ifsolutions
 ├─ config/shared.tex
 │    ├─ \newif\ifextracreditassignment (default false)
 │    ├─ config/course.tex                 → \CourseCode, \CourseTitle, \Instructor
 │    ├─ config/current_assignment.tex     → \Semester, \AssignmentFolder
 │    └─ assignments/\Semester/\AssignmentFolder/metadata.tex
 ├─ style/shared.sty                       → \dd, \pluralize
 ├─ style/homework.sty                     → environments, point bookkeeping, header
 └─ \MakeHomeworkHeader
    \input{assignments/\Semester/\AssignmentFolder/questions.tex}
```

Key facts:
- **Engine: XeLaTeX or LuaLaTeX** (required by `fontspec`/`unicode-math`). pdfLaTeX will fail.
  The main font is `Times New Roman` via `\setmainfont`.
- **Two compile passes are needed.** Point totals, per-question totals, and the "Question n/N"
  header are written to the `.aux` file at the end of the run and read back on the next run.
  Overleaf's latexmk handles this automatically. A first-pass PDF may show 0 points.
- Student vs. solutions differ only in `\ifsolutions`. In student mode the `answer` environment is
  removed entirely via the `comment` package (`\excludecomment{answer}`).
- `config/current_assignment.tex` selects which homework is compiled, e.g.:
  ```tex
  \def\Semester{Fall 2026}
  \def\AssignmentFolder{HW07}
  ```
  **This file is shared state.** Changing it changes what every collaborator compiles in Overleaf.
  Do not change it as part of an import unless the user asks; tell the user what to set it to in order
  to compile the new homework.
- `\Instructor` is defined in `config/course.tex` but is **not currently printed** anywhere.

---

## 2. Directory layout

```
assignments/
  <Semester>/                 e.g. "Summer 2025", "Summer 2026", "Fall 2026"  (note the space)
    HWxx/                     two-digit, zero-padded: HW00, HW01, ... HW09
      metadata.tex
      questions.tex
questionbank/
  <topic>/                    amplifiers, capacitors_and_inductors, circuit_quantities, diodes,
                              networks, simple_circuits, training, transistors
    <question_name>/          snake_case, descriptive (e.g. led_iv_curve)
      v0/                     original version
        source.tex
        <figures: .png/.jpg/.jpeg, .drawio sources, .m scripts>
      v1/ ...                 later variants
      version_history.md      optional, recommended when vN > 0 exists
config/  style/  main_student.tex  main_solutions.tex
import/                       this document, conversion notes, and scratch output of the last import
```

Note: `questionbank/training/` has no `<question_name>` level (`training/v0/source.tex`); it is an
exception, do not copy that pattern.

### 2.1 `assignments/<Semester>/HWxx/metadata.tex`

One file holds everything assignment-specific:
```tex
\newcommand{\HomeworkNumber}{7}
\newcommand{\DueDate}{November 15, 2026}
```
For an all-extra-credit homework (prints "EXTRA CREDIT ASSIGNMENT" in the header), add:
```tex
\extracreditassignmenttrue
```
Order of the lines does not matter. `\HomeworkNumber` must match the folder number (HW07 → 7);
`\DueDate`'s year must match the semester. Both have been wrong before — double-check.

The header prints "Due 11:59PM \DueDate", so `\DueDate` is just the date.

### 2.2 `assignments/<Semester>/HWxx/questions.tex` — the manifest

Exact pattern used by every existing assignment:
```tex
% Problem 1 - LED I-V Curve Load-Line Analysis (10 points)
\Point{ledloadline}{basicloadline}{3}
\Point{ledloadline}{ledbrightness}{2}
\Point{ledloadline}{resistorselection}{5}
\Point{ledloadline}{ambienthot}{5}
\MarkExtraCredit{ledloadline}{ambienthot}
\input{questionbank/diodes/led_iv_curve/v1/source}

% Problem 2 - Zener Diode Voltage Regulator (12 points)
\clearpage
\Point{zenerregulator}{inadequatedesign}{5}
...
\input{questionbank/diodes/zener_regulator/v1/source}
```
Rules:
- Comment line `% Problem N - <Title> (<X> points)` before each problem. X excludes extra credit.
- `\clearpage` before every problem except the first.
- One `\Point{questionkey}{partkey}{points}` for **every** `partquestion` in the included source. A
  part with no `\Point` silently gets 0 points; a `\Point` with a typo'd key is silently ignored.
- `\MarkExtraCredit{questionkey}{partkey}` after the `\Point` for extra-credit parts. Extra-credit
  points are excluded from the problem/assignment totals and reported separately in the header.
- `\input{questionbank/<topic>/<question_name>/vN/source}` — no `.tex` extension, path from the
  project root.
- A manifest may pin any version (v0, v1, ...). Past semesters keep pointing at the version they used.

### 2.3 `questionbank/.../vN/source.tex` — question content

```tex
\begin{mainquestion}{questionkey}{Question Title}

Shared problem statement, givens, figures...

\begin{center}
\includegraphics[width=4in]{questionbank/<topic>/<question_name>/vN/figure.png}
\end{center}

% =========================================================
\begin{partquestion}{partkey}
{Prompt text for this part.}

\begin{answer}
Solution text.
\end{answer}
\end{partquestion}

% =========================================================
\begin{partquestion}{otherpart}
{Prompt that refers back to part (\cref{prob:questionkey:partkey}).}

\begin{answer}
...
\end{answer}
\end{partquestion}

\end{mainquestion}
```
- The prompt is the **second mandatory argument** of `partquestion` (in braces, may be on the next
  line). The part letter and "(n points)" are generated automatically — never type them.
- Every part gets the label `prob:<questionkey>:<partkey>`; refer to other parts with
  `part (\cref{prob:<questionkey>:<partkey>})`, which prints the part letter.
- Every part should have an `answer` environment, even if empty (see `training/v0/source.tex`).
- Do not put `\documentclass`, `\usepackage`, `\begin{document}`, `\section*{Problem 4}`, or point
  values in a source file.
- Figure captions inside answers use `\captionof*{figure}{...}` within a `center` environment.
  If you use a `figure` float, give it a meaningful label like `fig:<questionkey>:<name>`.

### 2.4 Environments and macros available (from `style/`)

| Name | Purpose |
|---|---|
| `mainquestion{key}{title}` | One problem. Prints "Question n - title (X points)". |
| `partquestion{partkey}{prompt}` | One graded part, auto-lettered (a), (b), ... |
| `answer` | Solution text; blue in solutions mode, removed in student mode. |
| `kaitlyn` | Green-colored TA commentary (e.g. a boxed "Why we're doing this problem"), used inside `answer` in a few amplifier solutions. Only use it when the source material has equivalent TA commentary. |
| `\Point`, `\MarkExtraCredit` | Manifest-only, see 2.2. |
| `\pluralize{n}{point}{points}` | Number + singular/plural word. |
| `\dd` | Upright differential: `\int f(t)\dd t`. |

Packages already loaded (do not add `\usepackage` in sources): amsmath, amssymb, graphicx, xcolor,
xparse, comment, fancyhdr, fontspec, unicode-math, datetime2, siunitx, hyperref, cleveref, pgfkeys,
listings (Python style preset), verbatim, caption. Notably **not** loaded: circuitikz, tikz,
booktabs, enumitem. If a source needs one of these, ask the user before adding it to
`style/homework.sty` (it affects every homework).

---

## 3. Naming conventions

The existing bank is not fully consistent; follow the **preferred** convention for new content and
do not rename existing content.

- **Question folder** (`<question_name>`): descriptive snake_case naming the physics/skill —
  `led_iv_curve`, `zener_regulator`, `cs_amplifier_design`. Avoid numbered names (`circuit_001`,
  `dependentsource01`) and combined folders (`circuit_graph_and_circuit_001`).
- **Question key** (`mainquestion` first arg): short, lowercase, no separators, usually the folder
  name compressed — `ledloadline`, `zenerregulator`, `cstransfer`. (Some older keys use
  snake_case, e.g. `diode_hogging`; don't copy that.)
- **Part keys**: short lowercase descriptions of the part — `basicloadline`, `maxresistor`. Unique
  within the question.
- **Keys must be unique across the whole question bank**, except that v0/v1/... of the *same*
  question share a key. Points (`pt@key@part`) and labels (`prob:key:part`) are global; two
  different questions with the same key in one homework would merge their points and clash labels,
  with no error. Known existing exception: `superposition` is used by both `networks/superposition`
  and `networks/current_gain/v0` — never put both in one homework. Before choosing a key, grep:
  ```
  grep -rn "begin{mainquestion}{<key>}" questionbank
  ```
- **Figure files**: descriptive lowercase names (`iv_curve.png`, `schematic.png`,
  `sine_swing_limits.png`). Never leave camera/screenshot names (`IMG_1234.jpeg`,
  `Screenshot ... AM.png`) — macOS screenshot names contain a non-breaking space that breaks paths.
  No spaces in any new file or folder name.
- Keep a `.drawio` source next to any figure drawn in draw.io (`figures.drawio`, or `figure.drawio`).

---

## 4. Versioning

- `v0` is the original. Create `v1`, `v2`, ... when the **problem content changes** (new values,
  new parts, different circuit) — especially if any past assignment manifest points at the current
  version. Past semesters must keep compiling to what students actually received.
- Small corrections that don't change what students were asked (typos, a broken font command, a
  wrong path) may be fixed in place.
- A new version may reference unchanged figures from an earlier version folder
  (e.g. `.../cs_transfer_characteristic/v1/source.tex` uses `.../v0/Picture1.png`). This is
  accepted practice, but it means **older version folders must never be deleted**. Prefer copying a
  figure into the new folder if you're also modifying it.
- When creating vN > 0, add or update `<question_name>/version_history.md`:
  ```markdown
  # <Question Title>

  ## Version History

  ### v0 - Initial version
  - Author: <name>
  - Date: <YYYY-MM-DD or semester>
  - Content: <short description; parts and points>

  ### v1 - <short label>
  - Author: <name>
  - Date: <YYYY-MM-DD>
  - Content: <what changed and why>
  ```

---

## 5. LaTeX style conventions

- Units: prefer `siunitx` — `\qty{5}{\kilo\ohm}`, `\qty{0.4}{\milli\ampere\per\celsius}`,
  `\frac{5}{3}\unit{\volt}`. Older sources mix in `\text{ V}`, `1~k$\Omega$`, etc.; converting
  existing content is not required, but new/imported content should use `siunitx`.
- Text-mode emphasis: `\textit{...}`, `\textbf{...}`, `\emph{...}`. Never `\it{...}` / `\bf{...}`
  in text — they are switches, and the braces don't limit them.
- Display math: `\[ ... \]` or `align*`; never `$$ ... $$`.
- Local `\def`/`\renewcommand` for convenience is acceptable only inside a group (e.g. inside an
  `answer` or `{...}`) so it doesn't leak into later questions.
- Graphics paths always from the project root: `questionbank/<topic>/<question_name>/vN/<file>`.
  Never relative to the source file, never absolute, never files in the project root.
- Use `itemize`, `enumerate`, `center`, `tabular`, `\href{url}{text}`, `\url{...}` as normal.
- Separate parts with a `% =====...` comment line for readability.

---

## 6. Importing from a Word document (.docx)

Conversion (see `import/how_to_convert.md`):
1. In Word, convert all equations to Office Math format (so they become machine-readable).
2. `pandoc --extract-media=. input.docx -o output.md`
3. The resulting `output.md` plus `media/` folder are the input to the LLM import step.
   Equations that still did not convert appear as `.wmf` images.

`import/output.md` and `import/media/` in the repo are scratch output from a previous import
(Summer 2025 HW04). Ask the user before overwriting or deleting them; ideally put each new
conversion in its own subfolder, e.g. `import/<semester>_<HWxx>/`.

Import rules:
- **Do not change the wording of problems or solutions.** Import only; do not revise, correct, or
  "improve" content. If something looks wrong (inconsistent numbers, garbled OCR), keep it and add
  a `% NOTE: ...` comment next to it for the user to review (see `networks/bridge_rc_filter/v0`).
- pandoc tends to bold everything in problem statements (`\mathbf{R}_{\mathbf{w}}`, `**...**`).
  Earlier imports sometimes kept this (e.g. `amplifiers/cascade_cd_cg/v0`). Ask the user at the
  start of an import whether to strip conversion-artifact bolding (keeping intentional emphasis and
  bold phasors/vectors) or preserve it verbatim.
- Strip point annotations like "(12 points)" or "(24 points total)" from the text — they go in the
  manifest as `\Point`s. Check that the manifest's sum matches the document's stated total.
- Split a multi-problem document into one `questionbank/<topic>/<question_name>/v0/` per problem.
- Copy usable raster figures (PNG/JPEG) into that problem's `v0/` folder with descriptive names.
- **Never `\includegraphics` a `.wmf` file** — it breaks compilation. Instead leave a visible
  placeholder plus a comment, e.g.
  ```tex
  % TODO(import): equation/figure from media/image3.wmf could not be converted.
  \textbf{[MISSING EQUATION/FIGURE — see image3.wmf in the original document]}
  ```
  If the `.wmf` was an equation and the surrounding text makes the equation unambiguous, ask the
  user whether to transcribe it by hand.
- If the source document has problems that already exist in the question bank (same or very
  similar problem), **stop and ask** whether to reuse the existing version, create a new version of
  the existing question, or create a separate question.

## 7. Importing from another LaTeX project

- Do not copy the other project's preamble, packages, or custom environments. Translate its problem
  structure into `mainquestion`/`partquestion`/`answer`. If it relies on packages not loaded here
  (circuitikz, tikz, enumitem, booktabs, ...), list them and ask the user before adding anything to
  `style/`.
- Map its solution mechanism (`\ifsolution`, `solution` env, `exam` class `solution`, etc.) to
  `answer`.
- Convert its image paths to project-root paths in the new `vN/` folders.
- Check every new question key against the whole question bank for collisions (section 3).

---

## 8. Step-by-step: adding a new homework

Before creating any files, **ask for anything missing** and then **summarize the plan**:
- Semester (e.g. `Winter 2026`) and homework number (e.g. `HW03`).
- Due date.
- Where the source material is (docx/markdown + media, or LaTeX files).
- For each problem: target topic folder, question folder name, question key, part keys, points per
  part, extra credit parts, and whether it reuses/extends an existing question.
- The intended total points (and extra credit total).

Then:
1. Create `assignments/<Semester>/HWxx/metadata.tex` (`\HomeworkNumber`, `\DueDate`, optional
   `\extracreditassignmenttrue`).
2. Create or reuse question sources under `questionbank/` (section 2.3), with figures in the same
   `vN/` folder.
3. Create `assignments/<Semester>/HWxx/questions.tex` (section 2.2).
4. Run the checks in section 9.
5. Do **not** edit `config/current_assignment.tex`; tell the user the two values to set to compile.
6. Commit on a branch and report the full list of added / modified / moved files for mirroring into
   Overleaf (section 0).

---

## 9. Checks before handing back

There is no LaTeX engine guaranteed in the local environment, so do these static checks (and ask
the user to compile both `main_student.tex` and `main_solutions.tex` in Overleaf):
- Every `\input{...}` in the manifest resolves to an existing `.tex` file.
- Every non-commented `\includegraphics{...}` path exists (exact case — Overleaf is case-sensitive).
- For each manifest: the set of `(questionkey, partkey)` pairs in `\Point` equals the set of
  `partquestion` keys in the included sources; no `mainquestion` key appears twice in one homework.
- The new question keys are not used by any *other* question in the bank.
- `\Point` sum per problem matches the `% Problem N - ... (X points)` comment and the source
  document's stated totals.
- No `.wmf` is included; no `\documentclass`/`\usepackage` in sources; no files added at the
  project root; no spaces in new file/folder names.
- `metadata.tex`: `\HomeworkNumber` matches the folder; `\DueDate` year matches the semester.

---

## 10. Known quirks / legacy items (don't imitate, don't "fix" unless asked)

- Some sources reuse figures from an earlier version folder (by design, see section 4).
- Unused standalone documents remain in the bank as historical originals:
  `training/v0/HW0_overleaf.tex`, `networks/thevenin_meas/v0/problem4_with_solution.tex`,
  `networks/function_generator_and_scope/v0/source_problem4.tex`. They have their own
  `\documentclass` and must never be `\input`.
- Some unused question sources exist (e.g. `networks/double_dependent/v0`,
  `networks/current_gain/v0`). Unused ≠ obsolete; leave them.
- Unit formatting and key naming are mixed in older content (sections 3 and 5).
- `\Instructor` is defined but not printed.
