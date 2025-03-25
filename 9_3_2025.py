# Khởi tạo các biến và list
digitlist = [] # Mảng chứa chính để xử lý thuật toán
operatorlist = [] # Mảng chứa dấu
calculate = []
resultlist = [] # Lưu các kết quả sau khi tìm x
expression_2 = 0

#---------------------------------------------------------
# Các hàm xử lý biểu thức (tách, kiểm tra, tính toán)
#---------------------------------------------------------
# Hàm kiểm tra có phải là 1 số không
def is_number(s): 
    try:
        float(s) 
        return True
    except ValueError:
        return False

# Hàm tách biểu thức thành các phần phần tử thành 1 list
def devide_and_check_number(equation):
    numlist = [ ]
    num = ""
    for digit in equation:
        #print(digit)
        if (digit.isdigit()):  
            num = num + digit
        else:
            numlist.append(num)
            numlist.append(digit)
            num = ""
    if(num):
        numlist.append(num)
        #print(numlist)
    return numlist

    # Kiểm tra số âm và số thập phân có trong list không
def check_negative_and_decimal(numlist):    
    temp = [ ]
    index = 0 
    #print("len(numlist) là >>", len(numlist))
    last_index = len(numlist) - 1
    while (index < len(numlist)):
        #print('') # Khoảng trắng
        #print('\nVị trí index trong vòng này là >>', index, ',' ' Ứng với ký tự >> ',numlist[index])
        if (numlist[index] == '-'): # Kiểm tra ký tự là dấu âm hay dấu trừ
            if (index == 0 or numlist[index-1] in "+-*/^()"): # Xử lý số âm
                if (numlist[index+2] == '.'):
                    temp.append(numlist[index] + numlist[index+1] + numlist[index+2]+ numlist[index+3]) 
                    index += 4                   
                else:
                    temp.append(numlist[index] + numlist[index+1])
                    index += 2
            else:
                temp.append(numlist[index])
                index += 1               
        elif (numlist[index] == ''): # kiểm tra nếu là khoảng trống thì xóa
            del numlist[index]                              
        elif (numlist[index].isdigit() and index + 1 < len(numlist) and numlist[index+1] == '.'): # Xử lý số thập phân                   
            if (((index+1) == last_index) and ((index) > 0)):
                temp.append(numlist[index] + numlist[last_index])
                break
            elif (((index+2) == last_index) and ((index) > 0)):
                temp.append(numlist[index] + numlist[index+1] + numlist[last_index])
                break
            else:
                temp.append(numlist[index] + numlist[index+1] + numlist[index+2])
                index +=3          
        else: # Các ký tự bình thường thì thêm vào mảng theo thứ tự
            temp.append(numlist[index])
            index += 1                  
    numlist = temp                 
    #print(numlist)
    return numlist

# Xử lý theo thuật toán Shunting Yard 
def shunting_yard_algorithm(numlist):
    priority = {"+":1, "-":1, "*":2, "/":2, "^":3}
    digitlist = []
    for digit in numlist:
            if (digit.isdigit()):  
                digitlist.append(digit)  
                continue
            if (is_number(digit)):
                digitlist.append(digit)
                continue
            elif (digit in priority):  
                while (operatorlist and operatorlist[-1] != '(' and priority.get(operatorlist[-1], 0) >= priority[digit] and digit != '^'):  
                    digitlist.append(operatorlist.pop())  # Đưa dấu có độ ưu tiên cao hơn vào digitlist
                operatorlist.append(digit)  
            elif (digit == "("):
                operatorlist.append(digit)  
            elif (digit == ")"):  
                while operatorlist and operatorlist[-1] != '(':
                    digitlist.append(operatorlist.pop())  
                operatorlist.pop()  
    while operatorlist:
        digitlist.append(operatorlist.pop())  # Đưa toàn bộ dấu còn lại vào mảng digitlist   
    return digitlist

# Hàm tính toán cộng trừ nhân chia số mũ cơ bản:
def solve_equation(digitlist):
    result = 0
    digit = ""
    c =""
    temp = []
    calculate = []
    value = 0
    while value < len(digitlist):
        if(len(digitlist) == 1):
            #digitlist = []
            break
        for digit in (digitlist):
        #digit = digitlist[value]
            if (isinstance(digit, str)) and (digit.isdigit()):
                #value += 1
                digit = float(digit)
                continue  
            if (is_number(digit)):
                continue      
            else:
                i = digitlist.index(digit)
                start = max((i-2), 0) 
                position = int(i-2)
                calculate = digitlist[start:(i+1)]
                temp.extend(calculate)
                del digitlist[start:(i+1)]
                # break
            # Phép tính với 2 số            
            try:
                if (temp[-1] == "+"):
                    a = float(temp[0])
                    b = float(temp[1])
                    c = a + b
                elif (temp[-1] == "-"):
                    a = float(temp[0])
                    b = float(temp[1])
                    c = a - b
                elif (temp[-1] == "*"):
                    a = float(temp[0])
                    b = float(temp[1])
                    c = a * b
                elif (temp[-1] == "/"):
                    a = float(temp[0])
                    b = float(temp[1])
                    #try:
                    c = a / b
                    #except ZeroDivisionError:
                        #print("Lỗi chia cho 0 !")
                elif (temp[-1] == "^"):
                    a = float(temp[0])
                    b = float(temp[1])
                    c = a ** b 
            except ValueError:
                break  
            # Thêm kết quả vừa tính vào list digitlist và reset lại cái biến
            digitlist.insert((position), c)   
            #i = 0
            #value = 0
            calculate = [ ]
            temp = [ ]        
            a = b = c = ""
            if(len(digitlist) == 1):
                #print("Hoàn thành tính toán !")
                value = digitlist[-1]
            else:
                break
            result = digitlist[-1]           
            break
    if (len(digitlist) > 1):
        print("Lỗi phép tính !")
        result = None
    #digitlist = []
    return round(result, 9) # Làm tròn kết quả với 10 chữ số thập phân
    #return result

#---------------------------------------------------------
# Phần chính để giải phương trình
#---------------------------------------------------------
# Giải biểu thức ra kết quả với 1 giá trị x bất kì:
def solve_equation_with_x(expression, x):
    temp_expression = []
    temp_expression = expression
    if "=" in expression:
        i = expression.find("=")
        temp_expression = temp_expression[:i] + "-(" + temp_expression[i+1:] + ")"
    temp_expression = temp_expression.replace('x', str(x))
    # Đặt 1 tên biến để đỡ rối :)))
    temp_expression = devide_and_check_number(temp_expression)
    #print('Sau khi tách thành list:\n',temp_expression)             ########################################################################################
    temp_expression = check_negative_and_decimal(temp_expression)
    #print('Sau khi check số âm và số thập phân:\n',temp_expression) ########################################################################################
    temp_expression = shunting_yard_algorithm(temp_expression) 
    #print('Sau khi sắp sếp các phần tử theo thuật toán Shunting Yard:\n',temp_expression) ##################################################################
    result = solve_equation(temp_expression)
    return result

# Tính đạo hàm của biểu thức với 1 x bất kì:
def derivative(expression, x, delta = 0.0001): 
    a = solve_equation_with_x(expression, x+delta)
    b = solve_equation_with_x(expression, x)
    c = (a - b)/delta
    return c

# Hàm xuất ra 1 kết quả khi thế 1 x bất kì vào biểu thức:
def solve_simple_equation(expression):
    error = 0.0000000000001
    index_loop = 0    
    x = 0.5   
    temp_result = 1 
    c = None
    result_x = 0  
    while (abs(temp_result) > error): # Khi nào sai số gần bằng 0 thì out ra khỏi loop
            a = solve_equation_with_x(expression, x)
            b = derivative(expression, x, delta=0.0001)
            if (b == 0): 
                x = None
                break
            try:
                c = a/b
                x = x - c 
            except ZeroDivisionError: # Trường hợp chia cho 0
                break           
            try:
               temp_result = solve_equation_with_x(expression, x)        
            except ZeroDivisionError: # Trường hợp chia cho 0
                break 
            index_loop += 1
            if (index_loop >= 10000 and abs(round(x, 2)) != 0):
                x = 9999
                break
            if (index_loop >= 10000 and abs(round(x, 2)) == 0):
                x = 0
                break    
    if (x != None and x != 9999):  # Trường hợp có nghiệm
        result_x = round(x, 4)  
        return result_x # Trả về nghiệm x
    elif (x == 9999):
        result_x = ' Phương trình vô nghiệm !'
        return result_x
    elif (index_loop >= 10000 and abs(round(x, 1)) == 0):
        result_x = 0
        return result_x
    else:
        return None

# Tạo phương trình tính mới để tính nghiệm thứ n và kiểm tra phương trình vừa tạo có bằng 1 không:
def new_equation(expression, resultlist):
    temp_new = ''
    digit = ''
    #error = 0.00000001
    for digit in resultlist:
        temp_new += f"*(x-{digit})" #(x-xn)
    expresion_2 = f" ({expression}) / ({temp_new[1:]}) " # (f(x)/((x-x1)*(x-x2)*(x-x3)*...*(x-xn)))
    try:
        temp_result = solve_equation_with_x(expresion_2, 0.5)
    except ZeroDivisionError: # Nếu chia cho số 0
        return None
    if (temp_result == 1):
        return None
    else: 
        return expresion_2
    
# Thực hiện khử dấu '=' (chuyển vế đổi dấu):
def change_expression(expression):
    change_expression = '' 
    if "=" in expression:
        i = expression.find("=")
        change_expression = expression[:i] + "-(" + expression[i+1:] + ")"
    return  change_expression  

# Tìm nghiệm của phương trình vừa tạo:
def solve_new_equation(expression_2):
    temp_resultlist = []
    result_x = 0
    change = change_expression(expression)
    #index_solve = 0
    while True:
        #index_solve += 1                  #############              
        #print('Lần thứ >>', index_solve)  #############
        result_x = solve_simple_equation(expression_2)
        if (result_x == None):
            break
        elif (result_x == ' Phương trình vô nghiệm !'):
            break
        else:
            temp_resultlist.append(result_x)
            expression_2 = new_equation(change, temp_resultlist)
        if (expression_2 == None):
            break
    resultlist = temp_resultlist
    if (resultlist == []):
        resultlist = 'Phương trình vô nghiệm !'
    temp_resultlist = []
    return resultlist

# Kiểm tra phép tính bình thường hay phép tính có chứa x:
def check_expression(expression):
    if 'x' in expression:
        return 1
    else:
        return 0  
       
#---------------------------------------------------------   
# Phần nhập chương trình:
#---------------------------------------------------------
while True:
    expression = input('Mời nhập biểu thức >> ')
    check = check_expression(expression)
    if (check == 0):
        result = solve_equation_with_x(expression, 0.5)
        print('Kết quả của phép tính là >>',result)
    else:
        result = solve_new_equation(expression) 
        if (result == 'Phương trình vô nghiệm !'):
            print(result)
        else:
            print('Kết quả của phép tính là >> x =',result)