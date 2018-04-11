
import os
import serial
import math
import time

def H2D(x):
    if x >8388607:
        x = x - 16777216
        
 
    return x

def teslas(t):
    q = float(75)
    #format((float(t)/q), '.4f')

    
    return (float(t)/q)*float(1000)

def magnitude(a, b, c):
    return math.sqrt(a*a + b*b + c*c)


read_command = "$0wn00,70$1"
 
get_x = "$0wnA4rm$1"
 
get_y = "$0wnA7rm$1"
 
get_z = "$0wnAArm$1"
 
get_all = "$0wnA4mmm$1"
 
port = '/dev/ttyUSB0'
 
fo = open("data.txt", "w+")
 
 
command = " "
s = serial.Serial(port, 115200, timeout=1)

try:
 
    if s.isOpen() == False:
        s.open()
    else:
        s.close()    
        s.open()
except:
    s.port = '/dev/ttyUSB1'
    if s.isOpen() == False:
        s.open()
    else:
        s.close()    
        s.open()     
    raise
    

s.write("$0wn04,00,190,00,190,00,190$1") 
#-----------------------------------------------------------
s.write("$0r84nii$1")

print(str(s.read(16)))

time.sleep(3)

command = read_command
s.write(command.encode())
time.sleep(.05)

#x= 4403.30247686  y= -11808.8566425  z= 20465.3490118  magnitude = 24034.738985
 
while 1:
    #------Get one Measurement command----
    command = read_command
    s.write(command.encode())
    time.sleep(.05)
    #------------ Ends Measurement Command---
 
    #retrieve data
 
    command = get_x
    s.write(command.encode())
    respuesta = s.read(6)
    time.sleep(.05)
    x = H2D(int(respuesta.decode('utf-8'),16))
    time.sleep(.05)
 
    command = get_y
    s.write(command.encode())
    respuesta = s.read(6)
    time.sleep(.05)
    y = H2D(int(respuesta.decode('utf-8'),16))
 
 
    time.sleep(.05)
    command = get_z
    s.write(command.encode())
    respuesta = s.read(6)
    time.sleep(.05)
    z = H2D(int(respuesta.decode('utf-8'),16))
    
    

    os.system("clear")



    print(  "x= " + str(teslas(x)) + "  y= " + str(teslas(y)) + "  z= " + str(teslas(z)) + "  magnitude = " + str(magnitude(teslas(x), teslas(y), teslas(z))))
    fo.write( " " + str(teslas(x)) + "   " + str(teslas(y)) + "   " + str(teslas(z)) + " " + str(magnitude(teslas(x), teslas(y), teslas(z))))
    
   
fo.close()
