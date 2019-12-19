# sb2l

### Description ###

Translates biological models written in SBML into LaTeX code to be compiled and read by human eye

### Dependencies ###

The current version runs 1.3.1 version of `PyLaTeX`

Either `Tellurium` or `python-libsbml` is also required 

For PDF creation functionality, either `latexmk` or `pdflatex` needs to be installed on the computer

### Installation ###

`pip install sb2l`

### How to Use ###
The following structure gives a LaTeX string that can be copied to a online compiler like `Overleaf`:
```
import sb2l
latexStr = sb2l.s2string(sbmlStringOrFile)
```
If using with Tellurium or Antimony: 
```
import sb2l
latexStr = sb2l.s2latex(model_name.getSBML())
```
For making PDF files (The filepath must NOT have a .pdf or .tex suffix)
```
import sb2l
filepath = "/Users/Username/Desktop/theDesiredNameOfFile" #[NOTICE: no ".anything"]
sb2l.s2pdf(sbmlStringOrFile, file_path = filepath);
```
The same structure can be used to generate a .tex file if used with `sb2l.s2latex`

To generate the PDF file and open with the default PDF reader

```
import sb2l
filepath = "/Users/Username/Desktop/theDesiredNameOfFile" #[NOTICE: no ".anything"]
sb2l.s2open(sbmlStringOrFile, file_path = filepath);
```
### License ###

MIT License

Copyright (c) 2019

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

