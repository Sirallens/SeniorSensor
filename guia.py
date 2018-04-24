import serial, time, math
import networkx as nx
from networkx.utils import pairwise
import numbers

import matplotlib.pyplot as plt

# Commands
read_command = "$0wn01,71$1"

get_x = "$0wnA4rm$1"
get_y = "$0wnA7rm$1"
get_z = "$0wnAArm$1"
port = 'COM10'
port_arduino = 'COM8'
fo = open("Plain.txt", "w+")

choices = {'a': 1, 'b': 2}


# regresa vector del campo magnetico usando los componentes x y z
def magnitude(a, b, c):
    return math.sqrt(a * a + b * b + c * c)


# Esta funcion, junto con teslas(t), convierte 3 bytes Hexadecimal y decimal y posteriomente a nanoteslas
def H2D(v = 0.0):
    if v > 8388607.0:
        return v - 16777216.0
    return teslas(v)


def teslas(t):  # To nano Teslas
    q = float(75)
    return round(((float(t)/q)*float(1)), 3)


# --------

class point:
    def __init__(self, x=0.0, y=0.0, z=0.0, m=0.0, XIsPositive = False):
        self.x = x
        self.y = y
        self.z = z
        self.m = m
        

        if x > 0:
            self.XIsPositive = True

    def __str__(self):
        return "{} {} {} {}".format(str(self.x), str(self.y), str(self.z), str(self.m))



class GeoMagSensor:
    def __init__(self, port=None, port_a = None):
        self.port = port
        self.s = serial.Serial(port, 115200, timeout=1)
        self.data = []

        self.porta = port_a
        self.sa = serial.Serial(port_a, 9600, timeout= 1)

      
       
       

    def getGrid(self):
        loc = input("How many points will you record? \n")
        loc = int(loc)
        input("Start the sensor at the bottom left of the grid, hit enter when ready.")

        for q in range(loc):
            self.data.append(self.getData())
            input("Move to the next point")
               
           
    def getData(self, k=1):

        x = float()
        y = float()
        z = float()
        self.s.write(read_command.encode())
        for x in range(k):
            # ------Get one Measurement command---- Currently in continuos measurement mode;
            # command = read_command
            # self.s.write(command.encode())
            # time.sleep(.05)
            # ------------ Ends Measurement Command---
            # retrieve data
            command = get_x
            self.s.write(command.encode())
            respuesta = self.s.read(6)
            time.sleep(.05)
            x = H2D(int(respuesta.decode('utf-8'), 16))
            x = round(x, 1)
            time.sleep(.05)

            command = get_y
            self.s.write(command.encode())
            respuesta = self.s.read(6)
            time.sleep(.05)
            y = H2D(int(respuesta.decode('utf-8'), 16))
            y = round(y, 1)
            time.sleep(.05)

            command = get_z
            self.s.write(command.encode())
            respuesta = self.s.read(6)
            time.sleep(.05)
            z = H2D(int(respuesta.decode('utf-8'), 16))
            z = round(z, 1)


        mag = magnitude(x, y, z)
        mag = round(mag, 1)
        fo.write("x= " + str(x) + "  y= " + str(y) + "  z= " + str(z) + "  magnitude = " + str(mag) + '\n')
        p = point(x, y, z, mag)
        print(p)
        return p 

    
    def getCurrentLoc(self, k=1):

        x = float()
        y = float()
        z = float()
        self.s.write(read_command.encode())
        for x in range(k):
            # ------Get one Measurement command---- Currently in continuos measurement mode;
            # command = read_command
            # self.s.write(command.encode())
            # time.sleep(.05)
            # ------------ Ends Measurement Command---
            # retrieve data
            command = get_x
            self.s.write(command.encode())
            respuesta = self.s.read(6)
            time.sleep(.05)
            x = H2D(int(respuesta.decode('utf-8'), 16))
            x = round(x,1 )
            time.sleep(.05)

            command = get_y
            self.s.write(command.encode())
            respuesta = self.s.read(6)
            time.sleep(.05)
            y = H2D(int(respuesta.decode('utf-8'), 16))
            y = round(y, 1)
            time.sleep(.05)

            command = get_z
            self.s.write(command.encode())
            respuesta = self.s.read(6)
            time.sleep(.05)
            z = H2D(int(respuesta.decode('utf-8'), 16))
            z = round(z, 1)


        mag = magnitude(x, y, z)
        mag = round(mag, 1)
        fo.write("x= " + str(x) + "  y= " + str(y) + "  z= " + str(z) + "  magnitude = " + str(mag) + '\n')
        p = point(x, y, z, mag)
       
        return p


    def Get_direction(self, CurrLoc= point(), destLoc = point()):
        direction = str()
        print(CurrLoc)
        print(destLoc)

        if  (abs(CurrLoc.x - destLoc.x) < 500.0) & (abs(CurrLoc.y - destLoc.y) < 500.0):
            direction = "O"
            self.sa.write(direction.encode())
        elif (CurrLoc.x < destLoc.x) & (CurrLoc.y < destLoc.y):
            direction = "N"
            self.sa.write(direction.encode())
        elif (CurrLoc.x < destLoc.x) & (CurrLoc.y > destLoc.y):
            direction = "S" 
            self.sa.write(direction.encode())
        elif (CurrLoc.x > destLoc.x) & (CurrLoc.y < destLoc.y):
            direction = "W"
            self.sa.write(direction.encode())
        elif (CurrLoc.x > destLoc.x) & (CurrLoc.y  > destLoc.y):
            direction = "E"
            self.sa.write(direction.encode())
        
        else:
            #Should never get here
            direction = "Something bad hapenned"

        return direction

    def InitializeJourney(self, Destination):
        
        Dest_point = self.data[Destination]
        Actual_location = point()
        where_To_go = str()
        while(1):
            Actual_location = self.getCurrentLoc()
            where_To_go = self.Get_direction(Actual_location, Dest_point)
            if where_To_go == "OK":
                print("We think we have arrived, hopefully")
                break
            else:
                print(where_To_go)
                self.sa.write
            time.sleep(0.3)


    def Travel(self):
        
        dest_id = input("Where do you want to go, 0 to k-1? (Destination 0 is the first point saved, and k-1, the last")
        dest_id = int(dest_id)
        input("Press any key to start trip")

        self.InitializeJourney(dest_id)



    

def main():
    # main function
    Grid = GeoMagSensor(port, port_arduino)
    Grid.getGrid()
   
    Grid.Travel()
    #log of records
    fo.close()


if __name__ == '__main__':
    main()
