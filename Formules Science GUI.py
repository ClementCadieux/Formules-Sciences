from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import Separator, Style
import math
from xml.etree import ElementTree as ET
from decimal import Decimal

#-----------------------------------------------------------------------MAIN VARIABLES-------------------------------------------------------------------------
tree = ET.parse('formulas.xml')  
root = tree.getroot()
items = []
lastVariables = []

#-------------------------------------------------------------------------FUNCTIONS-------------------------------------------------------------------------
def formula_search (doc, svar):
    return doc.findall('.//function[@name="' + svar + '"]...')

def list_variables (fnode, svar):
    list_var = {}
    for child in fnode.iter('var'):
        if (child.attrib.get("name") != svar):
            list_var[str(child.attrib.get("name"))] = 0
    return(list_var)

def get_equation (fnode, svar):
    equation_node = fnode.find('./function[@name="' + svar + '"]')
    return (equation_node.attrib.get('equation'))

def reset():
    all_widgets = main.grid_slaves()
    for widget in all_widgets:
        widget.destroy()
    createHistoryButton()
    removeMenuBtn()
    showVarList()

def reset_error_msg():
    all_widgets = main.grid_slaves()
    for widget in all_widgets:
        if(widget.config("text")[-1] == "Please enter a number"):
            widget.destroy()

def get_unit (fnode, svar):
    unit_node = fnode.find('./var[@name="' + svar + '"]')
    return (unit_node.attrib.get('unit'))

def showHistory():
    iterator=1
    Label(main, text="PREVIOUS ANSWERS", font="Consolas 10", bg="#c2d1e8").grid(row=0, column=20, padx=15)
    global lastVariables
    while(len(lastVariables) > 5):
        del(lastVariables[0])
    for i in lastVariables:
        Label(main, text=i, font="Consolas 10", bg="#c2d1e8").grid(row=iterator, column=20)
        iterator+=1
    all_widgets = main.grid_slaves()
    for widget in all_widgets:
        if(widget.config("text")[-1] == "Previous answers"):
            widget.destroy()

def get_attrib (fnode, attribute, stype, key):
    dict_attribute_var = {}
    for child in fnode.iter(stype):
        var_key = str(child.attrib.get(key))
        var_attribute = str(child.attrib.get(attribute))
        if(var_key not in dict_attribute_var):
            dict_attribute_var[var_key] = var_attribute
    return (dict_attribute_var)

nameToTxt = get_attrib(root, "text", "var", "name")
nameOfFunc = get_attrib(root, "name", "function", "name")
txtToName = get_attrib(root, "name", "var", "text")

def selectEquation(btnText, argVar):
    searched_variable = txtToName[argVar]
    items = formula_search(root, searched_variable)
    selected_equation = btnText[0]
    formula_node = items[int(selected_equation) - 1]
    lvar = list_variables(formula_node, searched_variable) 
    svar_unit = get_unit(formula_node, searched_variable)
    

    all_widgets = main.grid_slaves()
    for widget in all_widgets:
        widget.destroy()
    createHistoryButton()

    i = 0
    textBoxes = []
    for qvar in lvar.items():
        qvar_unit = get_unit(formula_node, qvar[0])
        Label(main, text = "Enter the value of " + nameToTxt[qvar[0]] + " in " + qvar_unit + " : ", font="Consolas 10", bg="#c2d1e8").grid(row=i)
        varBox = Entry(main, font="Consolas 10", borderwidth=3, relief="sunken")
        varBox.grid(row=i, column=1)
        textBoxes.append(varBox)
        i += 1 

    def show_answer():
        reset_error_msg()
        variables = []
        for textBox in textBoxes:
            variables.append(textBox.get())
        s_equation = get_equation(formula_node, searched_variable) 
        i2 = 0
        for qvar in lvar.items():
            lvar[qvar[0]] = variables[i2]
            i2 += 1
            if ("^" in lvar[qvar[0]]):
                lvar[qvar[0]] = lvar[qvar[0]].replace("^", "**")       
            if ("E" in lvar[qvar[0]]):
                lvar[qvar[0]] = lvar[qvar[0]].replace("E", "* 10**")
            s_equation = s_equation.replace(qvar[0], str(lvar[qvar[0]]))                 
           
        try: 
            ans = eval(s_equation)
            if(ans >= 10000 or ans < 0.001):
                s_answer = '%.2E' % Decimal(ans)
            else:
                s_answer = str(round(ans, 2))
            if(s_answer[-2:] == ".0"):
                    s_answer = s_answer[:-2]
            string_answer = nameToTxt[searched_variable] + " has a value of " + s_answer + svar_unit
            label_answer = Label(main, text=string_answer, font="Consolas 10", bg="#c2d1e8").grid(row=0, column=3)
            global lastVariables
            txtToAdd = nameToTxt[searched_variable] + " = " + s_answer + svar_unit
            lastVariables.append(txtToAdd)
        except:
            reset_error_msg()
            error = Label(main, text = "Please enter a number", fg="red", font="Consolas 10", bg="#c2d1e8").grid(row=0, column=3) 

    show_ans = Button(main, text='Show answer', command=show_answer, font="Consolas 10", borderwidth=3, relief="ridge").grid(row=i + 1, column=1, sticky=W, pady=4)

def get_formula(argVar):
    reset_error_msg()
    all_widgets = main.grid_slaves()
    for widget in all_widgets:
        widget.destroy()

    createHistoryButton()

    searched_variable = txtToName[argVar]
    items = formula_search(root, searched_variable)
    
    if(len(items) == 1):
        formula_node = items[0]
        svar_unit = get_unit(formula_node, searched_variable)
        lvar = list_variables(formula_node, searched_variable) 

        i = 0
        textBoxes = []
        for qvar in lvar.items():
            qvar_unit = get_unit(formula_node, qvar[0])
            Label(main, text = "Enter the value of " + nameToTxt[qvar[0]] + " in " + qvar_unit + " : ", font="Consolas 10", bg="#c2d1e8").grid(row=i)
            varBox = Entry(main, font="Consolas 10", borderwidth=3, relief="sunken")
            varBox.grid(row=i, column=1)
            textBoxes.append(varBox)
            i += 1   
        
        def show_answer():
            reset_error_msg()
            variables = []
            for textBox in textBoxes:
                variables.append(textBox.get())
            s_equation = get_equation(formula_node, searched_variable) 
            i2 = 0
            for qvar in lvar.items():
                lvar[qvar[0]] = variables[i2]
                i2 += 1
                if ("^" in lvar[qvar[0]]):
                    lvar[qvar[0]] = lvar[qvar[0]].replace("^", "**")       
                if ("E" in lvar[qvar[0]]):
                    lvar[qvar[0]] = lvar[qvar[0]].replace("E", "* 10**")
                s_equation = s_equation.replace(qvar[0], str(lvar[qvar[0]]))                 
            
            try: 
                ans = eval(s_equation)
                if(ans >= 10000 or ans < 0.001):
                   s_answer = '%.2E' % Decimal(ans)
                else:
                   s_answer = str(round(ans, 2))
                if(s_answer[-2:] == ".0"):
                    s_answer = s_answer[:-2]
                string_answer = nameToTxt[searched_variable] + " has a value of " + s_answer + svar_unit
                label_answer = Label(main, text=string_answer, font="Consolas 10", bg="#c2d1e8").grid(row=0, column=3)
                global lastVariables
                txtToAdd = nameToTxt[searched_variable] + " = " + s_answer + svar_unit
                lastVariables.append(txtToAdd)
            except:
                reset_error_msg()
                error = Label(main, text = "Please enter a number", fg="red", font="Consolas 10", bg="#c2d1e8").grid(row=0, column=3)
            
        show_ans = Button(main, text='Show answer', command=show_answer, font="Consolas 10", borderwidth=3, relief="ridge").grid(row=i + 1, column=1, sticky=W, pady=4)
    
    elif(len(items) > 1):
        Label(guide, text = "Good! Now choose the formula you want to use to find your variable.", font="Consolas 10", bg="#c2d1e8").grid(row=2, column=22)
        i3 = 0
        for i in range(0, len(items)):
            form = get_attrib(root, "text", "function", "equation")       
            s_equation = get_equation(items[i], searched_variable)
            s_equation = form[s_equation]
            text = str(i + 1) + " - " + s_equation
            equation = Button(main, text=text, command=lambda s=text: selectEquation(s, argVar), font="Consolas 10", borderwidth=3, relief="ridge", width=30)
            equation.grid(row=i3, column=1, sticky=W, pady=2)
            i3 += 1   

def showVarList():
    row = 0
    col = 0
    for key, value in nameOfFunc.items():             
        text = nameToTxt[key]
        equation = Button(main, text=text, command=lambda s=text: get_formula(s), font="Consolas 10", borderwidth=3, relief="ridge", height=1, width=10)
        equation.grid(row=row, column=col, sticky=W, pady=2, padx=2)
        if(col > 4):
            col = 0
            row += 1
        else:
            col += 1

def createHistoryButton():
    global lastVariables
    if(len(lastVariables) != 0):
        history = Button(main, text="Previous answers", command=showHistory, font="Consolas 10", borderwidth=3, relief="ridge").grid(row=0, column=20, sticky=W, padx=15)
        menu = Button(main, text="Main menu", command=reset, font="Consolas 10", borderwidth=3, relief="ridge").grid(row=0, column=21, sticky=W)
    else:
        menu = Button(main, text="Main menu", command=reset, font="Consolas 10", borderwidth=3, relief="ridge").grid(row=0, column=21, sticky=W, padx=15)

def removeMenuBtn():
    all_widgets = main.grid_slaves()
    for widget in all_widgets:
        if(widget.config("text")[-1] == "Main menu"):
             widget.destroy()

#----------------------------------------------------------------------CREATING THE GUI----------------------------------------------------------------------
main = Tk()
main.title("Super Formulas")
main.iconbitmap("icon.ico")

guide = Tk()
guide.title("Super Formulas - Guide")
guide.iconbitmap("icon.ico")

Label(guide, text = "Welcome to \"Super Formulas\"", font="Consolas 10 bold underline", bg="#c2d1e8").grid(row=0, column=22)
Label(guide, text = "This little program was made to help you study and do your homeworks faster.", font="Consolas 10", bg="#c2d1e8").grid(row=1, column=22)
Label(guide, text = "To begin, use the list to choose the variable you want to find.", font="Consolas 10", bg="#c2d1e8").grid(row=2, column=22)

showVarList()
createHistoryButton()
removeMenuBtn()

main.configure(background="#c2d1e8")
guide.configure(background="#c2d1e8")

mainloop()
