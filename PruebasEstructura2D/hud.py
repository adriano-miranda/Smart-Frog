from pygame import *
from gestorRecursos import *
from typing import Tuple

class paqueteVidas():
    '''Su utilidad es la de proporcionar información de una manera compacta al HUD de vidas y tiene los siguientes campos:
      Quantity = cantidad de vidas a modificar
      Operation = tipo de operación a realizar
      Grupo = grupo a traves del cual se mostrarán las actualizaciones"
    '''
    QUITAR = 1
    AÑADIR = 2

    def __init__(self, quantity, operation, grupo = None) -> None:
        self.q = quantity
        self.operation = operation
        self.group = grupo
        

class Listener(sprite.Sprite):
    def run(self, datos):
        pass

class HUD(Listener):

    # position: La posición es una tupla de enteros
    # archivoImagen: El nombre del archivo o la ruta
    #       relativa junto con el nombre dentro de la carpeta "imagenes"
    def __init__(self, position: Tuple[int], archivoImagen, scaleX, scaleY):
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect(position[0], position[1], scaleX, scaleY)
        self.position = position
        self.image = GestorRecursos.CargarImagen(archivoImagen, 0)
        self.image = self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (scaleX, scaleY))

    def hide(self):
        self.kill()

    def show(self, grupo: sprite.Group):
        grupo.add(self)
    
    def update(self):
        pass

    def run(self, datos):
        pass

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.position)

class HUDVidas(HUD):
    
    # remainingLives = Número de vidas restantes
    # totalLives = Número de vidas totales que representa el HUD
    # lives[...] = Lista con los HUD's, cada uno de los cuales, representa una vida
    def __init__(self, position: Tuple[int], archivoImagen, scaleX, scaleY, distancia, num_lives):
        self.lives: list[HUD] = []

        for i in range(num_lives):
            self.lives.append(HUD((position[0]+distancia*i, position[1]), archivoImagen, scaleX, scaleY))
        
        self.remainingLives = num_lives
        self.totalLives = num_lives
    
    # PreCD: Se hace entre la llamada al constructor HUDVidas(...) y cualquier otra
    # Añade al grupo todas las vidas
    def addToGroup(self, grupo: sprite.Group):
        self.grupo = grupo
        grupo.add(self.lives[:self.totalLives])

    # Remove one life
    def removeLife(self):
        self.lives[self.remainingLives-1].kill()
        self.remainingLives = max(0, self.remainingLives - 1)

    # Remove all lives
    def hide(self):
        for l in self.lives:
            l.kill()
        self.remainingLives = 0

    # Add quantity lives
    def addLife(self, grupo: sprite.Group, quantity=1):
        if not (self.remainingLives == self.totalLives):
            aux = min(self.totalLives, self.remainingLives + quantity)
            grupo.add(self.lives[self.remainingLives:aux])
            self.remainingLives = aux

    def show(self, grupo: sprite.Group):
        self.addLife(grupo, quantity=self.totalLives)
    
    def setLives(self, q, grupo: sprite.Group = None):
        if self.remainingLives == q:
            return
        if self.remainingLives > q: # Restar
            for i in range(self.remainingLives - q):
                self.removeLife()
                return
        if grupo is None:
            self.addLife(self.grupo, q - self.remainingLives)
        else:
            self.addLife(grupo, q - self.remainingLives)
    
    def run(self, datos):
        aux = datos
        if datos<0:
            aux = 0
        elif datos>self.totalLives:
            aux = self.totalLives
        self.setLives(aux)
        # if type(datos) == type(paqueteVidas):
        #     if(datos.operacion == paqueteVidas.AÑADIR):
        #         if datos.group is None:
        #             self.addLife(self.grupo, datos.quantity)
        #         else:
        #             self.addLife(datos.group, datos.quantity)
        #     elif(datos.operacion == paqueteVidas.QUITAR):
        #         

    

class BarraCarga(HUD):
    def __init__(self, position, barraProgreso, scaleX, scaleY, max_time):
        super().__init__(position, barraProgreso, 1, scaleY)
        self.progress_bar_width = max(1, scaleX)
        self.progress_bar_height = scaleY
        self.maxTime = max_time
    
    def hide(self):
        self.kill()
    
    def show(self, grupo: sprite.Group):
        grupo.add(self)

    def run(self, datos: float):
        maxT = self.maxTime * 1000
        progress = min((datos), maxT) / maxT  # Calcula el porcentaje de carga del salto
        inner_width = int(progress * (self.progress_bar_width - 2))
        #inner_rect = pygame.Rect((self.position[0] + 1, self.position[1] + 1), (inner_width, self.progress_bar_height - 2))
        self.image = pygame.transform.scale(self.image, (max(1, inner_width), self.progress_bar_height))
