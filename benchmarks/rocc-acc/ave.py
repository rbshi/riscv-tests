
with open('log','r') as fp:
    fp.readline()
    fp.readline()    
    a = [int(x) for x in fp]
    print(sum(a)/len(a))
