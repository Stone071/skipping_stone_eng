# This is going to be a brief exercise to generate all the LaTeX
# for my audio bandpass filter page
from sympy import *

# for general examples
a, b, c = symbols('a b c')
# for circuit transfer functions
R1, R2, C, s, V1, V_in, V_out, V2 = symbols('R1 R2 C s V1 V_in V_out V2')
# general form of transfer function
K, H, wn, zeta= symbols('K H omega_n zeta')
# For first order lowpass
Z_c = symbols('Z_c')
# For general first order 
H_o, F_o = symbols('H_o F_o')

def mathjax(inExpr, Equals=None):
    if Equals != None: return ("\\("+latex(inExpr)+" = "+latex(Equals)+"\\)")  
    else: return ("\\("+latex(inExpr)+"\\)")

def pWrap(inStr):
    return "<p>"+inStr+"</p>"

def h3Wrap(inStr):
    return "<h3>"+inStr+"</h3>"

def textExpr(inExpr):
    return pWrap(mathjax(inExpr))+"\n"

def textEq(inExpr, Equals):
    return pWrap(mathjax(inExpr, Equals))+"\n"

def textComment(inText):
    return pWrap(inText)+"\n"

def textHeading(inText):
    return h3Wrap(inText)+"\n"

def textBreak():
    return "\n\n"

with open("Bandpass_LaTeX.txt", 'w') as file:
    # expr = (1/a*b*c)
    # file.write(textComment("TESTING EXPR"))
    # file.write(textExpr(expr))

    file.write(textComment("<i>NOTE: Sympy python library likes to make its precedence clear through adding many layers of \
    parenthesis. While it's not the exact way I wrote these equations, the math is still correct.</i>"))
    
    ### THIS SECTION IS FOR THE MULTIPLE-FEEDBACK BANDPASS FILTER ###
    file.write(textHeading("Multiple Feedback Bandpass Filter"))
    file.write(textComment("Node Voltage Method"))
    with evaluate(False):
        file.write(textComment("Node 1, between R<sub>1</sub> and C"))
        expr = (V1-V_in)/R1 + (V1-V_out)/(1/(s*C)) + (V1)/(1/(s*C))
        file.write(textEq(expr, 0))
    
    with evaluate(False):
        expr = V1/R1 - V_in/R1 + V1*s*C - s*V_out*C + s*V1*C
        file.write(textEq(expr, 0))
    
    with evaluate(False):
        file.write(textComment("Node 2, at the inverting input"))
        expr = -(V_out/R2) -(V1/(1/s*C))
        file.write(textEq(expr, 0))
    
    with evaluate(False):
        expr = -(V_out/R2) -s*V1*C
        file.write(textEq(expr, 0))
    
    expr = -(V_out/R2) -s*V1*C
    expr = solve(expr, V1)
    file.write(textEq(expr, V1))
   
    with evaluate(False):
        file.write(textComment("Substituting Node 2 equation into Node 1 equation"))
        expr = -((V_out/(R2*s*C))/R1) - (V_in/R1) - (V_out*s*C)/(R2*s*C) - V_out*s*C - (V_out*s*C)/(R2*s*C)
        file.write(textEq(expr, 0))
    
    with evaluate(False):
        expr = -V_out/(R1*R2*s*C) - V_in/R1 - (2*V_out)/R2 - V_out*s*C
        file.write(textEq(expr, 0))

    with evaluate(False):
        expr = -V_out*((1/(R1*R2*s*C)) + (2/R2) + s*C)
        sol = (V_in)/R1
        file.write(textEq(expr, sol))

    with evaluate(False):
        expr = -V_out*((R1/(R1*R2*s*C)) + ((2*R1)/R2) + R1*s*C)
        sol = V_in
        file.write(textEq(expr, sol))

    with evaluate(False):
        expr = -V_out*(1/(R2*s*C) + (2*R1*s*C)/(R2*s*C) + (R1*R2*s**2*C**2)/(R2*s*C))
        sol = V_in
        file.write(textEq(expr, sol))

    with evaluate(False):
        file.write(textComment("Final Transfer Function"))
        expr = -(s*R2*C)/(s**2*C**2*R2*R1 + s*C*2*R1 + 1)
        sol = V_out/V_in
        file.write(textEq(expr, sol))

    with evaluate(False):
        file.write(textComment("2<sup>nd</sup> order transfer function general form"))
        expr = (K*wn**2)/(s**2+2*zeta*wn*s+wn**2)
        sol = H
        file.write(textEq(expr, sol))

    file.write(textComment("Placing the transfer function in the general form, we can relate the component values " \
        "to the characteristics of the second order system."))
    with evaluate(False):
        file.write(textComment("Fundamental Frequency"))
        expr = 1/(C*sqrt(R2*R1))
        sol = wn
        file.write(textEq(expr, sol))

    with evaluate(False):
        file.write(textComment("Damping Ratio"))
        expr = sqrt(R2*R1)/R2
        sol = zeta
        file.write(textEq(expr, sol))
    file.write(textBreak())
    ### THIS SECTION IS FOR THE MULTIPLE-FEEDBACK BANDPASS FILTER ###

    ### THIS SECTION IS FOR THE FIRST ORDER HIGHPASS FILTER ###
    file.write(textHeading("First Order Highpass Filter"))
    with evaluate(False):
        file.write(textComment("KCL at Inverting Input"))
        expr = -(V_in)/(Z_c+R1) - (V_out/R2)
        sol = 0
        file.write(textEq(expr, sol))

    with evaluate(False):
        expr = -(V_in*R2)/(Z_c+R1)
        sol = V_out
        file.write(textEq(expr, sol))

    with evaluate(False):
        expr = -(V_in*R2)/((1/(s*C))+R1)
        sol = V_out
        file.write(textEq(expr, sol))

    with evaluate(False):
        expr = -(R2*s*C)/(R1*s*C+1)
        sol = V_out/V_in
        file.write(textEq(expr, sol))

    with evaluate(False):
        expr = -(R2/R1)*((s*C)/(s*C + (1/R1)))
        sol = V_out/V_in
        file.write(textEq(expr, sol))
    
    with evaluate(False):
        file.write(textComment("Final Transfer Function"))
        expr = -(R2/R1)*((s*C*R1)/(s*C*R1 + 1))
        sol = V_out/V_in
        file.write(textEq(expr, sol))

    with evaluate(False):
        file.write(textComment("Looking at the transfer function, we can determine the system characteristics " \
        "in terms of the circuit components."))
        expr = -(R2/R1)*((s*C*R1)/(s*C*R1 + 1))
        sol = V_out/V_in
        file.write(textEq(expr, sol))

    with evaluate(False):
        file.write(textComment("Passband Gain"))
        expr = -(R2/R1)
        sol = H_o
        file.write(textEq(expr, sol))
    
    with evaluate(False):
        file.write(textComment("Cut-off Frequency (pole location)"))
        expr = 1/(2*pi*R1*C)
        sol = F_o
        file.write(textEq(expr, sol))
    file.write(textBreak())
    ### THIS SECTION IS FOR THE FIRST ORDER HIGHPASS FILTER ###

    ### THIS SECTION IS FOR THE FIRST ORDER LOWPASS FILTER ###
    file.write(textHeading("First Order Lowpass Filter"))
    with evaluate(False):
        file.write(textComment("KCL at Inverting Input"))
        expr = -(V_in)/R1 - (V_out)/((R2*Z_c)/(R2+Z_c))
        sol = 0
        file.write(textEq(expr, sol))

    with evaluate(False):
        expr = (V_out)/((R2*Z_c)/(R2+Z_c))
        sol = -(V_in/R1)
        file.write(textEq(expr, sol))

    with evaluate(False):
        expr = (V_out*(R2+Z_c))/(R2*Z_c)
        sol = -(V_in/R1)
        file.write(textEq(expr, sol))

    with evaluate(False):
        expr = -(R1*(R2+Z_c))/(R2*Z_c)
        sol = (V_in/V_out)
        file.write(textEq(expr, sol))

    with evaluate(False):
        expr = -(R1*(R2+(1/(s*C))))/(R2/(s*C))
        sol = (V_in/V_out)
        file.write(textEq(expr, sol))

    with evaluate(False):
        expr = -(R2*R1*s*C+R1)/(R2)
        sol = (V_in/V_out)
        file.write(textEq(expr, sol))

    with evaluate(False):
        expr = -(R1/R2)*((R2*s*C+1)/1)
        sol = (V_in/V_out)
        file.write(textEq(expr, sol))

    file.write(textComment("Final Transfer Function"))
    with evaluate(False):
        expr = -(R2/R1)*(1/(s*R2*C+1))
        sol = V_out/V_in
        file.write(textEq(expr, sol))

    file.write(textComment("System characteristics in terms of circuit components"))
    with evaluate(False):
        file.write(textComment("Passband Gain"))
        expr = -(R2/R1)
        sol = H_o
        file.write(textEq(expr, sol))
    
    with evaluate(False):
        file.write(textComment("Cut-off Frequency (pole location)"))
        expr = 1/(2*pi*R2*C)
        sol = F_o
        file.write(textEq(expr, sol))
    file.write(textBreak())
    ### THIS SECTION IS FOR THE FIRST ORDER LOWPASS FILTER ###
    