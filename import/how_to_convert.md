# Converting a Word (.docx) homework for import

1. In Word, convert all equations to the standard Office Math format (this turns equation images
   into machine-readable math).
2. Make a scratch folder for this import, e.g. `import/winter2026_hw03/`, and put the `.docx` in it.
3. From inside that folder, run:

   ```
   pandoc --extract-media=. input.docx -o output.md
   ```

   The text is now in `output.md` and the images are extracted to `media/`. Any `.wmf` files are
   equations or figures that did not convert; they need to be redone by hand (see
   `import_instructions_for_LLM.md`).
4. After the import is finished and reviewed, delete the scratch folder.
