from pygame import *
from pygame.locals import *
from gestorRecursos import *

# cargamos sonidos
pygame.mixer.pre_init(44100, 16, 2, 512)   # el archivo tiene que estar formateado con exactamente la misma
                                            # frecuencia, bitrate y canales para que pueda abrirlo
pygame.mixer.init()
self.caidaAgua = GestorRecursos.CargarSonido("Heavy-Splash.ogg")
self.croak = GestorRecursos.CargarSonido("croak.ogg")
self.kaorc = GestorRecursos.CargarSonido("kaorc.ogg")
pygame.mixer.set_reserved(4) # reservamos canales para efectos de sonido
self.canal_reservado_0 = pygame.mixer.Channel(0)
self.canal_reservado_1 = pygame.mixer.Channel(1)
self.canal_reservado_2 = pygame.mixer.Channel(2)

# musiquita
pygame.mixer.music.load("sonidos/route11_-_hg_ss.ogg")
pygame.mixer.music.set_volume(0.2) # valores entre 0.0 y 1.0
pygame.mixer.music.play(-1) # el -1 hace que suene en bucle