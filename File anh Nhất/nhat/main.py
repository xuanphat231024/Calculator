from core import *
from keypad import *
from display import *

layoutid = 0
fomula_text = ''
fomula_text_start_pointer = 0
fomula_text_pointer = 0
max_size_text = 17
LINE = '-----------------------------------'
updateLCD(disp, ['', LINE, fomula_text, LINE, '', '', '', '', 'layout:' + str(layoutid)])
while True:
    key = getKey(layoutid)
    if (key!=None):
        if key == 'shift':
            layoutid = (layoutid + 1) % 2
            updateLCD(disp, ['', LINE, fomula_text[:fomula_text_pointer] + '|' + fomula_text[fomula_text_pointer:], LINE, '', '', '', '', 'layout:' + str(layoutid)])
            time.sleep(0.1)
        elif key == 'solve':
            isSolve, formula = formulaPreProcess(fomula_text)
            if isSolve == 0:
                ans = formulaProcess(formula, ans)
            else:
                ans = solve(formula)
            updateLCD(disp, ['', LINE, fomula_text, LINE, str(round(ans,5))])
            print(ans)
            fomula_text_start_pointer = 0
            fomula_text_pointer = 0
            fomula_text = ''
        elif key == 'solvea':
            isSolve, formula = formulaPreProcess(fomula_text)
            if isSolve == 0:
                ans = formulaProcess(formula, ans)
                updateLCD(disp, ['', LINE, fomula_text, LINE, str(round(ans,5))])
                print(ans)
            else:
                temp = ['', LINE, fomula_text, LINE]
                xf = solveFull(formula)
                print(xf)
                for i, x in enumerate(xf):
                    temp.append('x' + str(i+1) + '= ' + str(round(x,5)))
                updateLCD(disp, temp)
            fomula_text_start_pointer = 0
            fomula_text_pointer = 0    
            fomula_text = ''
        elif key == 'clr':
            fomula_text_start_pointer = 0
            fomula_text_pointer = 0    
            fomula_text = ''
            updateLCD(disp, ['', LINE, fomula_text, LINE, '', '', '', '', 'layout:' + str(layoutid)])
        elif key == 'del':
            if fomula_text_pointer > 1:
                fomula_text = fomula_text[:fomula_text_pointer-1] + fomula_text[fomula_text_pointer:]
                fomula_text_pointer -= 1
                updateLCD(disp, ['', LINE, fomula_text[:fomula_text_pointer] + '|' + fomula_text[fomula_text_pointer:], LINE, '', '', '', '', 'layout:' + str(layoutid)])
        elif key == '>':
            if fomula_text_pointer < len(fomula_text):
                fomula_text_pointer += 1
                updateLCD(disp, ['', LINE, fomula_text[:fomula_text_pointer] + '|' + fomula_text[fomula_text_pointer:], LINE, '', '', '', '', 'layout:' + str(layoutid)])
        elif key == '<':
            if fomula_text_pointer > 1:
                fomula_text_pointer -= 1
                updateLCD(disp, ['', LINE, fomula_text[:fomula_text_pointer] + '|' + fomula_text[fomula_text_pointer:], LINE, '', '', '', '', 'layout:' + str(layoutid)])
        else:
            fomula_text += key
            fomula_text_pointer += 1
            if fomula_text_pointer - fomula_text_start_pointer > max_size_text:
                fomula_text_start_pointer = fomula_text_pointer - max_size_text
            updateLCD(disp, ['', LINE, fomula_text[:fomula_text_pointer] + '|' + fomula_text[fomula_text_pointer:], LINE, '', '', '', '', 'layout:' + str(layoutid)])
            