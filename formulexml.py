from xml.etree import ElementTree as ET
tree = ET.parse('formulas.xml')
root = tree.getroot()


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

def get_attrib (fnode, attribute, stype):
    dict_attribute_var = {}
    for child in fnode.iter(stype):
        var_name = str(child.attrib.get("name"))
        var_attribute = str(child.attrib.get(attribute))
        if(var_name not in dict_attribute_var):
            dict_attribute_var[var_name] = var_attribute
    return dict_attribute_var

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
avar = get_attrib(root, "name", "var")
tvar = get_attrib(root, "text", "var")
tequation = get_attrib(root, "text", "function")

for qvar in lvar.items():
    qvar_unit = get_unit(formula_node, qvar[0])
    lvar[qvar[0]] = float(input("What is the value of " + qvar[0] + " in " + qvar_unit + "?"))
    s_equation = s_equation.replace(qvar[0], str(lvar[qvar[0]]))

print(avar)
print(tvar)
print(tequation)

answer = eval(s_equation)

if(answer >= 10000 or answer < 0.001):
    s_answer = '%.2E' % Decimal(answer)
else:
    s_answer = str(round(answer, 2))

print(searched_variable + " has a value of " + s_answer + " " + svar_unit + ".")
