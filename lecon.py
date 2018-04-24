
import os
import serial
import math
import time
import numbers




# Gain = 0.3671 * cycleCount + 1.5



def H2D(x):
    if x >8388607:
        x = x - 16777216
        
 
    return x

#0.3671 * cycleCount + 1.5
def teslas(t):
    q = float(75)
    return round(((float(t)/q)*float(1)), 3)

def magnitude(a, b, c):
    return math.sqrt(a*a + b*b + c*c)


read_command = "$0wn01,71$1"
 
get_x = "$0wnA4rm$1"
 
get_y = "$0wnA7rm$1"
 
get_z = "$0wnAArm$1"
 
get_all = "$0wnA4mmm$1"
 
port = "COM10"
 
fo = open("data.txt", "w+")
 
 
command = " "
s = serial.Serial(port, 115200, timeout=1)


 
if s.isOpen() == False:
    s.open()
else:
    s.close()    
    s.open()
 
 
    k = 100


#-----------------------------------------------------------




time.sleep(3)

command = read_command
s.write(command.encode())
time.sleep(.05)

#x= 4403.30247686  y= -11808.8566425  z= 20465.3490118  magnitude = 24034.738985
 
while 1:
    #------Get one Measurement command----
    
    #------------ Ends Measurement Command---
 
    #retrieve data
 
    command = get_x
    s.write(command.encode())
    respuesta = s.read(6)
    time.sleep(.05)
    x = H2D(int(respuesta.decode('utf-8'),16))
    x = round(x, 6)
    
    time.sleep(.05)
    

    command = get_y
    s.write(command.encode())
    respuesta = s.read(6)
    time.sleep(.05)
    y = H2D(int(respuesta.decode('utf-8'),16))
    y = round(y, 1)
 
    time.sleep(.05)
    command = get_z
    s.write(command.encode())
    respuesta = s.read(6)
    time.sleep(.05)
    z = H2D(int(respuesta.decode('utf-8'),16))
    
    z= round(z, 1)
    

    os.system("cls")

    m = magnitude(teslas(x), teslas(y), teslas(z))
    m = round(m, 1)
    

    print(  "x= " + str(teslas(x)) + "  y= " + str(teslas(y)) + "  z= " + str(teslas(z)) + "  magnitude = " + str(m))
    
    
   
fo.close()