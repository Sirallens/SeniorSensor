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

fo = open("Plain.txt", "w+")

choices = {'a': 1, 'b': 2}


# regresa vector del campo magnetico usando los componentes x y z
def magnitude(a, b, c):
    return math.sqrt(a * a + b * b + c * c)


# Esta funcion, junto con teslas(t), convierte 3 bytes Hexadecimal y decimal y posteriomente a nanoteslas
def H2D(v):
    if v > 8388607:
        return v - 16777216
    return teslas(v)


def teslas(t):  # To nano Teslas
    q = float(75)
    return (float(t) / q) * float(1000)


# --------

class point:
    def __init__(self, x=0, y=0, z=0, m=0):
        self.x = x
        self.y = y
        self.z = z
        self.m = m

    def __str__(self):
        return "{} {} {} {}".format(str(self.x), str(self.y), str(self.z), str(self.m))



class GeoMagSensor:
    def __init__(self, port=None):
        self.port = port
        self.s = serial.Serial(port, 115200, timeout=1)
        self.data = []
        self.map = nx.Graph()

    def getGrid(self):
        rows = input("Rows?: ")
        rows = int(rows)
        cols = input("Columns: ")
        cols = int(cols)

        input("Start the sensor at the bottom left of the grid, hit enter when ready.")
       
        
        for i in range(rows):
            for j in range(cols):
                self.map.add_node(self.getData())
                input("Move the sensor to the next position and hit enter when ready.")

        self.map.add_edges_from(((i, j), (pi, j)) for pi, i in pairwise(list(range(rows))) for j in range(cols))
        
        self.map.add_edges_from(((i, j), (i, pj)) for i in range(rows) for pj, j in pairwise(list(range(cols))))

    def printGrid(self):

        nx.draw(map, with_label= True)
        plt.draw()
        plt.show()

    def getData(self, k=1):

        x = 0
        y = 0
        z = 0
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
    
    def InitializeJourney(self)
        


    def Travel(self, Dest_Id):
        Destination = Dest_Id


    

def main():
    # main function
    Grid = GeoMagSensor(port)
    Grid.getGrid()
    fo.close()
    Grid.printGrid()


if __name__ == '__main__':
    main()
