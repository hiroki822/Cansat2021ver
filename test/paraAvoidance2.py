def ParaJudge(x):
    lux = [x,10,10]
    luxthd = input("")
    LuxThd = float(luxthd)
    
    if lux[0] < LuxThd:
        print(lux[0])
        return[0,lux[0]]
    else:
        return[1,lux[0]]
x = 9
ParaJudge(x)
    
