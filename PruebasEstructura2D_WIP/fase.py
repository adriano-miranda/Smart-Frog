# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
from pygame.locals import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

VELOCIDAD_SOL = 0.1 # Pixeles por milisegundo

# Los bordes de la pantalla para hacer scroll
MINIMO_X_JUGADOR = 5
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR
MINIMO_Y_JUGADOR = 5
MAXIMO_Y_JUGADOR = ALTO_PANTALLA - MINIMO_Y_JUGADOR

# -------------------------------------------------
# Clase Fase

class Fase(Escena):
    def __init__(self, director):

        # Habria que pasarle como parámetro el número de fase, a partir del cual se cargue
        #  un fichero donde este la configuracion de esa fase en concreto, con cosas como
        #   - Nombre del archivo con el decorado
        #   - Posiciones de las plataformas
        #   - Posiciones de los enemigos
        #   - Posiciones de inicio de los jugadores
        #  etc.
        # Y cargar esa configuracion del archivo en lugar de ponerla a mano, como aqui abajo
        # De esta forma, se podrian tener muchas fases distintas con esta clase

        # Primero invocamos al constructor de la clase padre
        Escena.__init__(self, director)

        # Creamos el decorado y el fondo
        self.decorado = Decorado()
        self.fondo = Agua()

        # Que parte del decorado estamos visualizando
        self.scrollx = 0
        self.scrolly = 0
        #  En ese caso solo hay scroll horizontal
        #  Si ademas lo hubiese vertical, seria self.scroll = (0, 0)

        # Creamos los sprites de los jugadores
        self.jugador = Jugador()
        self.grupoJugadores = pygame.sprite.Group(self.jugador)

        # Ponemos a los jugadores en sus posiciones iniciales
        self.jugador.establecerPosicion((200, 551))

        # Creamos las plataformas del decorado
        # La plataforma que conforma todo el suelo
        plataformaSuelo = Plataforma(pygame.Rect(0, 550, 1200, 15))
        # La plataforma del techo del edificio
        #plataformaCasa = Plataforma(pygame.Rect(870, 417, 200, 10))
        # y el grupo con las mismas
        self.grupoPlataformas = pygame.sprite.Group(plataformaSuelo)

        # Y los enemigos que tendran en este decorado
        #enemigo1 = Sniper()
        #enemigo1.establecerPosicion((1000, 418))

        # Creamos un grupo con los enemigos
        self.grupoEnemigos = pygame.sprite.Group( ) #enemigo1 )

        # Creamos un grupo con los Sprites que se mueven
        #  En este caso, solo los personajes, pero podría haber más (proyectiles, etc.)
        self.grupoSpritesDinamicos = pygame.sprite.Group(self.jugador)
        # Creamos otro grupo con todos los Sprites
        self.grupoSprites = pygame.sprite.Group(self.jugador, plataformaSuelo)



        
    # Devuelve True o False según se ha tenido que desplazar el scroll
    def actualizarScrollOrdenados(self, jugador):

        # Si el jugador se encuentra más allá del borde superior
        if (jugador.rect.top<MINIMO_Y_JUGADOR):
            print("ARRIBA: ", jugador.posicion)

            # Se calcula cuantos pixeles esta fuera del borde
            desplazamiento = MINIMO_Y_JUGADOR - jugador.rect.top

            # Si el escenario ya está a la izquierda del todo, no lo movemos mas
            if self.scrolly <= 0:
                self.scrolly = 0

                # En su lugar, colocamos al jugador que esté más a la izquierda a la izquierda de todo
                jugador.establecerPosicion((jugador.posicion[1], MINIMO_Y_JUGADOR))

                return False; # No se ha actualizado el scroll

            # Si se puede hacer scroll a la izquierda
            else:
                # Calculamos el nivel de scroll actual: el anterior - desplazamiento
                #  (desplazamos a la izquierda)
                self.scrolly = self.scrolly - desplazamiento;

                return True; # Se ha actualizado el scroll

        # Si el jugador se encuentra más allá del borde inferior
        if (jugador.rect.bottom>MAXIMO_Y_JUGADOR):
            print("ABAJO: ", jugador.posicion)

            # Se calcula cuantos pixeles esta fuera del borde
            desplazamiento = jugador.rect.bottom - MAXIMO_Y_JUGADOR

            # Si el escenario ya está abajo del todo, no lo movemos mas
            if self.scrolly + ALTO_PANTALLA >= self.fondo.rect.bottom:
                self.scrolly = self.fondo.rect.bottom - ALTO_PANTALLA

                # En su lugar, colocamos al jugador que esté más a la derecha a la derecha de todo
                jugador.establecerPosicion((jugador.posicion[1], self.scrolly+MAXIMO_Y_JUGADOR-jugador.rect.height))

                return False; # No se ha actualizado el scroll


            # Si se puede hacer scroll abajo
            else:

                # Calculamos el nivel de scroll actual: el anterior + desplazamiento
                #  (desplazamos abajo)
                self.scrolly = self.scrolly + desplazamiento;

                return True; # Se ha actualizado el scroll

        # Si el jugador se encuentra más allá del borde izquierdo
        if (jugador.rect.left<MINIMO_X_JUGADOR):

            # Se calcula cuantos pixeles esta fuera del borde
            desplazamiento = MINIMO_X_JUGADOR - jugador.rect.left

            # Si el escenario ya está a la izquierda del todo, no lo movemos mas
            if self.scrollx <= 0:
                self.scrollx = 0

                # En su lugar, colocamos al jugador que esté más a la izquierda a la izquierda de todo
                jugador.establecerPosicion((MINIMO_X_JUGADOR, jugador.posicion[1]))

                return False; # No se ha actualizado el scroll

            # Si se puede hacer scroll a la izquierda
            else:
                # Calculamos el nivel de scroll actual: el anterior - desplazamiento
                #  (desplazamos a la izquierda)
                self.scrollx = self.scrollx - desplazamiento;

                return True; # Se ha actualizado el scroll

        # Si el jugador se encuentra más allá del borde derecho
        if (jugador.rect.right>MAXIMO_X_JUGADOR):

            # Se calcula cuantos pixeles esta fuera del borde
            desplazamiento = jugador.rect.right - MAXIMO_X_JUGADOR

            # Si el escenario ya está a la derecha del todo, no lo movemos mas
            if self.scrollx + ANCHO_PANTALLA >= self.fondo.rect.right:
                self.scrollx = self.fondo.rect.right - ANCHO_PANTALLA

                # En su lugar, colocamos al jugador que esté más a la derecha a la derecha de todo
                jugador.establecerPosicion((self.scrollx+MAXIMO_X_JUGADOR-jugador.rect.width, jugador.posicion[1]))

                return False; # No se ha actualizado el scroll


            # Si se puede hacer scroll a la derecha
            else:

                # Calculamos el nivel de scroll actual: el anterior + desplazamiento
                #  (desplazamos a la derecha)
                self.scrollx = self.scrollx + desplazamiento;

                return True; # Se ha actualizado el scroll

        # Si el jugador está dentro los límites de la pantalla
        return False;


    def actualizarScroll(self, jugador):
        # Se ordenan los jugadores según el eje x, y se mira si hay que actualizar el scroll
        cambioScroll = self.actualizarScrollOrdenados(jugador)

        # Si se cambio el scroll, se desplazan todos los Sprites y el decorado
        if cambioScroll:
            # Actualizamos la posición en pantalla de todos los Sprites según el scroll actual
            for sprite in iter(self.grupoSprites):
                sprite.establecerPosicionPantalla((self.scrolly, 0))

            # Ademas, actualizamos el decorado para que se muestre una parte distinta
            self.decorado.update(self.scrolly)



    # Se actualiza el decorado, realizando las siguientes acciones:
    #  Se indica para los personajes no jugadores qué movimiento desean realizar según su IA
    #  Se mueven los sprites dinámicos, todos a la vez
    #  Se comprueba si hay colision entre algun jugador y algun enemigo
    #  Se comprueba si algún jugador ha salido de la pantalla, y se actualiza el scroll en consecuencia
    #     Actualizar el scroll implica tener que desplazar todos los sprites por pantalla
    #  Se actualiza la posicion del sol y el color del cielo
    def update(self, tiempo):

        # Primero, se indican las acciones que van a hacer los enemigos segun como esten los jugadores
        for enemigo in iter(self.grupoEnemigos):
            enemigo.mover_cpu(self.jugador)
        # Esta operación es aplicable también a cualquier Sprite que tenga algún tipo de IA
        # En el caso de los jugadores, esto ya se ha realizado

        # Actualizamos los Sprites dinamicos
        # De esta forma, se simula que cambian todos a la vez
        # Esta operación de update ya comprueba que los movimientos sean correctos
        #  y, si lo son, realiza el movimiento de los Sprites
        self.grupoSpritesDinamicos.update(self.grupoPlataformas, tiempo)
        # Dentro del update ya se comprueba que todos los movimientos son válidos
        #  (que no choque con paredes, etc.)

        # Los Sprites que no se mueven no hace falta actualizarlos,
        #  si se actualiza el scroll, sus posiciones en pantalla se actualizan más abajo
        # En cambio, sí haría falta actualizar los Sprites que no se mueven pero que tienen que
        #  mostrar alguna animación

        # Comprobamos si hay colision entre algun jugador y algun enemigo
        # Se comprueba la colision entre ambos grupos
        # Si la hay, indicamos que se ha finalizado la fase
        if pygame.sprite.groupcollide(self.grupoJugadores, self.grupoEnemigos, False, False)!={}:
            # Se le dice al director que salga de esta escena y ejecute la siguiente en la pila
            self.director.salirEscena()

        # Actualizamos el scroll
        self.actualizarScroll(self.jugador)
  
        # Actualizamos el fondo:
        #  la posicion del sol y el color del cielo
        self.fondo.update(tiempo)

        
    def dibujar(self, pantalla):
        # Ponemos primero el fondo
        self.fondo.dibujar(pantalla)
        # Después el decorado
        self.decorado.dibujar(pantalla)
        # Luego los Sprites
        self.grupoSprites.draw(pantalla)


    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        teclasPulsadas = pygame.key.get_pressed()
        self.jugador.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE)
        #self.jugador2.mover(teclasPulsadas, K_w,  K_s,    K_a,    K_d)

# -------------------------------------------------
# Clase Plataforma

#class Plataforma(pygame.sprite.Sprite):
class Plataforma(MiSprite):
    def __init__(self,rectangulo):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = pygame.Surface((0, 0))


# -------------------------------------------------
# Clase Cielo

class Cielo:
    def __init__(self):
        self.sol = GestorRecursos.CargarImagen('sol.png', -1)
        self.sol = pygame.transform.scale(self.sol, (300, 200))

        self.rect = self.sol.get_rect()
        self.posicionx = 0 # El lado izquierdo de la subimagen que se esta visualizando
        self.update(0)

    def update(self, tiempo):
        self.posicionx += VELOCIDAD_SOL * tiempo
        if (self.posicionx - self.rect.width >= ANCHO_PANTALLA):
            self.posicionx = 0
        self.rect.right = self.posicionx
        # Calculamos el color del cielo
        if self.posicionx >= ((self.rect.width + ANCHO_PANTALLA) / 2):
            ratio = 2 * ((self.rect.width + ANCHO_PANTALLA) - self.posicionx) / (self.rect.width + ANCHO_PANTALLA)
        else:
            ratio = 2 * self.posicionx / (self.rect.width + ANCHO_PANTALLA)
        self.colorCielo = (100*ratio, 200*ratio, 255)
        
    def dibujar(self,pantalla):
        # Dibujamos el color del cielo
        pantalla.fill(self.colorCielo)
        # Y ponemos el sol
        pantalla.blit(self.sol, self.rect)


# -------------------------------------------------
# Clase Decorado

class Decorado:
    def __init__(self):
        self.imagen = GestorRecursos.CargarImagen('decorado0.png', -1)
        self.imagen = pygame.transform.scale(self.imagen, (1200, 600))

        self.rect = self.imagen.get_rect()
        self.rect.left = ANCHO_PANTALLA

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto

    def update(self, scrollx):
        self.rectSubimagen.left = scrollx

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)

# -------------------------------------------------
# Clase Agua

class Agua:
    def __init__(self):
        self.tile = GestorRecursos.CargarImagen('water_tile.jpg', 0) # Cargar textura de fondo
        self.imagen = pygame.Surface((1400, 800)) # Crear capa de fondo
        self.imagen = self.imagen.convert()

        # Rellenar capa de fondo con la imagen
        for x in range(0, 800, self.tile.get_width()):
            for y in range(0, 1400, self.tile.get_height()):
                self.imagen.blit(self.tile, (x, y))

        self.rect = self.imagen.get_rect()

    def update(self, tiempo):
        return

    def dibujar(self, pantalla):
       pantalla.blit(self.imagen, self.rect)
