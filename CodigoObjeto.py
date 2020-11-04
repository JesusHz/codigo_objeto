entrada = open("codigo4.txt","r")
lineas = entrada.readlines()
auxLineas = []
dictValues = dict()

inicio = []
data = []
code = []

code.append("\n")
code.append(".CODE")

inicio.append("org 100h")
inicio.append("include \"emu8086.inc\"")
inicio.append("DEFINE_PRINT_STRING")
inicio.append("DEFINE_PRINT_NUM")
inicio.append("DEFINE_PRINT_NUM_UNS")
inicio.append("DEFINE_SCAN_NUM")
inicio.append("")
inicio.append("suma MACRO x,y")
inicio.append("    mov ax,x")
inicio.append("    mov cx,y")
inicio.append("    add ax,cx")
inicio.append("    mov x,ax")
inicio.append("ENDM")
inicio.append("")
inicio.append("resta MACRO x,y")
inicio.append("    mov ax,x")
inicio.append("    mov cx,y")
inicio.append("    sub ax,cx")
inicio.append("    mov x,ax")
inicio.append("ENDM")
inicio.append("")
inicio.append("multi MACRO x,y")
inicio.append("    mov ax,x")
inicio.append("    mov bx,y")
inicio.append("    mul bx")
inicio.append("    mov x,ax")
inicio.append("ENDM")
inicio.append("")
inicio.append("division MACRO x,y")
inicio.append("    mov ax,y")
inicio.append("    mov bx,ax")
inicio.append("    mov ax,x")
inicio.append("    xor dx,dx")
inicio.append("    Div cx")
inicio.append("    mov x,ax")
inicio.append("ENDM")
inicio.append("")
inicio.append(".MODEL")
inicio.append(".STACK 2000")
inicio.append(".DATA")
inicio.append("saltoLN db 0D,0AH,'$'")



print("Tabla de Cuadruples")
print("-----------------------------")

for j in lineas:
    j = j.strip("\n")
    op,arg1,arg2,res = j.split()
    print(op,arg1,arg2,res)
    auxLineas.append(op+" "+arg1+" "+arg2+" "+res)

print("\n")

for i in range(0,len(inicio)):
    print(inicio[i])


contadorMsg = -1
contadorVar = -1
for i in lineas:
    i = i.strip("\n")
    op,arg1,arg2,res = i.split()
    auxRes = res
    auxArg1 = arg1
    if (op in "+"):
        if (res[:1] == "t"):
            data.append(str(res)+" dw 0")
        code.append("\n")
        code.append("suma "+str(arg1)+","+str(arg2))
        code.append("mov "+str(res)+",ax")
    elif (op in "-"):
        if (res[:1] == "t"):
            data.append(str(res)+" dw 0")
        code.append("\n")
        code.append("resta "+str(arg1)+","+str(arg2))
        code.append("mov "+str(res)+",ax")
    elif (op in "/"):
        if (res[:1] == "t"):
            data.append(str(res)+" dw 0")
        code.append("\n")
        code.append("division "+str(arg1)+","+str(arg2))
        code.append("mov "+str(res)+",ax")
    elif (op in "*"):
        if (res[:1] == "t"):
            data.append(str(res)+" dw 0")
        code.append("\n")
        code.append("multi "+str(arg1)+","+str(arg2))
        code.append("mov "+str(res)+",ax")
    elif (auxRes[:5] == "print" and auxArg1[:1] == "\""):
        contadorMsg = contadorMsg + 1
        auxContador = contadorMsg
        data.append("msg"+str(contadorMsg) + " db "+ str(arg1) + ", 0Dh,0Ah, 24h ")
        code.append("\n")
        code.append("mov ah,09h")
        code.append("lea dx,"+"msg"+str(auxContador))
        code.append("int 21h")
    elif (auxRes[:4] == "read"):
        code.append("\n")
        code.append("CALL SCAN_NUM")
        code.append("mov "+str(arg1)+",cx")
        code.append("lea dx,saltoLN")
        code.append("mov ah,09h")
        code.append("int 21h")
    elif (op == "="):
        if (arg1[:1] != "t"):
            aux = int(arg1)
            if (aux >= 0 and aux <=100000):
                data.append(str(res)+" dw "+str(arg1))
        else:
            code.append("\n")
            code.append("mov ax,"+str(arg1))
            code.append("mov "+str(res)+",ax")
    elif (auxRes[:5] == "print"):
        code.append("\n")
        code.append("mov ax,"+str(arg1))
        code.append("CALL PRINT_NUM")
        code.append("lea dx,saltoLN")
        code.append("mov ah,09h")
        code.append("int 21h")
    elif (auxRes[:1] == "L"):
        code.append("\n")
        code.append(str(auxRes))
    elif (op == "<"):
        aux = ""
        for x in range(0,len(auxLineas)):
            if(auxLineas[x] == i):
                x=x+1
                aux = auxLineas[x]
        code.append("\n")
        code.append("mov ax,"+str(arg1))
        code.append("cmp ax,"+str(arg2))
        code.append("jl L"+str(auxRes[4:]))
        if (aux[15:19] == "goto"):
            code.append("jmp L"+str(aux[19:]))
    elif (op == ">"):
        aux = ""
        for x in range(0,len(auxLineas)):
            if(auxLineas[x] == i):
                x=x+1
                aux = auxLineas[x]
        code.append("\n")
        code.append("mov ax,"+str(arg1))
        code.append("cmp ax,"+str(arg2))
        code.append("jg L"+str(auxRes[4:]))
        if (aux[15:19] == "goto"):
            code.append("jmp L"+str(aux[19:]))
    elif (res[:4] == "goto"):
        code.append("jmp L"+str(res[4:]))
    elif (op == "=="):
        aux = ""
        for x in range(0,len(auxLineas)):
            if(auxLineas[x] == i):
                x=x+1
                aux = auxLineas[x]
        code.append("\n")
        code.append("mov ax,"+str(arg1))
        code.append("cmp ax,"+str(arg2))
        code.append("je L"+str(auxRes[4:]))
        if (aux[15:19] == "goto"):
            code.append("jmp L"+str(aux[19:]))

for i in data:
    print(i)
for i in code:
    print(i)