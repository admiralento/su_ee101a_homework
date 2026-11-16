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
  Overleaf by hand. Large changes are synced by replacing the `assignments/` and `questionbank/`
  folders in Overleaf wholesale.
- Because changes are transferred manually, **keep every change set explicit**:
  - At the end of an import, list every file that was **added**, **modified**, **renamed/moved**, or
    **deleted**, so the user can mirror exactly those changes in Overleaf.
  - Before starting, ask the user whether the local repo is up to date with Overleaf (edits made in
    Overleaf since the last sync must be brought into git first, or they will be overwritten).
- Line endings: `.gitattributes` forces LF. Keep it that way; Overleaf uses LF.

### Local tools (git copy only)

| Command | What it does |
|---|---|
| `python tools/check.py` | Static checks (section 9). Run before every hand-back. `--fix-index` regenerates `questionbank/index.tex`; `--catalog` rewrites `questionbank/README.md` and `questionbank/catalog.tex` (it warns when either is stale). |
| `python tools/build_all.py` | Compiles every homework in both modes **in a temporary copy** (never touches `config/current_assignment.tex`). `--only "Winter 2026/HW03"`, `--mode solutions`, `--save x.json` / `--compare x.json` for before/after regression checks, `--pdf-dir` to keep PDFs. |
| `powershell -ExecutionPolicy Bypass -File build.ps1 [-Mode student\|solutions\|questionbank]` | Compiles the homework selected in `config/current_assignment.tex` to `out.pdf` (default: solutions), or with `-Mode questionbank` the question bank catalog (section 2.6). Ctrl+Shift+B in VS Code. One-time setup: `build.ps1 -Install`. |

Both builders use Tectonic (XeTeX engine, automatic reruns) from `.tools/tectonic/`. Overleaf is the
reference build; Tectonic's package snapshot is older (2022) and can differ slightly.

---

## 1. Build chain

```
main_student.tex / main_solutions.tex
 ├─ config/student_mode.tex | config/solutions_mode.tex   → defines \ifsolutions
 ├─ config/shared.tex                      (read BEFORE \documentclass)
 │    ├─ \newif\ifextracreditassignment, \newif\ifshowinstructor (both default false)
 │    ├─ \HomeworkStyle{...} (default style-jeff)
 │    ├─ config/current_assignment.tex     → \Semester, \AssignmentFolder
 │    ├─ assignments/\Semester/course.tex  → course code/title/instructor, style, header settings
 │    ├─ assignments/\Semester/\AssignmentFolder/metadata.tex   (may override the style)
 │    └─ \HwFontSize                       → 11pt (style-jeff) or 10pt (style-mark)
 ├─ \documentclass[\HwFontSize]{article}
 ├─ style/shared.sty                       → \dd, \pluralize
 ├─ style/homework.sty                     → environments, \UseQuestion, point bookkeeping, header
 │    └─ questionbank/index.tex            → \RegisterQuestion{id}{folder} for every question
 └─ \MakeHomeworkHeader
    \input{assignments/\Semester/\AssignmentFolder/questions.tex}   → \UseQuestion{...} per problem
```

Key facts:
- **Engine: XeLaTeX or LuaLaTeX** (required by `fontspec`/`unicode-math`). pdfLaTeX will fail.
  The main font is `Times New Roman` in `style-jeff`, Latin Modern in `style-mark`.
- **Two homework styles** (section 2.0): `style-jeff`, the standard layout, and `style-mark`, which
  reproduces Mark Horowitz's Winter 2026 homework (his `exam.cls`). Same sources, same manifests;
  only the rendering differs. Winter 2026 uses `style-mark`; all other semesters `style-jeff`.
- **Two compile passes are needed.** Point totals, per-question totals, and the "Question n/N"
  header are written to the `.aux` file and read back on the next run. Overleaf's latexmk and
  Tectonic both rerun automatically.
- Student vs. solutions differ only in `\ifsolutions`. In the student version of `style-jeff` the
  `answer` environment is removed via the `comment` package (`\excludecomment{answer}`), which
  requires `\begin{answer}[..]` and `\end{answer}` to be **alone on their lines, in column 0**
  (`check.py` enforces this). In `style-mark` answers are replaced by blank writing space.
- `config/current_assignment.tex` selects which homework is compiled, e.g.:
  ```tex
  \def\Semester{Fall 2026}
  \def\AssignmentFolder{HW07}
  ```
  **This file is shared state.** Changing it changes what every collaborator compiles in Overleaf.
  Do not change it as part of an import; tell the user what to set it to. Use
  `tools/build_all.py --only ...` to compile a homework yourself without touching it.

---

## 2. Directory layout

```
assignments/
  <Semester>/                 e.g. "Summer 2025", "Summer 2026", "Fall 2026"  (note the space)
    course.tex                course code, title, instructor, header settings (required)
    HWxx/                     two-digit, zero-padded: HW00, HW01, ... HW09
      metadata.tex
      questions.tex           the manifest
questionbank/
  index.tex                   question id -> folder; the ONLY place a question's location is written
  tags.md                     concept tag vocabulary (human-edited; see section 4)
  README.md                   generated catalog table (tools/check.py --catalog); do not edit by hand
  catalog.tex                 generated content of main_questionbank.tex (same command); do not edit
  NN_<syllabus_topic>/        one folder per syllabus topic, numbered in course order (see below)
    <subtopic>/               the primary concept the problem teaches
      <question_id>/          folder name = question id (snake_case, unique across the bank)
        v0/                   original version
          source.tex
          <figures: .png/.jpg/.jpeg, .drawio sources, .m scripts>
        v1/ ...               later variants
        originals/            optional: standalone original documents (never \input)
        version_history.md    required: authors, dates, notes per version + Concepts tags
config/  style/  tools/  main_student.tex  main_solutions.tex  main_questionbank.tex
import/                       this document and conversion notes; per-import scratch folders
```

Question bank topic folders (each question is filed under the **primary** topic it teaches;
secondary concepts are expressed with concept tags, section 4):

| Syllabus folder | Subtopic folders |
|---|---|
| `00_course_introduction` | (questions directly inside, e.g. `lab_training`) |
| `01_circuit_abstraction` | `charge_current_energy`, `waveforms`, `resistors`, `circuit_topology`, `power_balance` |
| `02_resistive_networks` | `kirchhoff_laws`, `dividers`, `nodal_analysis`, `mesh_analysis`, `dependent_sources` |
| `03_network_theorems` | `superposition`, `source_transformation`, `thevenin_and_norton`, `power_transfer` |
| `04_diode_circuits` | `diode_physics`, `diode_models`, `load_line`, `zener_regulators` |
| `05_energy_storage` | `capacitors`, `transients` |
| `06_mosfets` | `process_parameters`, `iv_characteristics`, `dc_biasing`, `applications` |
| `07_mosfet_amplifier_analysis` | `transfer_characteristic` |
| `08_single_stage_amplifiers` | `amplifier_models`, `common_source`, `common_drain`, `multistage` |
| `09_sinusoidal_analysis` | `phasors`, `impedance_and_resonance`, `filters_and_bode_plots` |

- Put an imported problem in the existing subtopic that matches what it mainly teaches; create a
  new subtopic folder (snake_case, no number) if none fits, and mention it to the user. Number
  prefixes are only on the syllabus folders; they order the catalog and are hidden in it.
- Folder names are shown in the catalog with words capitalized and a few acronyms recognized
  (`dc`, `iv`, `mosfet`, `rc`, `rl`, ...; see `topic_name` in `tools/check.py`).
- Moving a question between folders: `git mv` it, then `python tools/check.py --fix-index` and
  `--catalog`. Nothing else references folder paths.

### 2.0 `assignments/<Semester>/course.tex`

Course-level metadata and header settings for one offering; every semester folder must have one:
```tex
% Course metadata for this semester (shared by every HWxx in this folder)
\newcommand{\CourseCode}{EE101A}
\newcommand{\CourseTitle}{Circuits I}
\newcommand{\Instructor}{Jeff Stribling}

% Homework style (optional; default style-jeff)
\HomeworkStyle{style-jeff}

% Header settings
\newcommand{\DueTime}{11:59PM}  % printed as "Due <DueTime> <DueDate>"
\newcommand{\NameReminder}{Please be sure to write your name on the front page!}  % student version only; leave {} empty to hide
\showinstructorfalse  % \showinstructortrue prints "Instructor: <Instructor>" under the title
```
`\CourseCode` appears in the page header ("EE101A/Fall 2026") and the PDF title. When creating a
new semester folder, copy an existing `course.tex` and ask the user for the instructor, the style,
and whether the header settings should differ.

**Styles.** `\HomeworkStyle{style-jeff}` or `\HomeworkStyle{style-mark}`; a homework's
`metadata.tex` may also set it to override the semester for that homework.

| Element | `style-jeff` | `style-mark` |
|---|---|---|
| Font / size | Times New Roman, 11 pt | Latin Modern, 10 pt |
| Page header | *EE101A/Semester* left, *Question n/N* right; compile date and page in footer | centered *Homework N / \CourseCode / Due \DueTime, \DueDate* |
| Title block | "Homework #N", due, total points, name reminder | none |
| Question heading | **Question n - Title (X points)** | **Question n: Title**, then *[X pts]* where `\questionpoints` is |
| Part | **(a)** prompt **(n points)** | (a) *[n pts]* prompt, as a list item |
| Solutions | blue text | sans-serif text in a framed box |
| Student version | answers removed | answers replaced by `[height]` of blank space (default 1in) |
| `\qnewpage` | ignored | page break in the student version |
| Lists | LaTeX defaults | `(a)` labels at every level; `\parskip`, no indent |

### 2.1 `assignments/<Semester>/HWxx/metadata.tex`

```tex
\newcommand{\HomeworkNumber}{7}
\newcommand{\DueDate}{November 15, 2026}
```
For an all-extra-credit homework (prints "EXTRA CREDIT ASSIGNMENT" in the header), add
`\extracreditassignmenttrue`. `\HomeworkNumber` must match the folder number (HW07 → 7) and
`\DueDate`'s year must match the semester — `tools/check.py` verifies both.

### 2.2 `assignments/<Semester>/HWxx/questions.tex` — the manifest

```tex
% Problem 1 - LED I-V Curve Load-Line Analysis (10 points)
\UseQuestion{led_iv_curve}{v1}{
    basicloadline     = 3,
    ledbrightness     = 2,
    resistorselection = 5,
    ambienthot        = 5 extra,
}

% Problem 2 - Zener Diode Voltage Regulator (16 points)
\clearpage
\UseQuestion{zener_regulator}{v1}{
    inadequatedesign = 5,
    maxresistor      = 5,
    zenercurrent     = 2,
    search           = 4,
}
```
`\UseQuestion{<question id>}{<version>}{<part key> = <points>, ...}`:
- The id is the question's folder name, looked up in `questionbank/index.tex`.
- List **every** `partquestion` key of that source with a whole number of points. Append `extra`
  to mark an extra-credit part (`5 extra`); extra-credit points are excluded from the problem and
  assignment totals and reported separately in the header. Align the `=` signs; trailing comma OK.
- Comment line `% Problem N - <Title> (<X> points)` before each problem; X excludes extra credit.
- `\clearpage` before every problem except the first.
- A manifest may pin any version. Past semesters keep pointing at the version they used.
- To leave a problem out temporarily, comment out the whole block (every line starting `% `).
- **Question-level points:** when the source only gives a total (no per-part breakdown), or the
  question has no parts, write `\UseQuestion{full_wave_rectifier}{v0}{ total = 14, }`. The parts
  then show no points; `total` is a reserved key and can't be combined with per-part points.

Compile-time safety (from `homework.sty`):
- **Errors:** unknown id; id registered twice; the same question used twice in one homework; two
  questions with the same `mainquestion` key in one homework; points that aren't a whole number
  (optionally `extra`); a part listed without `= points`; a source loaded without `\UseQuestion`;
  the old `\Point` / `\MarkExtraCredit` macros.
- **Warnings:** a part with no points (counts as 0); points given for a part that doesn't exist.

### 2.3 `questionbank/<topic>/<id>/vN/source.tex` — question content

```tex
\begin{mainquestion}{questionkey}{Question Title}

Shared problem statement, givens, figures...

\begin{center}
\includegraphics[width=4in]{figure.png}
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
- **File paths are relative to the version folder.** Sources are loaded with `\subimport`, so
  `\includegraphics{figure.png}` finds `vN/figure.png`, and `\includegraphics{../v0/plot.png}`
  reuses a figure from an earlier version of the same question. Same for `\verbatiminput{x.m}`.
  Never write `questionbank/...` paths, absolute paths, or reach into another question
  (`../../other_question/...`) — copy the file instead, so questions can be moved independently.
- The prompt is the **second mandatory argument** of `partquestion` (in braces, may be on the next
  line). The part letter and "(n points)" are generated automatically — never type them.
- Every part gets the label `prob:<questionkey>:<partkey>`; refer to other parts with
  `part (\cref{prob:<questionkey>:<partkey>})`, which prints the part letter.
- Every part should have an `answer` environment, even if empty
  (see `00_course_introduction/lab_training/v0/source.tex`). `\begin{answer}[2in]` gives the
  student writing space used by `style-mark` (ignored by `style-jeff`). Put `\begin{answer}[..]` and
  `\end{answer}` each alone on a line, in column 0 (no indentation).
- `\questionpoints` marks where `style-mark` prints the question's "[N pts]" (Mark's sources put it
  at the start of the statement); `\qnewpage` gives a page break in the `style-mark` student
  version. Both are harmless in `style-jeff`. A question may have no parts at all (statement and
  answer only); give it `total = N` in the manifest.
- `circuitikz` (options `american, siunitx, nooldvoltagedirection`), `tikz` and `pgfplots`
  (`compat=1.18`) drawings can be written inline.
- Do not put `\documentclass`, `\usepackage`, `\begin{document}`, `\section*{Problem 4}`, or point
  values in a source file.
- Figure captions inside answers use `\captionof*{figure}{...}` within a `center` environment.
  If you use a `figure` float, give it a meaningful label like `fig:<questionkey>:<name>`.

### 2.4 `questionbank/index.tex`

```tex
% --- 04_diode_circuits
\RegisterQuestion{led_iv_curve}{04_diode_circuits/load_line/led_iv_curve}
```
One line per question: id (= folder name) and its folder below `questionbank/`. **To move or
rename a question folder:** move it (`git mv`), then update its line here — or run
`python tools/check.py --fix-index`, which regenerates the whole file from the folder tree. If the
folder name (id) changes, also update the `\UseQuestion` lines that use it (grep the manifests).
No source file ever needs to change when a question moves.

### 2.5 Environments and macros available (from `style/`)

| Name | Purpose |
|---|---|
| `\UseQuestion{id}{vN}{points}` | Manifest only; see 2.2. |
| `\RegisterQuestion{id}{folder}` | `questionbank/index.tex` only; see 2.4. |
| `mainquestion{key}{title}` | One problem. Prints "Question n - title (X points)". |
| `partquestion{partkey}{prompt}` | One graded part, auto-lettered (a), (b), ... |
| `answer[height]` | Solution text (style-jeff: blue; style-mark: framed sans-serif). Student version: removed (style-jeff) or blank space of `height`, default 1in (style-mark). |
| `\questionpoints` | Where style-mark prints the question total; no-op in style-jeff. |
| `\qnewpage` | Page break in the style-mark student version; no-op otherwise. |
| `\HomeworkStyle{...}` | `course.tex` / `metadata.tex` only; see 2.0. |
| `kaitlyn` | Green-colored TA commentary (e.g. a boxed "Why we're doing this problem"), used inside `answer` in a few amplifier solutions. Only use it when the source material has equivalent TA commentary. |
| `\pluralize{n}{point}{points}` | Number + singular/plural word. |
| `\dd` | Upright differential: `\int f(t)\dd t`. |

Packages already loaded (do not add `\usepackage` in sources): amsmath, amssymb, graphicx, xcolor,
xparse, comment, fancyhdr, fontspec, unicode-math, datetime2, siunitx, hyperref, cleveref, pgfkeys,
listings (Python style preset), verbatim, caption, import, tikz, circuitikz, pgfplots, enumitem,
mdframed, float. Notably **not** loaded: booktabs, subfig, adjustbox. If a source needs another
package, ask the user before adding it to `style/homework.sty` (it affects every homework).

### 2.6 The question bank catalog (`main_questionbank.tex`)

A third root document that renders **every version of every question** for browsing and choosing
problems. Line 4 selects `config/student_mode` or `config/solutions_mode`.
- Table of contents: one section per topic folder, one subsection per question folder
  (title + id). Each version starts on its own page with an info box: id, version, folder,
  author, date, homeworks that used it (with point totals), part keys in order (ready to copy into
  `\UseQuestion`), and the version-history notes. Then the question itself, without points.
- Pieces: `config/questionbank.tex` (course code/title for the title page; replaces
  `config/shared.tex`), `style/questionbank.sty` (layout), and the generated
  `questionbank/catalog.tex`. `homework.sty` supplies catalog mode (`\hwcatalogtrue`):
  `\ShowQuestion{id}{vN}` loads a version without points and scopes its `\label`/`\cref`s to that
  version, since all versions of a question share part labels.
- Metadata comes from each question's `version_history.md` (Author, Date, Content, Concepts).
  Missing or `TODO` authors are shown as "Jeff Stribling (assumed)". A "Questions by concept"
  index after the table of contents lists every tag in `questionbank/tags.md` order with links to
  the questions using it (also at the end of `questionbank/README.md`).
- `catalog.tex` is committed so Overleaf can compile it, but only the local tool regenerates it:
  after adding/moving questions or editing version histories, run `python tools/check.py --catalog`.
  In Overleaf, compile it by setting the project's Main document to `main_questionbank.tex`
  (that setting is project-wide, so switch it back afterwards).

---

## 3. Naming conventions

The bank was reorganized and renamed in November 2026 (old ids such as `circuit_001` or
`solderpaste` no longer exist). Follow these conventions for new content.

- **Question id / folder name**: descriptive snake_case naming the physics/skill — `led_iv_curve`,
  `zener_regulator`, `cs_amplifier_design`. Must be unique across the whole bank (checked). Avoid
  numbered names (`circuit_001`), names of a scenario rather than the concept, and combining two
  problems into one folder.
- **Renaming a question** (changing its id) means: `git mv` the folder, update every
  `\UseQuestion{<old id>}` in `assignments/` (including commented-out ones), mentions of the old id
  in `version_history.md` files, then `check.py --fix-index --catalog`.
- **Question key** (`mainquestion` first argument): short, lowercase, no separators —
  `ledloadline`, `zenerregulator`, `cstransfer`. All versions of one question share the key.
  Keys must be unique across *different* questions: the key prefixes every part label, so two
  questions with the same key in one homework are a compile error. `tools/check.py` reports any
  key shared by different questions.
- **Part keys**: short lowercase descriptions of the part — `basicloadline`, `maxresistor`. Unique
  within the question.
- **Figure files**: descriptive lowercase names (`iv_curve.png`, `schematic.png`). Never leave
  camera/screenshot names (`IMG_1234.jpeg`, `Screenshot ... AM.png`) — macOS screenshot names
  contain a non-breaking space that breaks paths. No spaces in any file or folder name.
- Keep a `.drawio` source next to any figure drawn in draw.io (`figures.drawio`).

---

## 4. Versioning

- `v0` is the original. Create `v1`, `v2`, ... when the **problem content changes** (new values,
  new parts, different circuit) — especially if any past manifest uses the current version. Past
  semesters must keep compiling to what students actually received.
- Small corrections that don't change what students were asked (typos, a broken font command, a
  wrong path) may be fixed in place.
- A new version may reuse unchanged figures from an earlier version (`../v0/fig.png`). This means
  **older version folders must never be deleted**. Copy the figure into the new folder if you're
  also modifying it.
- **Every question has a `<id>/version_history.md`** (`check.py` warns otherwise), in exactly
  this format (title = the `mainquestion` title). Add a `### vN` entry whenever you create a
  version. Write `TODO` for anything you don't know rather than guessing. Author, Date, Content
  and Concepts are shown in the question bank catalog (section 2.6); for an imported question
  record the instructor who wrote it.
- **Concepts** are tags from the vocabulary in `questionbank/tags.md` (grouped by syllabus topic,
  plus skill tags such as `design`, `datasheet`, `measurement`). Use existing tags where they fit;
  if a new concept is needed, add it to `tags.md` (one line: `` - `tag-id` — description ``) and
  mention it to the user. `check.py` errors on tags not in the vocabulary;
  `check.py --rename-tag old new` renames a tag everywhere.
  ```markdown
  # <Question Title>

  Concepts: <tag>, <tag>, ...

  ## Version History

  ### v0 - Initial version
  - Author: <name>
  - Date: <YYYY-MM-DD, semester, or —>
  - Content: <short description; parts and points>

  ### v1 - <short label>
  - Author: <name>
  - Date: <YYYY-MM-DD>
  - Content: <what changed and why>
    - <optional detail bullets>
  ```

---

## 5. LaTeX style conventions

- Units: use `siunitx` — `\qty{5}{\kilo\ohm}`, `\qty{0.4}{\milli\ampere\per\celsius}`,
  `\frac{5}{3}\unit{\volt}`, `\num{25e3}`. Keep signs and operators outside: `V_D - \qty{1}{\volt}`.
  (Most of the bank was converted; about 130 plain forms like "17 mA" in running text remain.)
- Text-mode emphasis: `\textit{...}`, `\textbf{...}`, `\emph{...}`. Never `\it{...}` / `\bf{...}`
  in text — they are switches, and the braces don't limit them.
- Display math: `\[ ... \]` or `align*`; never `$$ ... $$`. "Evaluated at" bars need a null left
  delimiter: `\left.\frac{v_o}{v_i}\right|_{R_L\to\infty}`.
- Local `\def`/`\renewcommand` for convenience is acceptable only inside a group (e.g. inside an
  `answer` or `{...}`) so it doesn't leak into later questions.
- Use `itemize`, `enumerate`, `center`, `tabular`, `\href{url}{text}`, `\url{...}` as normal.
- Separate parts with a `% =====...` comment line for readability.

---

## 6. Importing from a Word document (.docx)

Conversion: see `import/how_to_convert.md` (pandoc into a per-import scratch folder such as
`import/winter2026_hw03/`, which is deleted after the import).

Import rules:
- **Do not change the wording of problems or solutions.** Import only; do not revise, correct, or
  "improve" content. If something looks wrong (inconsistent numbers, garbled OCR), keep it and add
  a `% NOTE: ...` comment next to it for the user to review (see `09_sinusoidal_analysis/filters_and_bode_plots/bridge_rc_filter/v0`).
- pandoc tends to bold everything in problem statements (`\mathbf{R}_{\mathbf{w}}`, `**...**`).
  Earlier imports sometimes kept this (e.g. `cascade_cd_cg/v0`). Ask the user at the
  start of an import whether to strip conversion-artifact bolding (keeping intentional emphasis and
  bold phasors/vectors) or preserve it verbatim.
- Strip point annotations like "(12 points)" or "(24 points total)" from the text — they go in the
  manifest's `\UseQuestion` points list. Check that the sum matches the document's stated total.
- Split a multi-problem document into one `questionbank/<topic>/<id>/v0/` per problem.
- Copy usable raster figures (PNG/JPEG) into that problem's `v0/` folder with descriptive names and
  reference them by bare filename.
- **Never `\includegraphics` a `.wmf` file** — it breaks compilation. Instead leave a visible
  placeholder plus a comment, e.g.
  ```tex
  % TODO(import): equation/figure from media/image3.wmf could not be converted.
  \textbf{[MISSING EQUATION/FIGURE — see image3.wmf in the original document]}
  ```
  If the `.wmf` was an equation and the surrounding text makes the equation unambiguous, ask the
  user whether to transcribe it by hand.
- If the source document has problems that already exist in the question bank (check
  `questionbank/README.md`), **stop and ask** whether to reuse the existing version, create a new
  version of the existing question, or create a separate question.

## 7. Importing from another LaTeX project

- Do not copy the other project's preamble, packages, or custom environments. Translate its problem
  structure into `mainquestion`/`partquestion`/`answer`. If it relies on packages not loaded here
  (circuitikz, tikz, enumitem, booktabs, ...), list them and ask the user before adding anything to
  `style/`.
- Map its solution mechanism (`\ifsolution`, `solution` env, `exam` class `solution`, etc.) to
  `answer`, and its point values to the `\UseQuestion` points list.
- Copy its figures into the new `vN/` folders and reference them by bare filename.
- Pick question ids and keys that don't collide with the existing bank (section 3; `check.py`
  reports collisions).
- Problems that share a circuit with an existing question are filed by the **method they ask the
  student to use** (e.g. the same circuit solved by nodal analysis vs. by superposition are
  different questions). A re-typeset version of the same problem becomes a new `vN`.
- Point annotations and labels typed into the text ("(5 pts)", `\textbf{[3 pts]}`, a leading
  "(a)") are formatting: remove them and put the points in the manifest. A trailing `\\` before
  an answer is also formatting. Everything else is copied exactly.
- Reference: the Winter 2026 import of Mark Horowitz's `exam.cls` project (Nov 2026) mapped
  `\question{T}` → `mainquestion`, `\points{N}` → `\questionpoints` + manifest points,
  top-level `enumerate` `\item`s → `partquestion`s (several lists split by `[resume]` → one
  sequence of parts), `answer[h]` → `answer[h]`, `$$...$$` → `\[...\]`; text was verified
  identical to the original after removing markup.

---

## 8. Step-by-step: adding a new homework

Before creating any files, **ask for anything missing** and then **summarize the plan**:
- Semester (e.g. `Winter 2026`) and homework number (e.g. `HW03`); for a new semester, the
  instructor, course code/title if different, and header settings (due time, name reminder).
- Due date.
- Where the source material is (docx/markdown + media, or LaTeX files).
- For each problem: topic folder, question id (folder name), question key, part keys, points per
  part, extra credit parts, and whether it reuses/extends an existing question.
- The intended total points (and extra credit total).

Then:
0. If the semester folder is new, create `assignments/<Semester>/course.tex` (section 2.0).
1. Create `assignments/<Semester>/HWxx/metadata.tex` (section 2.1).
2. Create or reuse question sources under `questionbank/<topic>/<id>/vN/` (section 2.3), with
   figures in the same folder.
3. Register new questions: `python tools/check.py --fix-index`.
4. Create `assignments/<Semester>/HWxx/questions.tex` (section 2.2).
5. Create/update each question's `version_history.md`, including its `Concepts:` tags (section 4).
6. Run the checks in section 9 and regenerate the catalogs (`--catalog`), so the new questions
   appear in `questionbank/README.md` and in the question bank PDF.
7. Do **not** edit `config/current_assignment.tex`; tell the user the two values to set to compile.
8. Commit on a branch and report the full list of added / modified / moved files for mirroring into
   Overleaf (section 0).

---

## 9. Checks before handing back

1. `python tools/check.py` — must report **0 errors**; read every warning. It verifies the index,
   every manifest (points ↔ parts, ids, versions, stated totals), every source (figures exist with
   exact case, no root-relative paths, no `.wmf`, `\cref` targets exist, no preamble commands),
   key collisions, and metadata (`\HomeworkNumber`, `\DueDate` year, `course.tex`).
2. `python tools/build_all.py --only "<Semester>/HWxx"` — both modes must compile with 0 warnings.
3. If you changed anything shared (`style/`, `config/`, an existing question), run
   `tools/build_all.py --save before.json` before the change and `--compare before.json` after:
   page counts, totals, images loaded, and warnings must match except where intended.
4. `python tools/check.py --catalog` to refresh `questionbank/README.md` and
   `questionbank/catalog.tex`. (`tools/build_all.py` without `--only` also compiles the catalog,
   which exercises every version of every question, including unused ones.)
5. Ask the user to compile in Overleaf as the final check.

---

## 10. Known quirks / legacy items (don't imitate, don't "fix" unless asked)

- Refer to parts only through the automatic `prob:<key>:<part>` labels; don't add hand-written
  `\label{prob:...}` lines (one in `tellegen_power_balance/v0` was removed for this reason).
- Standalone original documents live in `<id>/originals/` (`function_generator_loading`,
  `thevenin_from_measurements`, `lab_training`). They have their own `\documentclass` and must never be loaded.
- Some unused question versions exist (see "Used in: —" in `questionbank/README.md`). Unused ≠
  obsolete; leave them.
- Older content mixes key-naming styles (`diode_hogging` vs `ledloadline`) and has some plain-text
  units (section 5).
- Several `version_history.md` files contain `TODO` fields where the author/date/changes are not
  known.
