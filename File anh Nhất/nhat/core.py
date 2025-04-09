import numpy as np

symbol = ["+", "-", "*", "/", "^"]
variable = ["x", "y", "z"]
ans = 0
preAns = 0

# Class get string
def getKey():
    pass

def getStr():
    formula = input("Enter: ")
    return formula


# Class formula
def formulaPreProcess(string):
    # delete space
    formula = ""
    for i in range(len(string)):
        if string[i] != " ":
            formula += string[i]

    isSolve = 0 # Check if solve equation or normal calculation
    # convert to lhs f(x) = 0
    for i in range(len(formula)):
        if formula[i] == "=":
            formula = formula[:i] + "-(" + formula[i+1:] + ")"
            isSolve = 1
            break
    return isSolve, formula # return trả về loại biểu thức nào và biểu thức dùng để tính toán

def formulaProcess(formula, x):
    #Calculate subformula
    subFormula = 0
    temp = 0
    for i in range(len(formula)):
        if formula[i] == "(":
            subFormula += 1
        if formula[i] == ")":
            temp += 1
    if subFormula != temp: # check amount of lèt parenthesis '(' equal right pảenthesis ')'
        return 0 #Kiểm tra số lượng mở ngoặc và đóng ngoặc có bằng nhau không
    
    for _ in range(subFormula): #loop until no sub-formula left
        startSub = 0
        endSub = 0
        for i in range(len(formula)): # find the first right parenthesis ')' index
            if formula[i] == ")": 
                endSub = i
                break
        for i in range(endSub+1): # from first right parenthesis ')' index loop back find left parenthesis '('
            if formula[endSub-i] == "(": 
                startSub = endSub-i
                break

        # Tính biểu thức trong dấu ngoặc trước
        sub_res = calFormula(formula[startSub+1: endSub], x) #Calculate value sub-formula
        
        # Tạo biểu thức mới với các giá trị vừa tính trong ngoặc
        formula = formula[:startSub] + f'{sub_res:.7f}' + formula[endSub+1:] #Create new formula string, replace subformula with calculated value
    
    # Tính tất cả các phép tính sau khi tạo biểu thức mới =>> Kết quả cuối cùng của biểu thức
    return calFormula(formula, x) #return

def calFormula(string, x):
    # Make string formula to array -> ez to calculate
    numArr = [] # Array store all value in formula
    opArr = [] # Array store all operator
    j = 0 # start number pointer
    mulfactor = 1 # factor for negative number case Ex: +-1
    for i in range(len(string)):
        if string[i] in symbol: # Mảng chứa các toán tử + - * / ^
            if i-j == 0: # Case -a+b or b+-a
                if string[i]=='+': 
                    numArr.append(0)
                    j = i+1
                    opArr.append('+')
                elif string[i]=='-':
                    mulfactor = -1
                else: raise ValueError('Error equation!')

            elif string[i-1] in variable: # Case variable x y z
                numArr.append(mulfactor*x)
                mulfactor = 1
                j = i+1
                opArr.append(string[i])

            else:
                numArr.append(float(string[j:i])) # Case normal number
                j = i+1
                opArr.append(string[i])

        # Last number
        if i == len(string)-1:
            if string[j] in variable:
                numArr.append(mulfactor*x)
            else:
                numArr.append(float(string[j:]))

    # Calculate from the array
    for i, eq in enumerate(opArr): # Calculate the power first
        if eq == '^':
            numArr[i+1] = pow(numArr[i], numArr[i+1])
            numArr[i] = 1
            opArr[i] = '*'
    
    for i, eq in enumerate(opArr): # Process the formula from right to left
        # convert to sumable array by process all multiply and divide and negative number
        if eq == '-':
            numArr[i+1] = numArr[i+1]*-1
        elif eq == '*':
            numArr[i+1] = numArr[i]*numArr[i+1]
            numArr[i] = 0
        elif eq == '/':
            numArr[i+1] = numArr[i]/numArr[i+1]
            numArr[i] = 0
    
    return sum(numArr)

# dẻivative dx = (f(x+delta)-f(x))/delta with small delta
def derivative(formula, x, delta=0.001): 
    return (formulaProcess(formula, x+delta) - formulaProcess(formula, x))/delta

#Newton method x_new = x - f(x)/f'(x)
def solve(formula, x=0.5, maxtries=100000, maxerr=0.00001): # do 100k loop until error < 10e-5
    for _ in range(maxtries):
        err = formulaProcess(formula, x)
        if abs(err) < maxerr:
            return x
        x -= err/derivative(formula, x)

    raise ValueError('no solution found') #else not found solution

#Use divide polyminal law after find solution x1 we solve equation f(x)/(x-x1)=0 to find x2 and so on to xn
def solveFull(formula):
    xf = []
    for _ in range(100):
        if len(xf) == 0: temp = '1'
        else:
            temp = '(1*'
            for x in xf:
                temp += '(x-'+f'{x:.7f}'+')'
            temp += ')'
        formula = '(' + formula + ')/' + temp
        try:
            ans = solve(formula)
            xf.append(ans)
        except:
            return xf
    return xf

# System of equations
def sysEqua(arr2D, resArr):
    # x0 + 2 * x1 = 1 and 3 * x0 + 5 * x1 = 2
    # a = np.array([[1, 2], [3, 5]])
    # b = np.array([1, 2])
    # x = np.linalg.solve(a, b)
    return np.linalg.solve(arr2D, resArr)

# # Main loop
# while True:
#     text = getStr()
#     preAns = ans
#     isSolve, formula = formulaPreProcess(text)
#     if isSolve == 0:
#         ans = formulaProcess(text, ans)
#     else:
#         ans = solve(formula)
#         xf = solveFull(formula)
#         print(xf)
#     print(ans)
#     # print(calSubFormula(text, 2))