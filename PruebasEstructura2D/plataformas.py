 # -*- encoding: utf-8 -*-

from pygame import *
from pygame.locals import *
from escena import *
from gestorRecursos import *
from personajes import *

# Clase Mosca
class Insecto(MiSprite):
    def __init__(self,rectangulo, image,scaleX, scaleY, score):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        #Puntuación que suma el insecto al ser comido
        self.score = score
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = GestorRecursos.CargarImagen(image, 0)
        self.image = pygame.transform.scale(self.image, (scaleX, scaleY))
        


#class Plataforma(pygame.sprite.Sprite):
class Plataforma(MiSprite):
    def __init__(self,rectangulo, imagen, scaleX, scaleY):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = GestorRecursos.CargarImagen(imagen, 0)
        #self.image.set_colorkey(0)
        self.image = pygame.transform.scale(self.image, (scaleX, scaleY))

#class Plataforma(pygame.sprite.Sprite):
class Plataforma2(pygame.sprite.Sprite):
    def __init__(self,rectangulo, imagen, scaleX, scaleY):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        #self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = GestorRecursos.CargarImagen(imagen, 0)
        #self.image.set_colorkey(0)
        self.image = pygame.transform.scale(self.image, (scaleX, scaleY))

# plataforma Nenufar
class Nenufar(MiSprite):
    def __init__(self, rectangulo):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = GestorRecursos.CargarImagen('nenufar.png', -1)
        #self.image.set_colorkey(0)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

# plataforma dNenufar
class DNenufar(MiSprite):
    def __init__(self, rectangulo, tiempoActivo=180):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = GestorRecursos.CargarImagen('dNenufar.png', -1)
        #self.image.set_colorkey(0)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

        self.visible = True
        self.pisado = False
        self.tiempoActivo = tiempoActivo
        self.timer = 0

    def update(self, jugador):
        if(pygame.sprite.spritecollide(self, [jugador], False)):
            self.pisado = True

        if(self.pisado):
            self.timer += 1
            if self.timer >= self.tiempoActivo:
                self.visible = False
                self.pisado = False

        elif(not self.pisado and self.timer > 0):
            self.timer -= 1
            if self.timer <= 0:
                self.visible = True
                self.timer = 0

# -------------------------------------------------
# Clase Fondo

class Fondo:
    def __init__(self, imagen, alto=1400):
        self.tile = GestorRecursos.CargarImagen(imagen, 0) # Cargar textura de fondo
        self.imagen = pygame.Surface((800, alto)) # Crear capa de fondo
        self.imagen = self.imagen.convert()

        # Rellenar capa de fondo con la imagen
        for x in range(0, self.imagen.get_width(), self.tile.get_width()):
            for y in range(0, self.imagen.get_height(), self.tile.get_height()):
                self.imagen.blit(self.tile, (x, y))

        self.rect = self.imagen.get_rect()
        self.rect.right = ANCHO_PANTALLA

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.top = 0 # El scroll vertical empieza en la posicion 0 por defecto


    def update(self, scrolly):
        self.rectSubimagen.top = scrolly

    def dibujar(self, pantalla):
       pantalla.blit(self.imagen, self.rect, self.rectSubimagen)
