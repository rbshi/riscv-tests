import sys

f = open("syn.trace", 'w')

access_amount = 10000
for ii in range(access_amount):
    addr = 2148392960+ii*8
    f.write("0,RD,{:s}\n".format(hex(addr)))