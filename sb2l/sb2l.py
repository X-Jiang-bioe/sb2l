#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Created on Fri Oct 18 14:10:40 2019
"""
@author: XJiang, HSauro
SBML Utilitites
"""


def s2latex (sbmlArgument, file_path = None):
    ''' Convert sbml to a latex string
    
    Args: 
        param1 (string): file name to sbml OR sbml string
        
        file_path (string, optional): path for creation of a pdf file, only works with latexmk or pdflatex installed
    Returns:
        LaTeX string
    '''
    try:
        import tesbml as libsbml
    except:
        import libsbml
        
    try:
       from libsbml import formulaToL3String, writeMathMLToString, parseFormula, readMathMLFromString
    except:
        from tesbml import formulaToL3String, writeMathMLToString, parseFormula, readMathMLFromString
       
    
    import math
    import pathlib # For extracting file extensions
    import os
    
    def mathml2latex_yarosh(equation):
        from lxml import etree
        import os
        """ MathML to LaTeX conversion with XSLT from Vasil Yaroshevich, Modified by Xieergai Jiang"""
        script_base_path = os.path.dirname(os.path.realpath(__file__))
        xslt_file = os.path.join(script_base_path, 'xsl_yarosh', 'mmltex.xsl')
        dom = etree.fromstring(equation)
        xslt = etree.parse(xslt_file)
        transform = etree.XSLT(xslt)
        newdom = transform(dom)
        return str(newdom)

    def getLaTeXFromAST (tree):
        xmlstr = writeMathMLToString(tree)
        # Strip out the header
        xmlstr = xmlstr.replace ('<?xml version="1.0" encoding="UTF-8"?>', '')
        
        return  mathml2latex_yarosh(xmlstr).strip ('$')

    #The zeroes are out of nessessity, I don't know why, but just having a single obj variable does not work
    #So, predefined all classes that are used later
    def listfiller(Commands , obj = 0, R = 0 ,Sp = 0, 
               ass = 0, Par = 0, tr = 0, libsbml = libsbml, 
               tofill = [], twoD = 1):
        '''
        Uses a dismal method of evaluating a piece of code 
        from 'Commands' to fit a specific string into 'tofill' 
        takes in a libsbml object as obj
        
        if twoD = 0, then does not fill 'tofill' with the templin as one element
        but returns the compiled templin as 1-D list
        '''
        l = len(Commands)
        templin = [None]*l
        for i in range(l):
            templin[i] = eval(Commands[i])
        if twoD == 1:
            tofill.append(templin)
            return tofill
        elif twoD == 0:
            return templin
        
    def round_half_up(n, decimals=0):
        '''
        use this to round numbers that are way to big to put in a table
        '''
        multiplier = 10 ** decimals
        return math.floor(n*multiplier + 0.5) / multiplier
    
    def lawcutter(prefix):
        '''
        cuts up the string version of the KineticLaw object into something the 
        mathml converter can read
        '''
        lis = prefix.split('\n')
        i = len(lis)-1
        if ('  <listOfParameters>' in lis):
            i = lis.index('  <listOfParameters>') #NOT EVERY MODEL WILL HAVE THIS THOUGH
        lis = lis[1:i]
        for n in range(0, len(lis)):
            lis[n] = lis[n][2:] #so, here we are messing with indentation, not sure if it will be consistent
                                #for all models or even if it is nessessary, but it's here
        newstr = '\n'.join(lis)
        return newstr
    
    def notecutter(prefix):
        '''
        same as lawcutter but for notes
        
        '''
        prefix = prefix.replace("\n", "")
        lis = prefix.split('>')
        i = len(lis) - 2
        lis = lis[1:i]
        #for n in range(0, len(lis)):
        #   lis[n] =lis[n][1:]
        newstr = '>'.join(lis)
        newstr = newstr + '>'
        return newstr
    
       
    # ----------------------------------------------
    # Start of sb2l
    # ----------------------------------------------   
    reader = libsbml.SBMLReader()
    # Check if its a file name
    if os.path.isfile (sbmlArgument):     
       suff = pathlib.Path (sbmlArgument).suffix
       if suff == '.xml' or suff == '.sbml':
           sbmldoc = reader.readSBMLFromFile (sbmlArgument)
    else:
      # If it's not a file, assume it's an sbml string
      sbmldoc = reader.readSBMLFromString(sbmlArgument)  # Reading in the model

    errors = sbmldoc.getNumErrors()
    numReadErr = 0
    numReadWarn = 0
    for i in range(errors):
        severity = sbmldoc.getError(i).getSeverity()
        if (severity == libsbml.LIBSBML_SEV_ERROR) or (severity == libsbml.LIBSBML_SEV_FATAL):
           seriousErrors = True
           numReadErr += 1
        else:
           numReadWarn += 1

        oss = libsbml.ostringstream()
        sbmldoc.printErrors(oss)
        errMsgRead = oss.str()
        raise RuntimeError (errMsgRead)

    Model_id = sbmldoc.model.getName() # This is essentially how each list is filled, using commands for LibSBML
    Model_id = Model_id.replace (r'_', r'\_')    
           
    Compartments = [] 
    Species = [] 
    Parameters = []
    Reactions = []
    Events = []
    Rules = []
    FunctionDefinitions = []
    FunctionArgList = []
      
    # making a notes list
    lis = None
    notes = sbmldoc.model.getNotesString()
    if len(notes) != 0:
        lis = notecutter(notes).split('<')
        lis = lis[2:len(lis)]
    del notes
        
    
    l = sbmldoc.model.getNumCompartments()
    if l != 0:
        ComList = ['obj.getId()', 'obj.getSBOTerm()','obj.getSpatialDimensions()','obj.getSize()','obj.getConstant()']
        for x in range(0,l):
            obj = sbmldoc.model.getCompartment(x)
            Compartments = listfiller(ComList, obj = obj, tofill = Compartments) # see the function above 
        del(ComList)
    
    
    l = sbmldoc.model.getNumSpecies()
    if l != 0:   
        SpecList = ['obj.getId()','obj.getInitialConcentration()','obj.getHasOnlySubstanceUnits()', ' obj.getBoundaryCondition()','obj.getConstant()' ]
        for x in range(0,l):
            obj = sbmldoc.model.getSpecies(x)
            Species = listfiller(SpecList, obj = obj, tofill = Species)
            if not math.isnan (Species[x][1]):
               if (Species[x][1] * 1000 < 1): # need this to round things to fit in the table
                  Species[x][1] = round_half_up(Species[x][1], decimals = 6)
               else:
                  Species[x][1] = round_half_up(Species[x][1], decimals = 4)
            
        del(SpecList)
        
    l = sbmldoc.model.getNumParameters()
    if l !=0:
        ParList = ['obj.getId()','obj.getValue()', 'obj.getConstant()']
        for x in range(0,l):
            obj = sbmldoc.model.getParameter(x)
            Parameters = listfiller(ParList, obj =obj, tofill = Parameters)
        del(ParList)
        
        
    l = sbmldoc.model.getNumReactions()
    if l !=0:
        Rlist = ['R.getId()','R.getReversible()','R.getFast()']
        ReProlist = ['Sp.getSpecies()','Sp.getStoichiometry()','Sp.getConstant()']
        Modlist = ['obj.getSpecies()']
        for x in range(0,l):
            R = sbmldoc.model.getReaction(x)
            RL = listfiller(Rlist, R = R, twoD=0) #starting the element of common matrix/list to append at the end
            
            #making the list for reactants
            lRe = R.getNumReactants()
            ReL = []
            for y in range(0,lRe):
                Sp = R.getReactant(y)
                ReL = listfiller(ReProlist, Sp = Sp, tofill = ReL)
            RL.append(ReL); del(lRe, ReL) #Adding reactants list to RL
            
            #making the list for products
            lPro = R.getNumProducts()
            ProL = []
            for y in range(0,lPro):
                Sp = R.getProduct(y)
                ProL = listfiller(ReProlist, Sp = Sp, tofill = ProL)
            RL.append(ProL);  del(Sp, ProL, y, lPro)#Adiing products list to RL
            
            #making the law thing
            law = R.getKineticLaw()
            prefix = law.toSBML()
            Formula = lawcutter(prefix)
            # repeating the deleted list for now, so that code works consitstnently 
            ParList = ['Par.getId()','Par.getValue()','Par.getDerivedUnitDefinition()', 'Par.getConstant()']
            lPar = law.getNumParameters()
            ParL = []
            for y in range(0, lPar):
                Par = law.getParameter(y)
                ParL = listfiller(ParList, Par = Par, tofill = ParL)
            KinLaw = [Formula, ParL]
            RL.append(KinLaw); del(Formula, law)
            
            lMod = R.getNumModifiers()
            if lMod>0:
                ModL = []
                for y in range(0, lMod):
                    obj = R.getModifier(y)
                    ModL = listfiller(Modlist, obj = obj, tofill = ModL)
                RL.append(ModL)                 
            
            Reactions.append(RL) #Appending all info about a given reaction to the common list
        del(RL, R, Rlist, ReProlist, ParList, lPar,ParL, KinLaw, prefix)       
        
    l = sbmldoc.model.getNumEvents()
    if l !=0:
        TrList = ['tr.getInitialValue()', 'tr.getPersistent()', 'tr.getMath()' ]
        AsList = ['ass.getId()','ass.getMath()']
        for x in range(0,l):
            eve = sbmldoc.model.getEvent(x) #get the event
            tr = eve.getTrigger()
            TrigL = [0,0,0]
            TrigL = listfiller(TrList, tr = tr, tofill = TrigL, twoD = 0) #define trigger things
            m = eve.getNumEventAssignments()
            AssL = []
            for i in range(0,m):
                ass = eve.getEventAssignment(i)
                AssL = listfiller(AsList, ass = ass, tofill = AssL) #add up all of the ID = Formula in a single list
            del (i,m) 
                
            Events.append([eve.getId(), eve.getName(), TrigL, AssL])
        del (TrList, AsList, eve, tr, TrigL, ass, AssL)
        
    l = sbmldoc.model.getNumRules()
    if l != 0:
        RuList = ['obj.getVariable()', 'obj.getFormula()']
        for x in range (0,l):
            obj = sbmldoc.model.getRule(x)
            Rules = listfiller(RuList, obj = obj, tofill = Rules)
        del(RuList)
        del (obj)      
           
    l1 = sbmldoc.model.getNumFunctionDefinitions();
    if l1 != 0:
        FuncList = ['obj.getId()', 'obj.getBody()']
        for x in range (0,l1):
            obj = sbmldoc.model.getFunctionDefinition(x)
            FunctionDefinitions = listfiller(FuncList, obj = obj, tofill = FunctionDefinitions)
            l2 = obj.getNumArguments()
            if l2 != 0:
               for k in range(0,l2):
                   FunctionArgList.append (obj.getArgument (k))    
        
    del(libsbml, lawcutter,l, notecutter, listfiller)
        
    # The part where everything is compiled into the TeX file
    
    from pylatex import Document, Section, Subsection, Subsubsection, Command, Math, Tabular, LongTable 
    from pylatex import Table, LineBreak
    from pylatex.utils import italic, NoEscape, bold
    
    doc = Document() # start a doc
    
    doc.packages.append (NoEscape(r'\usepackage{xcolor}'))
    doc.packages.append (NoEscape(r'\usepackage{titlesec}'))
    doc.packages.append (NoEscape(r"\usepackage{hyperref}"))
    doc.packages.append (NoEscape(r"\hypersetup{colorlinks=true,linkcolor=blue,urlcolor=blue}"))
    doc.packages.append (NoEscape(r"\usepackage{amsmath}"))
    
    doc.preamble.append (NoEscape(r'\definecolor{blue}{cmyk}{.93, .59, 0, 0}'))
    doc.preamble.append ('')
    doc.preamble.append (NoEscape(r'\titleformat{\chapter}[display]'))
    doc.preamble.append (NoEscape(r'  {\normalfont\sffamily\huge\bfseries\color{blue}}'))
    doc.preamble.append (NoEscape(r'  {\chaptertitlename\ \thechapter}{20pt}{\Huge}')) 
    doc.preamble.append (NoEscape(r'\titleformat{\section}'))
    doc.preamble.append (NoEscape(r'  {\normalfont\sffamily\Large\bfseries\color{blue}}'))
    doc.preamble.append (NoEscape(r'  {\thesection}{1em}{}'))
    doc.preamble.append (NoEscape(r'\titleformat{\subsection}'))
    doc.preamble.append (NoEscape(r'  {\normalfont\sffamily\large\bfseries\color{blue}}'))
    doc.preamble.append (NoEscape(r'  {\thesubsection}{1em}{}'))
    doc.preamble.append (NoEscape(r'\titleformat{\subsubsection}'))
    doc.preamble.append (NoEscape(r'  {\normalfont\sffamily\normalsize\bfseries\color{blue}}'))
    doc.preamble.append (NoEscape(r'  {\thesubsubsection}{1em}{}'))
          
    doc.append(NoEscape(r'\begin{center}'))
    doc.append(NoEscape(r'{\normalfont\sffamily\huge\bfseries SBML Model Report}\\'))

    doc.append (NoEscape(r'\vspace{5mm}'))
    doc.append (NoEscape(r'{\normalfont\sffamily\LARGE\bfseries\color{blue} Model name: ' + Model_id + r'}\\'))
        
    doc.append (NoEscape(r'\vspace{5mm}'))
    doc.append (NoEscape(r'\large\today'))
    doc.append (NoEscape(r'\end{center}'))
    
    def rxn_eq(Reaction, Command = Command):
        '''
        Stitches up a list to plug into Math function for reaction equations
        
        '''
        numRe = len(Reaction[3])# the products info is stored as a list in position 3
        numPr = len(Reaction[4])
        try:
            numMod = len(Reaction[6])
        except:
            numMod = 0
        arrow = []
        plus = ['+']
        Re = []
        Pr = []
        
        if numRe > 0:
            for i in range(0,numRe):
                if (i>0):
                    Re = Re + plus
                Re.append(Command(command = 'text', arguments = Reaction[3][i][0])) #Appends with IDs of species that are reactannts
        else:
            Re.append(Command(command = 'text', arguments = ['None']))      
        
        if numPr > 0:
            for i in range(0,numPr):                              # Put in the form Math class can interpret
                if (i>0):
                    Pr = Pr + plus
                Pr.append(Command(command = 'text', arguments = Reaction[4][i][0]))
        else:
            Pr.append(Command(command = 'text', arguments = ['None']))
            
        if numMod > 0:
            arg = []
            for i in range(0,numMod):
                arg.append(Reaction[6][i][0])
            arg = ", ".join(arg)
            arrow = [Command(command = 'xrightarrow', arguments = Command(command = 'text', arguments = arg))]
        else:
            arrow = [Command('longrightarrow')]  
        
        DaList = Re+arrow+Pr
        return DaList   
          
    if lis != None:
        # NOTES -- made from html string, can recognize:
        # <a href...>, <b>, <i>,<br/> and treats emphasis as italic or bold
        # there is a known issue with special characters such as # not being interpreted right
        # to fix that, follow the structure below
        leng = len(lis)
        with doc.create(Section('Notes')):
            def findOccurrences(s, ch):
                return [i for i, letter in enumerate(s) if letter == ch]
            doc.append(Command('raggedright'))
            doc.append(Command('frenchspacing'))
            for i in range(0,leng):
                if (leng<2):
                    doc.append(lis[i])
                    continue
                if ('&apos;' in lis[i]):#THIS if statement is being referenced above, &apos; is the HTML code for 
                                        #the apostrophe
                    lis[i] = lis[i].replace("&apos;","'")
                if ('&amp;' in lis[i]):
                    lis[i] = lis[i].replace("&amp;","&")
                if ('/' in lis[i] and 'br/>' not in lis[i] and '//' 
                    not in lis[i] and len(lis[i].replace(" ",""))<4 and 'strong>' not in lis[i]):
                    continue #! trying to skip every instance of </something> assuming the 4 length as cutoff
                        
                elif ('br/>' in lis[i] and len(lis[i].replace(" ", ""))< 4):
                    doc.append(LineBreak())
                elif ('br/>' in lis[i]):
                    doc.append(LineBreak())
                    doc.append(lis[i].replace("br/>",""))
                elif('p>' in lis[i]):
                    doc.append(Command('par'))
                    doc.append(lis[i][2:len(lis[i])])
                elif('sub>' in lis[i] and '/sub>' not in lis[i]):
                    temp = lis[i].replace("sub>","")
                    doc.append(NoEscape("$_{\\text{"+temp+"}}$"))
                
                elif(('b>'in lis[i] or 'strong>' in lis[i]) and ('/b>' not in lis[i]) and ('/strong>' not in lis[i]) and ('/sub>' not in lis[i])):
                    temp = lis[i].replace("b>", "")
                    temp = temp.replace("strong>","")
                    doc.append(bold(temp))
                
                elif(('i>'in lis[i] or 'em>' in lis[i]) and ('/i>' not in lis[i]) and ('/em>' not in lis[i])):
                    temp = lis[i].replace("i>", "")
                    temp = temp.replace("em>","")
                    doc.append(italic(temp))
                elif(('/b>' in lis[i]) or ('/strong>' in lis[i]) or ('/i>' in lis[i]) or('/em>' in lis[i]) or ('/sub>' in lis[i])):
                    temp = lis[i].replace("/i>", "")
                    temp = temp.replace("/em>","")
                    temp = temp.replace("/b>", "")
                    temp = temp.replace("/strong>","")
                    temp = temp.replace("/sub>","")
                    
                    doc.append(temp)
                elif('a href=' in lis[i]):
                    t_list = lis[i].split('>')
                    pos = findOccurrences(t_list[0], '\"')
                    link = t_list[0][pos[0]+1:pos[1]] #! Assuming that the first to places with " \" "
                                                      #will surround the link
                    doc.append(NoEscape("\href{" + link +"}"+"{"+ t_list[1] +"}"))
                    #! Assuming that in a hyperlink notation: 
                    # i. e <a href="http://link.com">text that the author wants to be seen</a>
                else: 
                    pos = findOccurrences(lis[i], '>')
                    doc.append(lis[i][pos[0]+1:])

            del(leng)
      
    with doc.create(Section('Contents')):
         # Summary of contents of sbml model
        doc.append('The number of components in this model:')
        doc.append(NoEscape(r'\\[2mm]'))
      
        with doc.create (Table (position='htpb')) as table1: 
            doc.append (NoEscape(r'\centering'))
            tbl_cmnd ='' 
            tbl_cmnd = 'l|c|l|c'
            with doc.create(Tabular(tbl_cmnd, booktabs = True)) as table:
                 table.add_row('Element', 'Quantity', 'Element', 'Quantity')
                 table.add_hline()
                 table.add_row ('Compartment', str (len(Compartments)), 'Species',  str (len(Species)))
                 table.add_row ('Reactions', str (len(Reactions)), 'Events', str (len(Events)))
                 table.add_row ('Global Parameters', str (len(Parameters)), 'Function Definitions', str (len(FunctionDefinitions)))
            table1.add_caption ('Components in this model.')
        
    # SPECIES TABLE
    # getting info from the list
    listlen = len(Species) #number of rows
    sublistlen = len(Species[0]) #number of columns 
    tbl_cmnd ='' 
    #tbl_cmnd.join('X|' for i in range(0, sublistlen))
    tbl_cmnd = tbl_cmnd.join('c|' for i in range(0, sublistlen))
    tbl_cmnd = tbl_cmnd[:-1] # Remove last character, dont want verical line
    
    # making a tble for latex
    # As the most simple way of doing this, we can convert the lists into tuples and just paste into
    # the add_row command. For something more complicated: some if statements would be useful   
    with doc.create(Section('Species')):
        doc.append('Table of species in the model:')
        with doc.create(LongTable(tbl_cmnd, booktabs = True)) as table:
            table.add_row(('ID', 'Initial ', 'Only ', 'Boundary', 'Constant'))
            table.add_row(('', 'Concentration','Substance Units',' Conditions', ''))
            table.add_hline()
            for i in range(0, listlen):
                if math.isnan (Species[i][1]):
                   Species[i][1] = 'undefined'
                table.add_row(tuple(Species[i]))
                    
    # GLOBAL PARAMETER TABLE
    listlen = len(Parameters) #number of rows
    if (listlen<1):
        with doc.create(Section('Parameters')):
            doc.append('The function could not identify any global Parameters in the model')
    else:
        sublistlen = len(Parameters[0]) #number of columns 
        tbl_cmnd ='' 
        #tbl_cmnd.join('X|' for i in range(0, sublistlen))
        tbl_cmnd = tbl_cmnd.join('c|' for i in range(0, sublistlen))
        tbl_cmnd = tbl_cmnd[:-1] # Remove last character, dont want verical line

        with doc.create(Section('Parameters')):
            doc.append('The following table is the list of Parameters in the model.')
            with doc.create(LongTable(tbl_cmnd, booktabs = True)) as table:
                table.add_row(('ID', 'Value', 'Constant'))
                table.add_hline()
                for i in range(0, listlen):
                    table.add_row(tuple(Parameters[i]))
                        
    # PROCESS RULES
    listlen = len(Rules)
    if (listlen>=1):
        with doc.create(Section('Rules')):
            doc.append('Number of rules in the model: ' + str (listlen))
            for i in range(0, listlen):
                with doc.create(Subsection('Rule ' + str(i+1)+': '+ Rules[i][0])):
                    doc.append(Math(data = [Rules[i][0] + '=' + Rules[i][1]]))
    
    # PROCESS FUNCTION DEDFINITIONS
    listlen = len(FunctionDefinitions)
    if (listlen >= 1):
        with doc.create(Section('Function Definitions')):
            doc.append('Number of usr defined functions in the model: ' + str (listlen))
            for i in range(0, listlen):
                latexstr = getLaTeXFromAST (FunctionDefinitions[i][1])
                
                with doc.create(Subsection('Function ' + str(i+1))): 
                    doc.append (NoEscape ('$$' + '\\text{' + FunctionDefinitions[i][0].replace('_','\\_') + '}\ ('))
                    for j in range (0, len (FunctionArgList)):
                        if len(FunctionArgList)>10: 
                            break
                        latexarg = getLaTeXFromAST(FunctionArgList[j])
                        if j == len (FunctionArgList)-1:
                           doc.append(NoEscape(str(latexarg.replace('_','\\_'))))
                        else: 
                           doc.append(NoEscape(latexarg.replace('_','\\_') + ','))
                    doc.append(NoEscape ('): ' + latexstr.replace('_','\\_') + '$$'))

    # PROCESS EVENTS
    listlen = len(Events)
    if (listlen>=1):
        with doc.create(Section('Events')):
            doc.append('Number of events defined in the model: ' + str (listlen))
            for i in range(0, listlen):
                with doc.create(Subsection('Event '+ str(i+1)+': '+ Events[i][0])):
                    if (len(Events[i][1])>0):
                        with doc.create(Subsubsection('Name', numbering = False)):
                            doc.append(Events[i][1])
                    with doc.create(Subsubsection('Trigger', numbering = False)):
                        doc.append (NoEscape('$$' + getLaTeXFromAST (Events[i][2][2]) + '$$'))
                    with doc.create(Subsubsection('Assignments', numbering = False)):
                        for j in range(0, len(Events[i][3])):
                            assTree = parseFormula (Events[i][3][j][0])
                            ass = '$$' + getLaTeXFromAST(assTree) + '=' + getLaTeXFromAST (Events[i][3][j][1]) + '$$'
                            doc.append(NoEscape(ass))                           
                               
    # PROCESS REACTIONS
    listlen = len(Reactions) # number of rows
    
    with doc.create(Section('Reactions')):
        doc.append('Number of reactions in the model: ' + str(listlen))
        for i in range(0, listlen):
            with doc.create(Subsection('Reaction ' + str(i+1) + ': ' + Reactions[i][0])):
                
                with doc.create(Subsubsection('Reaction equation', numbering=False)):
                    doc.append(Math(data = rxn_eq(Reaction = Reactions[i])))
                with doc.create(Subsubsection('Kinetic Law', numbering=False)):  
                    m = readMathMLFromString(Reactions[i][5][0])
                    formula = getLaTeXFromAST (m)
                    formula = formula.replace ('\mathrm', '\ \mathrm')
                    doc.append(NoEscape('$$v =' + formula.replace('_','\\_') + '$$'))
                with doc.create(Subsubsection('Local Parameters')):
                    if len(Reactions[i][5][1]) != 0:
                        sublistlen = len(Reactions[i][5][1][0])
                        tbl_cmnd = ''
                        tbl_cmnd = '||'+ tbl_cmnd.join('c|' for n in range(0, sublistlen)) +'|'
                        with doc.create(LongTable(tbl_cmnd, booktabs = False)) as table:
                            table.add_hline()
                            table.add_row(('ID', 'Value','Units', 'Constant'))
                            table.add_hline()
                            table.add_hline()
                            listleng = len(Reactions[i][5][1])
                            for j in range(0,listleng):
                                table.add_row(tuple(Reactions[i][5][1][j]))
                                table.add_hline()
                    else:
                        doc.append('No LOCAL Parameters found')
        
    del(Command, Document, NoEscape, Section, Subsection, italic)
    import traceback
    if (file_path == None):
        return doc.dumps()
    else:
        try:
            doc.generate_pdf(filepath = file_path)
        except:
            print("An error in compilation has occured.\n An attempt to generate .tex object was made. \n The error came with following message:")
            traceback.print_exc()
            with open(file_path+'.tex', 'w') as f:
                f.write(doc.dumps())

