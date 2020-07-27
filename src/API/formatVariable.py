# Replaces triple, double and single whitespaces with underscore
import re


def formatVariable(variable):
    variable = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", variable)
    variable = variable.replace("   ", "  ")
    variable = variable.replace("  ", " ")
    variable = variable.replace(" ", "_")
    variable = variable.lower()
    return variable
