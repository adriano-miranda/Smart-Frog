from pygame import *
from gestorRecursos import *

class ElementoGUI(sprite.Sprite):
    def __init__(self, position, archivoImagen):
        pygame.sprite.Sprite.__init__(self)
        self.position_x, self.position_y = position
        self.imagen = GestorRecursos.CargarImagen(archivoImagen,-1)
        self.imagen = self.imagen.convert_alpha()
        pygame.transform.scale(self.imagen, (125, 25))
        self.rect = (self.position_x, self.position_y, 125, 5)

    def update(self):
        pass

    def draw(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

class AvanceSalto(ElementoGUI):
    def __init__(self, position, archivoImagen):
        super().__init__(position, archivoImagen)
        pygame.transform.scale(self.imagen, (10, 20))