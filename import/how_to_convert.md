First take your docx file and convert all equations to the standard office math format (converts from images to latex so its computer readable).
Next run the following command in this 'temp' folder:
pandoc --extract-media=. input.docx -o output.md
The text is now readable by computer and the images are linked in this seperate folder. The wmf files are the equations that did not convert correctly.