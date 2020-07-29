# Maria Isabel Ortiz Naranjo
# Graficas por computadora
# Laboratorio 1
# 18176

# Basado en codigo proporcionado en clase por Dennis y en la pagina: https://blogprofesoraelizabeth.files.wordpress.com/2010/10/geometria2d.pdf
# Poligonos

import struct

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(c):
    return struct.pack('=h', c)

def dword(c):
    return struct.pack('=l', c)

def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

NEGRO = color(0,0,0)
BLANCO = color(1,1,1)
OTRO = color(0.75, 0.43, 0.13)


class Render(object):
    def __init__(self, width, height):
        self.curr_color = BLANCO
        self.clear_color = NEGRO
        self.glCreateWindow(width, height)

    # función glInit() 
    def glInit(self):
        pass

    # función glCreateWindow(width, height) 
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()
        self.glViewport(0, 0, width, height)

    # función glViewPort(x, y, width, height)
    def glViewport(self, x, y, width, height):
        self.xViewPort = x
        self.yViewPort = y
        self.viewPortWidth = width
        self.viewPortHeight = height

    # función glClear() 
    def glClear(self):
        self.framebuffer = [ [ self.clear_color for x in range(self.width)] for y in range(self.height) ]
    # funcion glLine
    def glLine(self, x0, y0, x1, y1):
        x0 = round(( x0 + 1) * (self.viewPortWidth   / 2 ) + self.xViewPort)
        x1 = round(( x1 + 1) * (self.viewPortWidth   / 2 ) + self.xViewPort)
        y0 = round(( y0 + 1) * (self.viewPortHeight / 2 ) + self.yViewPort)
        y1 = round(( y1 + 1) * (self.viewPortHeight / 2 ) + self.yViewPort)

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        steep = dy > dx
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        offset = 0 
        limit = 0.5
        
        m = dy/dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.glVertex_coord(y, x)
            else:
                self.glVertex_coord(x, y)

            offset += m
            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 1

    # Funcion de las coordenadas
    def glLine_coord(self, x0, y0, x1, y1): 
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5
        
        try:
            m = dy/dx
        except ZeroDivisionError:
            pass
        else:
            y = y0

            for x in range(x0, x1 + 1):
                if steep:
                    self.glVertex_coord(y, x)
                else:
                    self.glVertex_coord(x, y)

                offset += m
                if offset >= limit:
                    y += 1 if y0 < y1 else -1
                    limit += 1

    def glClearColor(self, r, g, b):
        self.clear_color = color(r,g,b)


    def glColor(self, r=0.5, g=0.5, b=0.5):
        self.curr_color = color(r,g,b)

    def glVertex(self, x, y):
        pixelX = ( x + 1) * (self.viewPortWidth / 2 ) + self.xViewPort
        pixelY = ( y + 1) * (self.viewPortHeight / 2 ) + self.yViewPort
        try:
            self.framebuffer[round(pixelY)][round(pixelX)] = self.curr_color
        except:
            pass

    def glVertex_coord(self, x, y):
        try:
            self.framebuffer[y][x] = self.curr_color
        except:
            pass

    def glFinish(self, filename):
        f = open(filename, 'bw')
        f.write(bytes('B'.encode('ascii')))
        f.write(bytes('M'.encode('ascii')))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for x in range(self.width):
            for y in range(self.height):
                f.write(self.framebuffer[y][x])

        f.close()

    def drawPoligono(self, points):

        count = len(points)

        for i in range(count):
            v0 = points[i]
            v1 = points[(i+1)%count]

            self.glLine_coord(v0[0], v0[1], v1[0], v1[1])

    # Funcion tomada del blog citado arriba, pagina 35
    def Inundacion(self, x, y, r, g, b):
        color1 = color(1, 1, 1)
        color2 = color(r, g, b)
        punto = self.framebuffer[y][x]

        if (punto != color1 and punto != color2):
            self.glColor(r, g, b)
            self.glVertex_coord(x,y)

            self.Inundacion(x+1, y, r, g, b)
            self.Inundacion(x, y+1, r, g, b)
            #self.Inundacion(x-1, y, r, g, b)
            self.Inundacion(x, y-1, r, g, b)    
# Lineas 
r = Render(1000,500)
r.glColor(1, 1, 1)

poly1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
poly2 = [(321, 335), (288, 286), (339, 251), (374, 302)]
poly3 = [(377, 249), (411, 197), (436, 249)]
poly4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52), (750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230), (597, 215), (552, 214), (517, 144), (466, 180)]
poly5 = [(682, 175), (708, 120), (735, 148), (739, 170)]

r.drawPoligono(poly1)
r.drawPoligono(poly2)
r.drawPoligono(poly3)
r.drawPoligono(poly4)
r.drawPoligono(poly5)

# Poligono 1 - Estrella
r.Inundacion(168, 379, 0.5, 0.89, 0.42)
r.Inundacion(182, 332, 0.5, 0.89, 0.42)

# Poligono 2 - Rombo
r.Inundacion(289, 286, 0.8, 0.12, 0.34)

# Poligono 3 - Triangulo
r.Inundacion(379, 248, 0.99, 0.87, 0.2)

# Poligono 4 - Tetera
r.Inundacion(418, 176, 0.54, 0.34, 0.76)
r.Inundacion(582, 229, 0.54, 0.34, 0.76)
r.Inundacion(537, 37, 0.54, 0.34, 0.76)

# Poligono 5 - Agujero de Tetera
r.Inundacion(683, 174, 0.56, 0.7, 0.75)

r.glFinish('output.bmp')
