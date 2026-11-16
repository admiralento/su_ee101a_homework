# Importing or creating a new homework assignment in this project

This workspace uses a small LaTeX build system that separates course metadata, assignment metadata, reusable question content, and shared formatting. The goal is to create a new homework in the same style as the existing assignments under the assignments/ folder.

## 1. What each file is for

### Top-level entry points
- main_student.tex
  - The student-facing build entry point.
  - It loads student-mode settings, shared config, shared style, and the homework package.
  - It then includes the currently selected assignment via:
    - \input{assignments/\AssignmentFolder/\Semester/questions.tex}
- main_solutions.tex
  - The solutions build entry point.
  - It is the same structure as main_student.tex, but it loads solutions_mode.tex instead of student_mode.tex.

### Configuration files
- config/course.tex
  - Course-level metadata only.
  - Contains \CourseCode, \CourseTitle, and \Instructor.
- config/current_assignment.tex
  - Selects which homework folder and semester are compiled.
  - This file must be updated when building a different homework.
  - Example:
    - \def\AssignmentFolder{HW03}
    - \def\Semester{Summer 2026}
- config/shared.tex
  - Pulls in the course metadata and the currently selected assignment metadata.
  - It is the bridge between the assignment selection and the rest of the document.
- config/student_mode.tex
  - Disables solutions output.
- config/solutions_mode.tex
  - Enables solutions output.

### Assignment folders
- assignments/HWXX/
  - One folder per homework number.
  - Contains the homework-specific metadata and the semester-specific subfolders.
- assignments/HWXX/metadata.tex
  - Defines the homework number, for example:
    - \newcommand{\HomeworkNumber}{3}
- assignments/HWXX/[Semester]/metadata.tex
  - Defines the due date for that semester offering, for example:
    - \newcommand{\DueDate}{July 12, 2026}
- assignments/HWXX/[Semester]/questions.tex
  - This is the assignment manifest.
  - It should list each problem in order, assign point values using \Point, mark extra credit with \MarkExtraCredit, and include the corresponding questionbank source file.
  - It is the file that tells the build which questions belong to this homework.

### Question bank
- questionbank/<topic>/<question_name>/vN/source.tex
  - This is where the actual problem statement and solution content live.
  - Each problem source should usually begin with \begin{mainquestion}{key}{Title} and then use \begin{partquestion}{partkey}{Prompt} for each subpart.
  - The key names used in \Point and \MarkExtraCredit should match the keys used in the question source.
- questionbank/<topic>/<question_name>/vN/figures.drawio or other assets
  - Keep related figures and supporting files in the same version folder.
  - Use relative paths from the project root when including graphics.
- questionbank/<topic>/<question_name>/version_history.md
  - Optional but encouraged for documenting revisions.

### Style files
- style/homework.sty
  - Defines the custom homework macros and environments used throughout the question bank.
  - This is where environments such as mainquestion and partquestion are implemented.
  - Do not redefine these in individual questions unless you are intentionally extending the system.
- style/shared.sty
  - Contains shared LaTeX packages and utility definitions.

## 2. How a new homework should be created

1. Create a new assignment folder such as assignments/HW04/.
2. Create the homework-level metadata file at assignments/HW04/metadata.tex with the homework number.
3. Create a semester folder such as assignments/HW04/Summer 2026/ and add a metadata.tex file with the due date.
4. Create questions.tex inside that semester folder.
5. Add the problem list there, using the same pattern as the existing assignments:
   - Add a comment for each problem.
   - Use \Point{questionkey}{partkey}{points} for each graded subpart.
   - Use \MarkExtraCredit{questionkey}{partkey} for extra credit parts.
   - Use \clearpage between major problems.
   - Use \input{questionbank/.../source} to include the problem source.
6. Create or reuse a question source under questionbank/.
7. Update config/current_assignment.tex so the build points to the new homework folder and semester.
8. Compile with main_student.tex or main_solutions.tex.

## 3. Folder hierarchy conventions

The include paths are expected to be consistent with the directory structure.

- The assignment manifest should be included from the top-level entry point using the macros from config/current_assignment.tex.
- The question sources should be included from the assignment manifest with paths like:
  - \input{questionbank/diodes/led_iv_curve/v1/source}
- Graphics in those sources should use paths relative to the project root, such as:
  - \includegraphics[width=4in]{questionbank/diodes/led_iv_curve/v1/fig4.png}

Do not use absolute paths. Do not place files in a folder that does not match the logical topic/question hierarchy. If a problem is about LEDs, place it under questionbank/diodes/ or a sensible subtopic folder.

- When importing a multi-question document, split each problem into its own questionbank folder and create a dedicated v0/ version folder for each source. Keep the associated figures in the same v0 folder so the relative graphics paths remain stable.

## 4. LaTeX conventions encouraged in this project

- Keep content modular: put reusable question content in questionbank/ and assignment-specific organization in assignments/.
- Use the existing custom environments rather than inventing new ones.
- Keep question keys and part keys short, descriptive, and consistent across the assignment manifest and the source file.
- Keep point totals aligned between the assignment manifest and the problem content.
- Use comments to organize the file and make it easier to maintain.
- Prefer standard LaTeX constructs such as itemize, center, equation, and href.
- Use the package utilities already loaded by style/homework.sty and style/shared.sty instead of adding new dependencies unless necessary.
- When adding images, place them next to the source file or in the same version folder so the relative path remains stable.
- If a source was revised, create a new version folder such as v1/ rather than overwriting v0/ blindly.
- If a conversion from Word produced imperfect equations or figures, leave a note in the LaTeX source near the affected content so the user can manually fix it.
- When possible use the siunitx package for si unit formatting. For example, use patterns like
'''tex
\qty{5}{\kilo\ohm}
\frac{5}{3}\unit{\volt}
'''

## 5. Additional Instructions

- Do not change the wording of the problems, nor the solutions. Your role is to import the text only, not revise.
- If a .wmf image file would be included in the latex, do not add it. This will block compliation. Instead, add placeholder text that makes it clear that an image was unable to be imported and the user need to address it.

## 6. Minimal template pattern

### Assignment manifest
```tex
% Problem 1
\Point{questionkey}{partone}{5}
\Point{questionkey}{parttwo}{5}
\input{questionbank/topic/questionname/v1/source}
```

### Question source
```tex
\begin{mainquestion}{questionkey}{Question Title}

\begin{partquestion}{partone}
{Prompt text here.}
\begin{answer}
Answer text here.
\end{answer}
\end{partquestion}

\end{mainquestion}
```

## 7. Practical reminder

Before creating new files, briefly summarize:
- which new files will be created,
- which questionbank source will be used,
- and the intended total point value of the assignment.

This project is easiest to maintain when every new homework follows the same structure: metadata in assignments/, content in questionbank/, and selection in config/current_assignment.tex.

You should review the workspace to make sure you see actual examples of how these standards are implemented.

## 8. Export directory for Overleaf import

When the import is complete, create a small export directory that contains only the new homework files and assets. Preserve the same relative folder hierarchy so the export can be imported cleanly into Overleaf. For example:
- assignments/HW05/metadata.tex
- assignments/HW05/Summer 2025/metadata.tex
- assignments/HW05/Summer 2025/questions.tex
- questionbank/<topic>/<questionname>/v0/source.tex
- questionbank/<topic>/<questionname>/v0/<image assets>

Copy usable raster assets (PNG/JPEG) into the same questionbank v0 folders. Do not include WMF files in the export; instead leave a clear placeholder in the LaTeX source where the figure needs conversion or replacement.

## 9. Ask for missing details

If the homework number, semester, due date, or source file location is not provided, ask for that information before proceeding. Useful questions include:
- "Which homework assignment should this be imported as? (for example, HW05)"
- "What semester offering and due date should be used?"
- "Where are the source markdown and image asset files located?"
- "Where should the export directory be created, and what should it be called?"

If the export folder or file location is not specified, ask for the intended destination and naming convention so the package can be created in the correct place.