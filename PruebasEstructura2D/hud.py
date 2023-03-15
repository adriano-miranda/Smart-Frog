from pygame import *
from gestorRecursos import *

class Listener(sprite.Sprite):
    def run(datos):
        pass

class HUD(Listener):

    # position: La posición es una tupla de enteros
    # archivoImagen: El nombre del archivo o la ruta
    #       relativa junto con el nombre dentro de la carpeta "imagenes"
    def __init__(self, position: tuple[int], archivoImagen, scaleX, scaleY):
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

    # def run(datos):
    #     pass

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.position)

class HUDVidas(HUD):
    
    # remainingLives = Número de vidas restantes
    # totalLives = Número de vidas totales que representa el HUD
    # lives[...] = Lista con los HUD's, cada uno de los cuales, representa una vida
    def __init__(self, position: tuple[int], archivoImagen, scaleX, scaleY, distancia, num_lives):
        self.lives: list[HUD] = []

        for i in range(num_lives):
            self.lives.append(HUD((position[0]+distancia*i, position[1]), archivoImagen, scaleX, scaleY))
        
        self.remainingLives = num_lives
        self.totalLives = num_lives
    
    # PreCD: Se hace entre la llamada al constructor HUDVidas(...) y cualquier otra
    # Añade al grupo todas las vidas
    def addToGroup(self, grupo: sprite.Group):
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
        if not (self.remainingLifes == self.totalLives):
            aux = min(self.totalLives, self.remainingLives + quantity)
            grupo.add(self.lives[self.remainingLives:aux])
            self.remainingLives = aux

    def show(self, grupo: sprite.Group):
        self.addLife(grupo, quantity=self.totalLives)

    

# class BarraCarga(HUD):
#     def __init__(self, position1, position2, fondoBarra, barraProgreso):
#         self.position1 = position1
#         self.position2 = position2
#         self.imagen1 = GestorRecursos.CargarImagen(fondoBarra, -1)
#         self.imagen2 = GestorRecursos.CargarImagen(barraProgreso, -1)
#         pygame.transform.scale(self.imagen, (10, 20))