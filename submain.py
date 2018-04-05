import os, serial, time, math

# Commands
read_command = "$0wn01,71$1"

get_x = "$0wnA4rm$1"
get_y = "$0wnA7rm$1"
get_z = "$0wnAArm$1"
port = '/dev/ttyUSB0'

fo = open("Plain.txt", "w+")

choices = {'a': 1, 'b': 2}

#regresa vector del campo magnetico usando los componentes x y z
def magnitude(a, b, c):
    return math.sqrt(a*a + b*b + c*c)

# Esta funcion, junto con teslas(t), convierte 3 bytes Hexadecimal y decimal y posteriomente a nanoteslas
def H2D(v):
    if v > 8388607:
        return v - 16777216
    return teslas(v)

def teslas(t): #To nano Teslas
    q = float(75)
    return (float(t)/q)*float(1000)
#--------

class point:
    def __init__(self,x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return "{} {} {}".format(str(self.x), str(self.y), str(self.z))

class GeoMagSensor:
    def __init__(self, port=None):
        self.port = port
        self.s = serial.Serial(port, 115200, timeout=1)
        self.data = []

    def getGrid(self):
        raw_input("Start the sensor at the bottm left of the grid, hit enter when ready.")
        for i in range(2):
            row = []
            for j in range(3):
                row.append(self.getData())
                raw_input("Move the sensor to the next position and hit enter when ready.")
        
    def printGrid(self):
        print ('\n'.join([''.join(['{:3}'.format(item) for item in row]) for row in self.data]))
        
        
    

    
    def getData(self, k = 1):
        
        x = 0
        y = 0
        z = 0
        self.s.write(read_command.encode())
        for x in range(k):
            #------Get one Measurement command---- Currently in continuos measurement mode; 
            #command = read_command
            #self.s.write(command.encode())
            #time.sleep(.05)
            #------------ Ends Measurement Command---
            #retrieve data
            command = get_x
            self.s.write(command.encode())
            respuesta = self.s.read(6)
            time.sleep(.05)
            x = H2D(int(respuesta.decode('utf-8'),16))
            time.sleep(.05)

            command = get_y
            self.s.write(command.encode())
            respuesta = self.s.read(6)
            time.sleep(.05)
            y = H2D(int(respuesta.decode('utf-8'),16))
            time.sleep(.05)
            
            command = get_z
            self.s.write(command.encode())
            respuesta = self.s.read(6)
            time.sleep(.05)
            z = H2D(int(respuesta.decode('utf-8'),16))

            
        fo.write(  "x= " + str(x) + "  y= " + str(y) + "  z= " + str(z) + "  magnitude = " + str(magnitude(x,y, z)) + '/n')
        p = point(x,y,z)
        print(p)
        return p
                
def main():
    # main function
    Grid = GeoMagSensor(port)
    Grid.getGrid()
    fo.close()
    Grid.printGrid()
    
    





if __name__ == '__main__':
    main()
