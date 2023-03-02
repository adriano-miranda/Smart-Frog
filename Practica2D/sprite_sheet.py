import pygame 

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image
    
    #funcion para obtener un sprite de la hoja 
    def get_image(self, frame_fila, frame_col, width, height, scale):
        image = pygame.Surface((width,height)).convert_alpha()
        image.blit(self.sheet, (0,0), ((frame_fila*width),(frame_col*height), width, height))
        image = pygame.transform.scale(image, (width*scale, height*scale))
        colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey)
    
        return image
