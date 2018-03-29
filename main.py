import os, serial, time

# Commands
read_command = "$0wn00,70$1"

get_x = "$0wnA4rm$1"
get_y = "$0wnA7rm$1"
get_z = "$0wnAArm$1"
port = '/dev/ttyUSB0'

def H2D(v):
    if v > 8388607:
        return v - 16777216
    return v

class point:
    def __init__(self,x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return "x:{} y:{} z:{}".format(str(self.x), str(self.y), str(self.z))

class GeoMagSensor:
    def __init__(self, port=None):
        self.port = port
        self.s = serial.Serial(port, 115200, timeout=1)
        self.data = []

    def getGrid(self):
        raw_input("Start the sensor at the bottm left of the grid, hit enter when ready.")
        for i in range(4):
            row = []
            for j in range(4):
                row.append(self.getData())
                raw_input("Move the sensor to the next position and hit enter when ready.")
        
    def printGrid(self):
        print('\n'.join([''.join(['{:3}'.format(item) for item in row]) for row in self.data]))
                

    def getData(self):
        x = 0
        y = 0
        z = 0
        for x in range(100):
            #------Get one Measurement command----
            command = read_command
            self.s.write(command.encode())
            time.sleep(.05)
            #------------ Ends Measurement Command---
            #retrieve data
            command = get_x
            self.s.write(command.encode())
            respuesta = self.s.read(6)
            time.sleep(.05)
            x += H2D(int(respuesta.decode('utf-8'),16))
            time.sleep(.05)

            command = get_y
            self.s.write(command.encode())
            respuesta = self.s.read(6)
            time.sleep(.05)
            y += H2D(int(respuesta.decode('utf-8'),16))

            time.sleep(.05)
            command = get_z
            self.s.write(command.encode())
            respuesta = self.s.read(6)
            time.sleep(.05)
            z += H2D(int(respuesta.decode('utf-8'),16))

        p = point(x/100,y/100,z/100)
        print(p)
        return p
                
def main():
    # main function
    Grid = GeoMagSensor(port)
    Grid.getGrid()
    Grid.printGrid()

if __name__ == '__main__':
    main()
