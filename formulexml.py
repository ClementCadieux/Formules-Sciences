from xml.etree import ElementTree as ET

course = input("""What course are you doing right now? 
1-Science
2-Math""")

if (course == "1"):
    tree = ET.parse('sciences_formulas.xml')
elif (course == "2"):
    tree = ET.parse('math_formulas.xml')

root = tree.getroot()

import re

import math

from decimal import Decimal

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

def get_unit (fnode, svar):
    unit_node = fnode.find('./var[@name="' + svar + '"]')
    return (unit_node.attrib.get('unit'))

def get_attrib (fnode, attribute, stype, key):
    dict_attribute_var = {}
    for child in fnode.iter(stype):
        var_key = str(child.attrib.get(key))
        var_attribute = str(child.attrib.get(attribute))
        if(var_key not in dict_attribute_var):
            dict_attribute_var[var_key] = var_attribute
    return (dict_attribute_var)

def print_answer(answer, sunit, svar):
    if(abs(answer) >= 10000 or abs(answer) < 0.005):
        s_answer = '%.2E' % Decimal(answer)
    else:
        s_answer = str(round(answer, 2))

    s_response = svar + " has a value of " + s_answer
    if (sunit != ""):
        s_response = s_response + sunit

    return(s_response + ".")

#---------------------------------------------------------------

items = []
formula_node = 0

while (formula_node == 0):
    searched_variable = input("What are you searching?")
    items = formula_search(root, searched_variable)
    if (len(items) == 0):
        print("We don't have that variable")
    elif(len(items) == 1):
        formula_node = items[0]
    elif(len(items) > 1):
        for i in range(0, len(items)):
            s_equation = get_equation(items[i], searched_variable)
            print(str(i) + " " + s_equation)
        selected_equation = input("Which formula do you want? 0 - " + str(len(items) - 1))
        formula_node = items[int(selected_equation)]
                

lvar = list_variables(formula_node, searched_variable)
s_equation = get_equation(formula_node, searched_variable)
svar_unit = get_unit(formula_node, searched_variable)
avar = get_attrib(root, "name", "var", "name")
tvar = get_attrib(root, "text", "var", "name")
text_to_name = get_attrib(root, "name", "var", "text")

#((?<=[^a-zA-Z])|^)a(?=[^a-zA-Z$]|$)

sOp1 = r"((?<=[^a-zA-Z])|^)"
sOp2 = r"(?=[^a-zA-Z$]|$)"

for qvar in lvar.items():
    qvar_unit = get_unit(formula_node, qvar[0])
    s_question = "What is the value of " + qvar[0]
    if (qvar_unit != ""):
        s_question = s_question + " in " + qvar_unit
    lvar[qvar[0]] = input(s_question + "?")
    if ("^" in lvar[qvar[0]]):
        lvar[qvar[0]] = lvar[qvar[0]].replace("^", "**")       
    if ("E" in lvar[qvar[0]]):
        lvar[qvar[0]] = lvar[qvar[0]].replace("E", "* 10**")
    regex = sOp1 + qvar[0] + sOp2
    #s_equation = s_equation.replace(qvar[0], str(lvar[qvar[0]]))
    s_equation = re.sub(regex, str(lvar[qvar[0]]), s_equation)

try:
    if ("±" not in s_equation):
        answer = eval(s_equation)
        print (print_answer(answer, svar_unit, searched_variable))
    elif ("±" in s_equation):
        print(s_equation.replace("±", "+"))
        answer1 = eval(s_equation.replace("±", "+"))
        answer2 = eval(s_equation.replace("±", "-"))
        print (print_answer(answer1, svar_unit, searched_variable))
        if (answer1 != answer2):
            print(print_answer(answer2, svar_unit, searched_variable))
except(ValueError):
    print("There is no possible value to the equation.")