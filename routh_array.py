import sympy as sym
from fractions import Fraction

def main():
    done = False 
    k = sym.Symbol('k')
    # k = Fraction(0)
    coef = [1,k+7,4*k,8*k]
    # coef = [1,15,-50,2,0.1]
    matrix = routh_array(coef) 
     
    
    if len(matrix) != len(coef):
        print("Original Array:")
        print_matrix(matrix) 
        s = sym.Symbol('s')
        print(s**2*matrix[-2][0]+matrix[-2][1])
        print("Pole Crossing located at: " 
                + str(sym.solve(s**2*matrix[-2][0]+matrix[-2][1])))

        print("\nReversed Array to check stability:")
        matrix = routh_array(coef[::-1])

    print_matrix(matrix)
    stable = check_stability(matrix) 
    if stable is True and len(matrix) is len(coef):
        print("System is Stable")

def first_layers(coef):
    a = coef[::2]
    b = coef[1::2] 
    b += [0]*(len(a)-len(b))
    return [a,b]

def routh_array(coef):
    lines = first_layers(coef) 
    for i in range(len(coef)-2):
        new_line  = []
        new_value = [0]*len(lines[0])
        for j in range(1,len(lines[0])):
            new_value[j-1] = (find_next([lines[-2][0],lines[-2][j]],
                                [lines[-1][0],lines[-1][j]]))
            if new_value[j-1] is 'nan':
                return lines 
        lines += [new_value]
    return lines

def find_next(a,b):
    if b[0] == 0:
        return 'nan'
    try:
       terms = Fraction(b[0]*a[1]/b[0]).limit_denominator()
    except TypeError:
       terms = b[0]*a[1]/b[0]
    try:
       terms -= Fraction(a[0]*b[1]/b[0]).limit_denominator()
    except TypeError:
       terms -= a[0]*b[1]/b[0]
    return terms 

def print_matrix(lines):
    # get largest term length for each column
    col_max = [1]*len(lines[0])
    for line in lines:
        for i,term in enumerate(line):
            col_max[i] = max(col_max[i],len(str(term)))

    # match the column width to the largest term and center 
    for line in lines:
        print(end="[ ")
        for i,term in enumerate(line[:-1]):
            print(str(term).center(int(col_max[i])),end=" , ")
        print(str(line[-1]).center(int(col_max[i]))+" ]")
    print(end="\n")

def check_stability(lines):
    k_values = []
    k_ranges = []
    for line in lines:
        try:
            if line[0] < 0:
                print("System not stable")
                return False

        except TypeError:
            k_ranges.append(sym.solve(line[0]>0))
            k_values.append(sym.solve(line[0]))
            
    if len(k_values) is 0:
        return True

    else:
        print("Decision Boundaries: ")
        for value in sum(k_values,[]):
            print(Fraction(float(value)).limit_denominator(),end=" ")
        print(end="\n")
        for k_range in k_ranges:
            print(k_range)
        
    return sum(k_values,[])


if __name__ == '__main__':
  main()
