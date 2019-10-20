# sb2l

### Description ###

Translates biological models written in SBML into LaTeX code to be compiled and read by human eye

### Dependencies ###

The current cersion runs 1.3.1 version of PyLaTeX

For PDF creation functionality, either `latexmk` or `pdflatex` needs to be installed on the computer

### How to Use ###

```
import s2l
latexStr = s2l.sbml2latex(sbmlString)
```
If using with Tellurium or Antimony: 
```
latexStr = s2l.sbml2latex(model_name.getSBML())
```
For making PDF files (The filepath must NOT have a .pdf or .tex suffix)
```
filepath = /Users/Username/Desktop/thefile
s2l.sbml2latex(sbmlStringOrFile, filepath);
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

