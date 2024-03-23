import pyperclip

inpTxtL = []

def replaceArray(txt):
    i = 0
    pos0 = ''
    pos1 = ''
    for j in range(len(txt)):
        if txt[j] == '[':
            i += 1
            if i == 4:
                pos0 = j
        if pos0 != '' and txt[j] == ']':
            pos1 = j
            break
    
    txtMod = txt[0:pos0] + '[0, 0, 0, 0]' + txt[pos1+1:]
    return txtMod
    
inpTxt = 0
while True:
    inpTxt = str(input())
    if inpTxt == '':
        break
    inpTxt = replaceArray(inpTxt)
    inpTxtL.append(inpTxt)

outTxt = ''

for i in inpTxtL:
    outTxt += i + '\n'

pyperclip.copy(outTxt)