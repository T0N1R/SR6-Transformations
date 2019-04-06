'''
Antonio Reyes
carnet> 17273
5/2/2019
Graficas por Computadora
materiales

'''

import struct
import collections
import time
import random
import math
import copy

def char(c):
    return struct.pack("=c", c.encode('ascii'))


def word(c):
    return struct.pack("=h", c)


def dword(c):
    return struct.pack("=l", c)


def color(r, g, b):
    try:
        return bytes([b, g, r])

    except:
        return bytes([255,0,0])

#listas para guardar los valores de los vertices
V2 = collections.namedtuple("Vertex2", ["x", "y"])
V3 = collections.namedtuple("Vertex3", ["x", "y", "z"])

class Texture(object):
    def __init__(self, filename):
        self.path = filename
        self.read()

    def read(self):
        img = open(self.path, "rb")
        img.seek(2 + 4 + 4)
        header_size = struct.unpack("=l", img.read(4))[0]
        img.seek(2 + 4 + 4 + 4 + 4)
        self.width = struct.unpack("=l", img.read(4))[0]
        self.height = struct.unpack("=l", img.read(4))[0]
        self.pixels = []
        img.seek(header_size)

        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(img.read(1))
                g = ord(img.read(1))
                r = ord(img.read(1))
                self.pixels[y].append(color(r,g,b))

        img.close()

    def get_color(self, tx, ty, intensity):
        x = int(tx * self.width) -1
        y = int(ty * self.height) -1
        #print(x)
        #print(y)
        return bytes (
            map(
            lambda b : round(b * intensity) 
            if b * intensity > 0 else 0, 
            self.pixels[y][x] 
            )
        )



class Bitmap(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.framebuffer = []


    '''
    Colorear toda la pantalla de un color, establecido con glClearcolor
    El color eleido se establece por medio del valor de red, green y blue.
    '''
    

    def glClear(self):
        self.framebuffer = [
            [color(r.red, r.green, r.blue) for x in range(self.width)]
            for y in range(self.height)
        ]

        self.zbuffer = [
            [-float('inf') for x in range(self.width)]
            for y in range(self.height)
        ]

    def tipoColor(self, x, y):
        return self.framebuffer[y][x]
        

    '''
    Elegir cual es el color que va a utilizar glClear para colorear la imagen.
    Establece el valor de red, green
    '''

    def glClearColor(self, r, g, b):
        red = int(255 * r)
        green = int(255 * g)
        blue = int(255 * b)

        self.red = red
        self.green = green
        self.blue = blue

    def write(self, filename):
        f = open(filename, 'bw')

        # file header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # image header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width + self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])

        f.close()

    '''
    point agrega un punto de un color especifico en el lugar deseado
    '''

    def point(self, x, y, color):
        #print(y,x)
        try:
            self.framebuffer[y][x] = color
        except:
            pass
    '''
    Funcion que modifica el color del punto que se genera en glVertex
    '''

    def glColor(self, r, g, b):
        
        redVertex = int(255 * r)
        greenVertex = int(255 * g)
        blueVertex = int(255 * b)
        
        """
        redVertex = int(r)
        greenVertex = int(g)
        blueVertex = int(b)
        """

        self.redVertex = redVertex
        self.greenVertex = greenVertex
        self.blueVertex = blueVertex

    def glViewPort(self, viewportX, viewportY, viewportWidth, viewportHeight):
        self.viewportX = viewportX
        self.viewportY = viewportY
        self.viewportWidth = viewportWidth
        self.viewportHeight = viewportHeight
        self.glClear()

    def glVertex(self):
        
        #Se establcece el centro del viewport

        centroX = r.viewportX + (int(r.viewportWidth / 2))
        centroY = r.viewportY + (int(r.viewportHeight / 2))

        self.centroX = centroX
        self.centroY = centroY

        arrayX = []
        self.arrayX = arrayX

        arrayY = []
        self.arrayY = arrayY

        arrayLlenar = []
        self.arrayLlenar = arrayLlenar


    def borrarArray(self):
        self.arrayLlenar = []
        self.arrayX = []
        self.arrayY = []

    def glLine(self, x0, y0, x1, y1):
        '''
        Se establece la posición de los puntos en el viewport en base al centro establecido en 
        glVertex
        '''
        #x0 = round(r.centroX + ((r.viewportWidth / 2) * x0))
        #y0 = round(r.centroY + ((r.viewportHeight / 2) * y0))
        #x1 = round(r.centroX + ((r.viewportWidth / 2) * x1))
        #y1 = round(r.centroY + ((r.viewportHeight / 2) * y1))

        r.arrayX.append(x0)
        r.arrayY.append(y0)

        #diferencia entre los valores de "x" y "y"
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        #steep va a definir si se ingresa los puntos sucesivos en "x" o en "y"
        #esto sera defnido por la pendiente que se define entre los puntos.
        steep = dy > dx

        if steep:
            x0,y0 = y0,x0
            x1,y1 = y1,x1

        if x0 > x1:
            x0,x1 = x1,x0
            y0,y1 = y1,y0
        
        dy = abs(y1-y0)
        dx = abs(x1 - x0)

        offset = 0 * 2 * dx
        threshold = 0.5 * 2 * dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                try:
                    r.point(int(y), int(x), color(r.redVertex, r.greenVertex, r.blueVertex))
                except:
                    pass

            else:
                try:
                    r.point(int(x), int(y), color(r.redVertex, r.greenVertex, r.blueVertex))

                except:
                    pass
            
            offset += dy

            #define el patron de pixeles consecutivos
            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += 1 * dx

    def gouard(self, **kwdargs):
        #barycentric
        w,v,u = kwdargs['bar']

        light = kwdargs['luzShader']
        nA, nB, nC = kwdargs['varying_normals']
        #print(nA, nB, nC)

        normalx = float(nA.x) * w * float(nB.x) * v * float(nC.x) * u
        normaly = float(nA.y) * w * float(nB.y) * v * float(nC.y) * u
        normalz = float(nA.z) * w * float(nB.z) * v * float(nC.z) * u

        vn = V3(normalx, normaly, normalz)

        intensity = abs(pPunto(vn, light)) * 20


        return color(int(intensity * 255), int(intensity * 244), int(intensity * 60) )


    #los tres puntos del triangulo
    def triangle(self, A, B, C, intensidad, vn1, vn2, vn3, light):
        #print(A, B, C)
        try:
            
            bbox_min, bbox_max = bbox(A, B, C)

            if bbox_min.x < 0:
                bbox_min = V2(0, bbox_min.y)

            if bbox_min.y < 0:
                bbox_min = V2(bbox_min.x, 0)

            
            for x in range(bbox_min.x, bbox_max.x + 1):
                for y in range(bbox_min.y, bbox_max.y + 1):

                    w,v,u = barycentric(A, B, C, V2(x,y))

                    if w < 0 or v < 0 or u < 0:
                        continue


                    colorShade = self.gouard(
                        bar=(w,v,u),
                        varying_normals = (vn1, vn2, vn3),
                        luzShader = light,
                        )

                    z = A.z * w + B.z * v + C.z * u

                    #Se verifica si se pinta el punto en caso su coordenada en z sea mayor a la anteriormente pintada en el mismo lugar
                    if z > self.zbuffer[y][x]:
                        self.point(x,y,colorShade)
                        self.zbuffer[y][x] = z
        
        except:
            pass

    def viewportMatrix(self,x,y):
        w = int(self.width/2)
        h = int(self.height/2)
        newx = int(x + w)
        newy = int(y + h)
        return [
            [w, 0, 0, newx],
            [0, h, 0, newy],
            [0, 0, 128, 128],
            [0, 0, 0, 1]
        ]
    
    def modelMatrix(self, tx, ty, tz, rotx, roty, rotz, sx, sy, sz):
        rotx = rotx * (180/math.pi)
        roty = roty * (180/math.pi)
        rotz = rotz * (180/math.pi)

        matriz_traslacion = [
            [1,0,0,tx],
            [0,1,0,ty],
            [0,0,1,tz],
            [0,0,0,1]
            ]

        """
        print("MATRIZ TRASLACION")
        for x in matriz_traslacion:
            print(x)
        """

        matriz_rotacionX = [
            [1,     0,              0,              0],
            [0,math.cos(rotx), math.sin(rotx) * -1, 0],
            [0,math.sin(rotx), math.cos(rotx)     , 0],
            [0,     0,              0,              1]
            ]

        """
        print("MATRIZ ROTACION X")
        for x in matriz_rotacionX:
            print(x)
        """

        matriz_rotacionY = [
            [math.cos(roty)     , 0  ,math.sin(roty),0],
            [0                  , 1  ,0             ,0],
            [math.sin(roty * -1), 0  ,math.cos(roty),0],
            [0                  , 0  ,0             ,1]
            ]

        """
        print("MATRIZ ROTACION Y")
        for x in matriz_rotacionY:
            print(x)
        """


        matriz_rotacionZ = [
            [math.cos(rotz)     , math.sin(rotz) * -1  ,0,0],
            [math.sin(rotz)     , math.cos(rotz)       ,0,0],
            [0                  , 0                    ,1,0],
            [0                  , 0                    ,0,1]
            ]
        
        """
        print("MATRIZ ROTACION Z")
        for x in matriz_rotacionZ:
            print(x)
        """

        matriz_escala = [
            [sx,0 ,0 ,0],
            [0 ,sy,0 ,0],
            [0 ,0 ,sz,0],
            [0 ,0 ,0 ,1]
            ]
        
        """
        print("MATRIZ ESCALA")
        for x in matriz_escala:
            print(x)
        """

        operacion1 = multMATRIX4(matriz_rotacionY, matriz_rotacionZ)

        """
        print("OPERACION 1")
        for x in operacion1:
            print(x)
        """
        
        operacion2 = multMATRIX4(operacion1, matriz_rotacionX)

        """
        print("OPERACION 2")
        for x in operacion2:
            print(x)
        """

        operacion3 = multMATRIX4(operacion2, matriz_escala)
        
        """
        print("OPERACION 3")
        for x in operacion3:
            print(x)
        """

        operacion4 = multMATRIX4(operacion3, matriz_traslacion)

        """
        print("OPERACION 4")
        for x in operacion4:
            print(x)
        """

        return operacion4
    
    def viewMatrix(self, x, y, z, center):
        M = [
            [x.x,  x.y,  x.z, 0],
            [y.x,  y.y,  y.z, 0],
            [z.x,  z.y,  z.z, 0],
            [  0,    0,    0, 1]
        ]

        """
        print("MATRIZ M")
        for x in M:
            print(x)
        """

        O = [
            [1, 0, 0, -1 * center.x],
            [0, 1, 0, -1 * center.y],
            [0, 0, 1, -1 * center.z],
            [0, 0, 0, 1]
        ]

        operacionView = multMATRIX4(M, O)

        return operacionView

    
    def proyectionMatrix(self, coeff):
        return [
            [1,0,0,0],
            [0,1,0,0],
            [0,0,1,0],
            [0,0,0.0016,1]
        ]

    def look(self, eye, center, up):
        z = restaVector(eye, center)
        normalZ = (math.sqrt(z.x**2 + z.y**2 + z.z**2))

        if normalZ == 0:
            zNormalizado = V3(0,0,0)
        else:
            zNormalizado = V3((z.x / normalZ), (z.y/normalZ), (z.z/normalZ))
        

        x = cross(up, z)
        normalX = (math.sqrt(x.x**2 + x.y**2 + x.z**2))

        if normalX == 0:
            xNormalizado = V3(0,0,0)
        else:
            xNormalizado = V3((x.x / normalX), (x.y/normalX), (x.z/normalX))

        y = cross(z, x)
        normalY = (math.sqrt(y.x**2 + y.y**2 + y.z**2))
        if normalY == 0:
            yNormalizado = V3(0,0,0)
        else:
            yNormalizado = V3((x.x / normalY), (x.y/normalY), (x.z/normalY))

        a = self.viewMatrix(xNormalizado, yNormalizado, zNormalizado, center)
        b = self.proyectionMatrix(-1/normalZ)

        return a, b



def sumaVector(v0, v1):
    return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def multiEscalar(esc, v0):
    return V3(esc * v0.x, esc * v0.y, esc * v0.z)

def pPunto(v0, v1):
    return (v0.x * v1.x + v0.y * v1.y + v0.z * v1.z)

def cross(v0,v1):
    return V3( (v0.y * v1.z - v1.y * v0.z), (v0.z * v1.x - v1.z * v0.x), (v0.x * v1.y - v1.x * v0.y)      )

def restaVector(v0,v1):
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def multMATRIX(matriz1, matriz2):
    matriz_respuesta = [0,0,0,0]

    matriz_respuesta[0] = matriz1[0][0] * matriz2[0] + matriz1[0][1] * matriz2[1] + matriz1[0][2] * matriz2[2] + matriz1[0][3] * matriz2[3]
    matriz_respuesta[1] = matriz1[1][0] * matriz2[0] + matriz1[1][1] * matriz2[1] + matriz1[1][2] * matriz2[2] + matriz1[1][3] * matriz2[3]
    matriz_respuesta[2] = matriz1[2][0] * matriz2[0] + matriz1[2][1] * matriz2[1] + matriz1[2][2] * matriz2[2] + matriz1[2][3] * matriz2[3]
    matriz_respuesta[3] = matriz1[3][0] * matriz2[0] + matriz1[3][1] * matriz2[1] + matriz1[3][2] * matriz2[2] + matriz1[3][3] * matriz2[3]

    return matriz_respuesta



def multMATRIX4(matriz1, matriz3):
    matrizRespuesta4 = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]
    ]

    matrizRespuesta4[0][0] = matriz1[0][0] * matriz3[0][0] + matriz1[0][1] * matriz3[1][0] + matriz1[0][2] * matriz3[2][0] + matriz1[0][3] * matriz3[3][0]
    matrizRespuesta4[0][1] = matriz1[0][0] * matriz3[0][1] + matriz1[0][1] * matriz3[1][1] + matriz1[0][2] * matriz3[2][1] + matriz1[0][3] * matriz3[3][1]
    matrizRespuesta4[0][2] = matriz1[0][0] * matriz3[0][2] + matriz1[0][1] * matriz3[1][2] + matriz1[0][2] * matriz3[2][2] + matriz1[0][3] * matriz3[3][2]
    matrizRespuesta4[0][3] = matriz1[0][0] * matriz3[0][3] + matriz1[0][1] * matriz3[1][3] + matriz1[0][2] * matriz3[2][3] + matriz1[0][3] * matriz3[3][3]

    matrizRespuesta4[1][0] = matriz1[1][0] * matriz3[0][0] + matriz1[1][1] * matriz3[1][0] + matriz1[1][2] * matriz3[3][0] + matriz1[1][3] * matriz3[3][0]
    matrizRespuesta4[1][1] = matriz1[1][0] * matriz3[0][1] + matriz1[1][1] * matriz3[1][1] + matriz1[1][2] * matriz3[2][1] + matriz1[1][3] * matriz3[3][1]
    matrizRespuesta4[1][2] = matriz1[1][0] * matriz3[0][2] + matriz1[1][1] * matriz3[1][2] + matriz1[1][2] * matriz3[2][2] + matriz1[1][3] * matriz3[3][2]
    matrizRespuesta4[1][3] = matriz1[1][0] * matriz3[0][3] + matriz1[1][1] * matriz3[1][3] + matriz1[1][2] * matriz3[2][3] + matriz1[1][3] * matriz3[3][3]

    matrizRespuesta4[2][0] = matriz1[2][0] * matriz3[0][0] + matriz1[2][1] * matriz3[1][0] + matriz1[2][2] * matriz3[3][0] + matriz1[2][3] * matriz3[3][0]
    matrizRespuesta4[2][1] = matriz1[2][0] * matriz3[0][1] + matriz1[2][1] * matriz3[1][1] + matriz1[2][2] * matriz3[2][1] + matriz1[2][3] * matriz3[3][1]
    matrizRespuesta4[2][2] = matriz1[2][0] * matriz3[0][2] + matriz1[2][1] * matriz3[1][2] + matriz1[2][2] * matriz3[2][2] + matriz1[2][3] * matriz3[3][2]
    matrizRespuesta4[2][3] = matriz1[2][0] * matriz3[0][3] + matriz1[2][1] * matriz3[1][3] + matriz1[2][2] * matriz3[2][3] + matriz1[2][3] * matriz3[3][3]

    matrizRespuesta4[3][0] = matriz1[3][0] * matriz3[0][0] + matriz1[3][1] * matriz3[1][0] + matriz1[3][2] * matriz3[3][0] + matriz1[3][3] * matriz3[3][0]
    matrizRespuesta4[3][1] = matriz1[3][0] * matriz3[0][1] + matriz1[3][1] * matriz3[1][1] + matriz1[3][2] * matriz3[2][1] + matriz1[3][3] * matriz3[3][1]
    matrizRespuesta4[3][2] = matriz1[3][0] * matriz3[0][2] + matriz1[3][1] * matriz3[1][2] + matriz1[3][2] * matriz3[2][2] + matriz1[3][3] * matriz3[3][2]
    matrizRespuesta4[3][3] = matriz1[3][0] * matriz3[0][3] + matriz1[3][1] * matriz3[1][3] + matriz1[3][2] * matriz3[2][3] + matriz1[3][3] * matriz3[3][3]

    return matrizRespuesta4



newmtl = []
mtlCOLOR = []
vertices = [["0", "0", "0", "0"]]
verticeT = [["0", "0", "0", "0"]]
verticeN = [["0", "0", "0", "0"]]

def leerMTL(archivo):
    with open(archivo) as mtl:
        lines = mtl.read()

    arregloLineas = lines.split("\n")
    
    for x in arregloLineas:
        if x.startswith("newmtl"):
            a = x.split()
            if a[1] not in newmtl:
                newmtl.append(a[1])

        if x.startswith("Kd"):
            colorMTL = []
            a = x.split()
            colorMTL.append(a[1])
            colorMTL.append(a[2])
            colorMTL.append(a[3])
            if colorMTL not in mtlCOLOR:
                mtlCOLOR.append(colorMTL)

def dataObj(archivo, enviarOBJ):
    with open(archivo) as a:
        lines = a.read()

    arregloLineas = lines.split("\n")
    
    for x in arregloLineas:

        if x.startswith("v "):
            nuevoVertice = []
            a = x.split()

            contador = 1

            while contador < 4:
                nuevoVertice.append(a[contador])
                contador += 1

            vertices.append(nuevoVertice)   

        if x.startswith("vt "):
            nuevoVT = []
            a = x.split()
            contador = 1
            while contador < 3:
                nuevoVT.append(a[contador])
                contador += 1

            #print(nuevoVT)
            verticeT.append(nuevoVT)

        if x.startswith("vn "):
            nuevoVN = []
            a = x.split()
            contador = 1
            while contador < 4:
                nuevoVN.append(a[contador])
                contador += 1
            
            verticeN.append(nuevoVN)


    for x in arregloLineas:
        

        if x.startswith("f "):
            serieCaras1 = []
            serieVT = []
            serieCaras3 = []
            a = x.split(" ")
            del a[0]

            for i in a:
                q = i.split("/")
                serieCaras1.append(q[0])
                if q[1] == "":
                    serieVT.append(0)
                else:
                    serieVT.append(q[1])
                serieCaras3.append(q[2])
                        
            #print(serieCaras)
            x0 = float(vertices[int(serieCaras1[0])][0])
            y0 = float(vertices[int(serieCaras1[0])][1])
            z0 = float(vertices[int(serieCaras1[0])][2])

            x1 = float(vertices[int(serieCaras1[1])][0])
            y1 = float(vertices[int(serieCaras1[1])][1])
            z1 = float(vertices[int(serieCaras1[1])][2])

            x2 = float(vertices[int(serieCaras1[2])][0])
            y2 = float(vertices[int(serieCaras1[2])][1])
            z2 = float(vertices[int(serieCaras1[2])][2])

            x0 = round(r.centroX + ((r.viewportWidth / 2) * x0))
            y0 = round(r.centroY + ((r.viewportHeight / 2) * y0))
            x1 = round(r.centroX + ((r.viewportWidth / 2) * x1))
            y1 = round(r.centroY + ((r.viewportHeight / 2) * y1))
            x2 = round(r.centroX + ((r.viewportWidth / 2) * x2))
            y2 = round(r.centroY + ((r.viewportHeight / 2) * y2))
        
            z0 = round(r.centroX + ((r.viewportWidth / 2) * z0))
            z1 = round(r.centroX + ((r.viewportWidth / 2) * z1))
            z2 = round(r.centroX + ((r.viewportWidth / 2) * z2))

            luces = V3(1,1,1)
            normal = (math.sqrt(luces.x**2 + luces.y**2 + luces.z**2))
            luz = V3(luces.x/normal, luces.y/normal, luces.z/normal)

            ba = restaVector(V3(x1, y1, z1), V3(x0, y0, z0))
            ca = restaVector(V3(x2, y2, z2), V3(x0, y0, z0))

            cruz = cross( V3(ba.x, ba.y, ba.z), V3(ca.x, ca.y, ca.z))

            normal = (math.sqrt(cruz.x**2 + cruz.y**2 + cruz.z**2))

            try:
                nuevoVector = V3((cruz.x / normal), (cruz.y/normal), (cruz.z/normal))
            except:
                nuevoVector = V3(1,1,1)

            intensidad = pPunto(nuevoVector, luz)
            if intensidad > 1:
                intensidad = 1

            if intensidad < 0:
                intensidad = 0

            vt0x = verticeT[int(serieVT[0])][0]
            vt0y = verticeT[int(serieVT[0])][1]

            vt1x = verticeT[int(serieVT[1])][0]
            vt1y = verticeT[int(serieVT[1])][1]

            vt2x = verticeT[int(serieVT[2])][0]
            vt2y = verticeT[int(serieVT[2])][1]

            matriz1 = [x0,y0,z0,1]

            """
            print("MATRIZ 1")
            print(matriz1)
            print("-----------------")
            """

            matriz2 = [x1,y1,z1,1]
            
            """
            print("MATRIZ 2")
            print(matriz2)
            print("-----------------")
            """

            matriz3 = [x2,y2,z2,1]

            """
            print("MATRIZ 3")
            print(matriz3)
            print("-----------------")
            """

            vertice1 = multMATRIX(enviarOBJ, matriz1)

            """
            print("MULTIPLICACION CON enviarOBJ")
            print(vertice1)
            print("-----------------")
            """

            vertice2 = multMATRIX(enviarOBJ, matriz2)

            """
            print("MULTIPLICACION CON enviarOBJ")
            print(vertice2)
            print("-----------------")
            """


            vertice3 = multMATRIX(enviarOBJ, matriz3)
            
            """
            print("MULTIPLICACION CON enviarOBJ")
            print(vertice3)
            print("-----------------")
            """
            
            contador = 0
            while contador < 4:
                vertice1[contador] = abs( int(  vertice1[contador] / vertice1[len(vertice1)-1] ) )
                vertice2[contador] = abs( int( vertice2[contador] / vertice2[len(vertice2)-1]  ) )
                vertice3[contador] = abs( int( vertice3[contador] / vertice3[len(vertice3)-1]  ) )
                contador = contador + 1
            

            #son los valores x, y, z del vn 1
            vn0x = verticeN[int(serieCaras3[0])][0]
            #print(vn0x)
            vn0y = verticeN[int(serieCaras3[0])][1]
            #print(vn0y)
            vn0z = verticeN[int(serieCaras3[0])][2]
            #print(vn0z)

            #son los valores x, y, z del vn 2
            vn1x = verticeN[int(serieCaras3[1])][0]
            vn1y = verticeN[int(serieCaras3[1])][1]
            vn1z = verticeN[int(serieCaras3[1])][2]

            #son los valores x, y, z del vn 3
            vn2x = verticeN[int(serieCaras3[2])][0]
            vn2y = verticeN[int(serieCaras3[2])][1]
            vn2z = verticeN[int(serieCaras3[2])][2]



            r.triangle( V3(vertice1[0], vertice1[1], vertice1[2]), V3(vertice2[0], vertice2[1], vertice2[2]), V3(vertice3[0], vertice3[1], vertice3[2]), intensidad, V3(vn0x, vn0y, vn0z), V3(vn1x, vn1y, vn1z), V3(vn2x, vn2y, vn2z), luz)
            #r.triangle(V3(int(vertice1[0]/vertice1[len(vertice1)-1]), int(vertice1[1]/vertice1[len(vertice1)-1]), int(vertice1[2]/vertice1[len(vertice1)-1])), V3( int(vertice2[0]/vertice2[len(vertice2)-1]), int(vertice2[1]/vertice2[len(vertice2)-1]), int(vertice2[2]/vertice2[len(vertice2)-1])), V3(int(vertice3[0]/vertice3[len(vertice3)-1]), int(vertice3[1]/vertice3[len(vertice3)-1]), int(vertice3[2]/vertice3[len(vertice3)-1])), vt0x, vt0y, vt1x, vt1y, vt2x, vt2y, intensidad)
            #r.triangle( V3(vertice1[0], vertice1[1], vertice1[2]), V3(vertice2[0], vertice2[1], vertice2[2]), V3(vertice3[0], vertice3[1], vertice3[2])  , vt0x, vt0y, vt1x, vt1y, vt2x, vt2y, intensidad)

            
#A son las dos coordenadas de punto 1 de trinagulo
def bbox(A, B, C):
    xs = sorted([A.x, B.x, C.x])
    ys = sorted([A.y, B.y, C.y])

    return V2(xs[0], ys[0]), V2(xs[2], ys[2])


def barycentric(A, B, C, Punto):
    cx, cy, cz = cross(

        V3(B.x - A.x, C.x - A.x, A.x - Punto.x),
        
        V3(B.y - A.y, C.y - A.y, A.y - Punto.y)
    )

    #cz no puede ser < 1
    if cz == 0:
        return -1, -1, -1
        
    u = cx/cz
    v = cy/cz
    w = 1 - (u + v)
    return w, v, u

def resultado_de_matrices(modelM, viewM, projectionM, viewportM):
    a = multMATRIX4(modelM, viewM)

    """
    print("MULTIPLICACION MODEL Y VIEW")
    for x in a:
        print(x)
    """


    b = multMATRIX4(a, projectionM)

    """
    print("MULTIPLICACION RESULTADO PREVIO Y PROJECTION")
    for x in b:
        print(x)
    """


    c = multMATRIX4(b, viewportM)

    """
    print("MULTIPLICACION RESULTADO Y VIEWPORT")
    for x in c:
        print(x)
    return c
    """

#NUEVO MODEL MATRIX
def pruebaMATRIZ(x, y, z, traslacion, escala):
    rotx = x * 180/math.pi
    roty = y * 180/math.pi
    rotz = z * 180/math.pi

    matriz_rotacionX = [
            [1,     0,              0,              0],
            [0,math.cos(rotx), math.sin(rotx) * -1, 0],
            [0,math.sin(rotx), math.cos(rotx)     , 0],
            [0,     0,              0,              1]
            ]

    """
    print("MATRIZ ROTACION X")
    for x in matriz_rotacionX:
        print(x)
    """

    matriz_rotacionY = [
            [math.cos(roty)     , 0  ,math.sin(roty),0],
            [0                  , 1  ,0             ,0],
            [math.sin(roty * -1), 0  ,math.cos(roty),0],
            [0                  , 0  ,0             ,1]
            ]
    """
    for x in matriz_rotacionY:
        print(x)
    """

    matriz_rotacionZ = [
            [math.cos(rotz)     , math.sin(rotz) * -1  ,0,0],
            [math.sin(rotz)     , math.cos(rotz)       ,0,0],
            [0                  , 0                    ,1,0],
            [0                  , 0                    ,0,1]
            ]
    
    """
    print("MATRIZ ROTACION Z")
    for x in matriz_rotacionZ:
        print(x)
    """

    matriz_traslacion = [
            [1,0,0,traslacion.x],
            [0,1,0,traslacion.y],
            [0,0,1,traslacion.z],
            [0,0,0,1]
            ]

    """
    print("MATRIZ TRASLACION")
    for x in matriz_traslacion:
        print(x)
    """


    matriz_escala = [
            [escala.x,0 ,0 ,0],
            [0 ,escala.y,0 ,0],
            [0 ,0 ,escala.z,0],
            [0 ,0 ,0 ,1]
            ]
    
    """
    print("MATRIZ ESCALA")
    for x in matriz_escala:
        print(x)
    """

    matriz1 = multMATRIX4(matriz_rotacionX, matriz_rotacionY)
    matriz2 = multMATRIX4(matriz1, matriz_rotacionZ)
    matriz3 = multMATRIX4(matriz2, matriz_traslacion)
    matriz5 = multMATRIX4(matriz3, matriz_escala)
    matriz = matriz5


    return matriz

condicion = "a"
#t = Texture("rojo.bmp")
r = Bitmap(600, 400)
r.glClearColor(0.5, 0.3, 1)
r.glClear()
r.glColor(1, 1, 1)
r.glViewPort(0, 0, 600, 400)
r.glVertex()

while condicion != "0" :
    print("1. Medium Shot (tambien puede ser Dutch Angle)")
    print("2. Low Angle")
    print("3. High Angle")
    print("4. Dutch Angle (la opcion 1 tambien puede ser un Dutch Angle)")
    print("0. Salir")
    condicion = input("Ingrese la opción que se desea: ")

    if condicion == "1":
        modelM = pruebaMATRIZ(0,10,0, V3(-1200,-250,0), V3(2.9,2.9,2.9))
        viewM, projectionM = r.look(V3(0, 0, 5), V3(1,1,1), V3(0,0,1))

        matrizView = [
            [1,  0,  0,   0],
            [0,  1,  0,   0],
            [0,  0,  1, -1],
            [0,  0,  0,   1]
        ]

        viewportM = r.viewportMatrix(1,1)

        m = multMATRIX4(modelM, matrizView)
        m1 = multMATRIX4(m, projectionM)
        m2 = multMATRIX4(m1, viewportM)

        enviarOBJ = m1

        dataObj("porygonTextura.obj", enviarOBJ)

        r.write("camara.bmp")

    if condicion == "2":
        modelM = pruebaMATRIZ(1.7,5.3,4.1, V3(-800,-250,0), V3(2.7,2.7,2.7))
        viewM, projectionM = r.look(V3(0, 0, 5), V3(1,1,1), V3(0,0,1))

        matrizView = [
            [1,  0,  0,   0],
            [0,  1,  0,   0],
            [0,  0,  1, -1],
            [0,  0,  0,   1]
        ]

        viewportM = r.viewportMatrix(1,1)

        m = multMATRIX4(modelM, matrizView)
        m1 = multMATRIX4(m, projectionM)
        m2 = multMATRIX4(m1, viewportM)

        enviarOBJ = m1

        dataObj("porygonTextura.obj", enviarOBJ)

        r.write("camara.bmp")

    if condicion == "3":
        modelM = pruebaMATRIZ(0,20.1,4.9, V3(-200,-200,0), V3(2,2,2))
        viewM, projectionM = r.look(V3(0, 0, 5), V3(1,1,1), V3(0,0,1))

        matrizView = [
            [1,  0,  0,   0],
            [0,  1,  0,   0],
            [0,  0,  1, -1],
            [0,  0,  0,   1]
        ]

        viewportM = r.viewportMatrix(1,1)

        m = multMATRIX4(modelM, matrizView)
        m1 = multMATRIX4(m, projectionM)
        m2 = multMATRIX4(m1, viewportM)

        enviarOBJ = m1

        dataObj("porygonTextura.obj", enviarOBJ)

        r.write("camara.bmp")

    if condicion == "4":
        modelM = pruebaMATRIZ(0,5,0.1, V3(-300,0,0), V3(1.5, 1.5, 1.5))
        viewM, projectionM = r.look(V3(0, 0, 5), V3(1,1,1), V3(0,0,1))

        matrizView = [
            [1,  0,  0,   0],
            [0,  1,  0,   0],
            [0,  0,  1, -1],
            [0,  0,  0,   1]
        ]

        viewportM = r.viewportMatrix(1,1)

        m = multMATRIX4(modelM, matrizView)
        m1 = multMATRIX4(m, projectionM)
        m2 = multMATRIX4(m1, viewportM)

        enviarOBJ = m1

        dataObj("porygonTextura.obj", enviarOBJ)

        r.write("camara.bmp")
#modelM = pruebaMATRIZ(0,10,0, V3(-1200,-300,0), V3(2.9,2.9,2.9))
#viewM, projectionM = r.look(V3(0, 0, 5), V3(1,1,1), V3(0,0,1))

#print("*******************")
#print("VIEWPORT MATRIX")
#for x in viewportM:
#    print(x)
#print("*******************")

#enviarOBJ = resultado_de_matrices(modelM, viewM, projectionM, viewportM)

#enviarOBJ = modelM
#leerMTL("porygonTextura.mtl")
#dataObj("porygonTextura.obj", enviarOBJ)


