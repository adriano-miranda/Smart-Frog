# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from escena import *
from gestorRecursos import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

# Movimientos
IZQUIERDA = 0
DERECHA = 1
ARRIBA = 2
ABAJO = 3
SALTO = 4
QUIETO = 5

M_IZQUIERDA = [1, 0, 0, 0, 0]
M_DERECHA   = [0, 1, 0, 0, 0]
M_ARRIBA    = [0, 0, 1, 0, 0]
M_ABAJO     = [0, 0, 0, 1, 0]
M_SALTO     = [0, 0, 0, 0, 1]
M_QUIETO    = [0, 0, 0, 0, 0]

#Posturas
SPRITE_QUIETO = 0
SPRITE_ANDANDO = 1
SPRITE_SALTANDO = 2

IDLE_UP_SPRITE = 0
IDLE_DOWN_SPRITE = 1
IDLE_SIDE_SPRITE = 2
MOVING_UP_SPRITE = 3
MOVING_DOWN_SPRITE = 4
MOVING_SIDE_SPRITE = 5
JUMPING_UP_SPRITE = 6
JUMPING_DOWN_SPRITE = 7
JUMPING_SIDE_SPRITE = 8


# Velocidades de los distintos personajes
VELOCIDAD_JUGADOR = 0.2 # Pixeles por milisegundo
VELOCIDAD_SALTO_JUGADOR = 0.3 # Pixeles por milisegundo
RETARDO_ANIMACION_JUGADOR = [5, 5] # updates que durará cada imagen del personaje
                              # debería de ser un valor distinto para cada postura

VELOCIDAD_PAJARO = 0.2 # Pixeles por milisegundo
RETARDO_ANIMACION_PAJARO = 3 # updates que durará cada imagen del personaje
                             # debería de ser un valor distinto para cada postura


# -------------------------------------------------
# -------------------------------------------------
# Clases de los objetos del juego
# -------------------------------------------------
# -------------------------------------------------


# -------------------------------------------------
# Clase MiSprite
class MiSprite(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.posicion = (0, 0)
        self.velocidad = (0, 0)
        self.scroll   = (0, 0)

    def establecerPosicion(self, posicion):
        self.posicion = posicion
        self.rect.left = self.posicion[0] - self.scroll[0]
        self.rect.bottom = self.posicion[1] - self.scroll[1]

    def establecerPosicionPantalla(self, scrollFondo):
        self.scroll = scrollFondo;
        (scrollx, scrolly) = self.scroll;
        (posx, posy) = self.posicion;
        self.rect.left = posx - scrollx;
        self.rect.bottom = posy - scrolly;

    def incrementarPosicion(self, incremento):
        (posx, posy) = self.posicion
        (incrementox, incrementoy) = incremento
        self.establecerPosicion((posx+incrementox, posy+incrementoy))

    def update(self, tiempo):
        incrementox = self.velocidad[0]*tiempo
        incrementoy = self.velocidad[1]*tiempo
        self.incrementarPosicion((incrementox, incrementoy))



# -------------------------------------------------
# Clases Personaje

#class Personaje(pygame.sprite.Sprite):
class Personaje(MiSprite):
    "Cualquier personaje del juego"

    # Parametros pasados al constructor de esta clase:
    #  Archivo con la hoja de Sprites
    #  Archivo con las coordenadoas dentro de la hoja
    #  Numero de imagenes en cada postura
    #  Velocidad de caminar y de salto
    #  Retardo para mostrar la animacion del personaje
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidadCarrera, velocidadSalto, retardoAnimacion):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self);

        # Se carga la hoja
        self.hoja = GestorRecursos.CargarImagen(archivoImagen,-1)
        self.hoja = self.hoja.convert_alpha()

        # El movimiento que el usuario quiere realizar
        self.movimiento       = [0, 0, 0, 0, 0]
        self.movimientoPasado = [1, 1, 1, 1, 1]
        
        # Lado hacia el que esta mirando
        self.mirando = ARRIBA

        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()
        self.numPostura = 1;
        self.numImagenPostura = 0;
        cont = 0;
        self.coordenadasHoja = [];
        for linea in range(0, len(numImagenes)):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0;

        # En que postura esta inicialmente
        self.numPostura = IDLE_UP_SPRITE

        # El rectangulo del Sprite
        self.rect = pygame.Rect(100,100,self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

        # Las velocidades de caminar y salto
        self.velocidadCarrera = velocidadCarrera
        self.velocidadSalto = velocidadSalto

        # El retardo en la animacion del personaje (podria y deberia ser distinto para cada postura)
        self.retardoAnimacion = retardoAnimacion
        self.moviendose = 0

        # Y actualizamos la postura del Sprite inicial, llamando al metodo correspondiente
        self.actualizarPostura()


    # Metodo base para realizar el movimiento: simplemente se le indica cual va a hacer, y lo almacena
    def mover(self, movimiento: list):
        # if movimiento == ARRIBA:
        #     # Si estamos en el aire y el personaje quiere saltar, ignoramos este movimiento
        #     if self.numPostura == SPRITE_SALTANDO:
        #         self.movimiento = QUIETO
        #     else:
        #         self.movimiento = ARRIBA
        # else:
        self.movimientoPasado = self.movimiento
        self.movimiento = movimiento


    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = self.retardoAnimacion[self.moviendose]
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0;
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1
            self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            # Si esta mirando a la izquierda, cogemos la porcion de la hoja
            if self.mirando == IZQUIERDA:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.mirando == DERECHA:
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)

    def salto(self, distance, velocidad):
        if self.mirando == ARRIBA:
            return ((self.posicion[0], max(0, self.posicion[1]-distance))), 0, -velocidad
        if self.mirando == ABAJO:
            return ((self.posicion[0], min(ALTO_PANTALLA, self.posicion[1]+distance))), 0, velocidad
        if self.mirando == DERECHA:
            return ((min(ANCHO_PANTALLA, self.posicion[0] + distance), self.posicion[1])), velocidad, 0
        if self.mirando == IZQUIERDA:
            return ((max(0, self.posicion[0] - distance), self.posicion[1])), -velocidad, 0

    def reachedPosition(self):
        if self.mirando == ARRIBA:
            return self.posicion[1]<=self.pos_final[1]
        if self.mirando == ABAJO:
            return self.posicion[1]>=self.pos_final[1]
        if self.mirando == DERECHA:
            return self.posicion[0]>=self.pos_final[0]
        if self.mirando == IZQUIERDA:
            return self.posicion[0]<=self.pos_final[0]


    def sumav(self, a: list, b: list):
        c = b.copy()
        for n in range(b.__len__()):
            c[n] = a[n] + b[n]
        return c
    
    def update(self, grupoPlataformas, tiempo):

        MAX_TIME = 1
        MAX_JUMP_DISTANCE = 160
        JUMP_V = 0.15
        

        # Las velocidades a las que iba hasta este momento
        (velocidadx, velocidady) = self.velocidad

        ##  self.movimiento and self.movimientoPasado
        if (self.isJumping):
            if (self.reachedPosition()):
                self.isJumping = False
        elif (not self.isLoadingJump and self.movimiento[4]): # Quiero cargar salto
            self.isLoadingJump = True
            self.t0 = tiempo
        elif (self.isLoadingJump and self.movimiento[4]):
            self.t0 += tiempo
        elif (self.isLoadingJump and (not self.movimiento[4])): # Ahora si salto
            self.isLoadingJump = False
            self.isJumping = True
            if(self.mirando == ARRIBA):
                self.numPostura = JUMPING_UP_SPRITE
            elif(self.mirando == ABAJO):
                self.numPostura = JUMPING_DOWN_SPRITE
            elif(self.mirando == IZQUIERDA) or (self.mirando == DERECHA):
                self.numPostura = JUMPING_SIDE_SPRITE
            jump_distance = (((self.t0) / 1000) / MAX_TIME) * MAX_JUMP_DISTANCE
            jump_distance = min(MAX_JUMP_DISTANCE, jump_distance)
            self.pos_final, velocidadx, velocidady = self.salto(jump_distance, JUMP_V)
            
        elif (self.movimiento == self.sumav(M_IZQUIERDA, M_ARRIBA)):
            self.movimiento = self.movimientoPasado

        elif (self.movimiento == self.sumav(M_IZQUIERDA, M_ABAJO)):
            self.movimiento = self.movimientoPasado

        elif (self.movimiento == self.sumav(M_DERECHA, M_ARRIBA)):
            self.movimiento = self.movimientoPasado
            
        elif (self.movimiento == self.sumav(M_DERECHA, M_ABAJO)):
            self.movimiento = self.movimientoPasado

        elif (self.movimiento == M_ARRIBA):
            # La postura actual sera estar saltando
            self.numPostura = MOVING_UP_SPRITE
            self.mirando = ARRIBA
            # Le imprimimos una velocidad en el eje y
            velocidady = -self.velocidadCarrera
            velocidadx = 0
            self.moviendose = 1

        elif (self.movimiento == M_ABAJO):
            # La postura actual sera estar saltando
            self.numPostura = MOVING_DOWN_SPRITE
            self.mirando = ABAJO
            # Le imprimimos una velocidad en el eje y
            velocidady = +self.velocidadCarrera
            velocidadx = 0
            self.moviendose = 1

        elif (self.movimiento == self.sumav(M_ARRIBA, M_ABAJO)):
            # Si no estamos saltando, la postura actual será estar quieto
            if self.numPostura == MOVING_UP_SPRITE:
                self.numPostura = IDLE_UP_SPRITE

            elif self.numPostura == MOVING_DOWN_SPRITE:
                self.numPostura = IDLE_DOWN_SPRITE

            elif self.numPostura == MOVING_SIDE_SPRITE:
                self.numPostura = IDLE_SIDE_SPRITE

            velocidadx = 0
            velocidady = 0
            self.moviendose = 0

        elif (self.movimiento == M_DERECHA):
            velocidadx = self.velocidadCarrera
            velocidady = 0
            self.numPostura = MOVING_SIDE_SPRITE
            self.mirando = DERECHA
            self.moviendose = 1

        elif (self.movimiento == M_IZQUIERDA):
            velocidadx = -self.velocidadCarrera
            velocidady = 0
            self.numPostura = MOVING_SIDE_SPRITE
            self.mirando = IZQUIERDA
            self.moviendose = 1

        elif (self.movimiento == self.sumav(M_DERECHA, M_IZQUIERDA)):
            # Si no estamos saltando, la postura actual será estar quieto
            if self.numPostura == MOVING_UP_SPRITE:
                self.numPostura = IDLE_UP_SPRITE

            elif self.numPostura == MOVING_DOWN_SPRITE:
                self.numPostura = IDLE_DOWN_SPRITE

            elif self.numPostura == MOVING_SIDE_SPRITE:
                self.numPostura = IDLE_SIDE_SPRITE

            velocidadx = 0
            velocidady = 0
            self.moviendose = 0

        else:   # M_QUIETO
            # Si no estamos saltando, la postura actual será estar quieto
            if self.numPostura == MOVING_UP_SPRITE:
                self.numPostura = IDLE_UP_SPRITE

            elif self.numPostura == MOVING_DOWN_SPRITE:
                self.numPostura = IDLE_DOWN_SPRITE

            elif self.numPostura == MOVING_SIDE_SPRITE:
                self.numPostura = IDLE_SIDE_SPRITE

            velocidadx = 0
            velocidady = 0
            self.moviendose = 0

        # Actualizamos la imagen a mostrar
        self.actualizarPostura()

        # Aplicamos la velocidad en cada eje      
        self.velocidad = (velocidadx, velocidady)

        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo
        #  calcule la nueva posición del Sprite
        MiSprite.update(self, tiempo)
        
        return



# -------------------------------------------------
# Clase Jugador

class Jugador(Personaje):
    "Cualquier personaje del juego"
    def __init__(self):
        self.score = 0
        self.isLoadingJump = False
        self.isJumping = False
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Personaje.__init__(self,'frog_sprites.png','coordRana.txt', [1, 2, 2, 2, 2, 2, 1, 1, 1], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR);

    def mover(self, teclasPulsadas, arriba, abajo, izquierda, derecha, salto):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        mov = [0, 0, 0, 0, 0]
        if teclasPulsadas[arriba]:
            mov[ARRIBA] = 1
        if teclasPulsadas[izquierda]:
            mov[IZQUIERDA] = 1
        if teclasPulsadas[derecha]:
            mov[DERECHA] = 1
        if teclasPulsadas[abajo]:
            mov[ABAJO] = 1
        if teclasPulsadas[salto]:
            mov[SALTO] = 1
        Personaje.mover(self, mov)


# -------------------------------------------------
# Clase NoJugador
class NoJugador(MiSprite):
    "Cualquier otro npc"
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidadCarrera, retardoAnimacion):

        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self);

        # Se carga la hoja
        self.hoja = GestorRecursos.CargarImagen(archivoImagen,-1)
        self.hoja = self.hoja.convert_alpha()
        # El movimiento que esta realizando
        self.movimiento = QUIETO # por defecto es andando pero como solo tiene uno le ponemos 0
        # Lado hacia el que esta mirando
        self.mirando = IZQUIERDA

        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()
        self.numPostura = 1;
        self.numImagenPostura = 0;
        cont = 0;
        self.coordenadasHoja = [];
        for linea in range(0, len(numImagenes)):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0;

        # En que postura esta inicialmente
        self.numPostura = IZQUIERDA

        # El rectangulo del Sprite
        self.rect = pygame.Rect(100,100,self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

        # La velocidad de caminar
        self.velocidadCarrera = velocidadCarrera

        # El retardo en la animacion del personaje (podria y deberia ser distinto para cada postura)
        self.retardoAnimacion = retardoAnimacion

        # Y actualizamos la postura del Sprite inicial, llamando al metodo correspondiente
        self.actualizarPostura()


    # Metodo base para realizar el movimiento: simplemente se le indica cual va a hacer, y lo almacena
    def mover(self, movimiento):
        self.movimiento = movimiento


    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = self.retardoAnimacion
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0;
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1
            self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if self.mirando == IZQUIERDA:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.mirando == DERECHA:
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)


    def update(self, grupoPlataformas, tiempo):

        # Las velocidades a las que iba hasta este momento
        (velocidadx, velocidady) = self.velocidad

        # Si vamos a la izquierda o a la derecha        
        if (self.movimiento == IZQUIERDA) or (self.movimiento == DERECHA):
            # Esta mirando hacia ese lado
            self.mirando = self.movimiento

            # Si vamos a la izquierda, le ponemos velocidad en esa dirección
            if self.movimiento == IZQUIERDA:
                velocidadx = -self.velocidadCarrera
            # Si vamos a la derecha, le ponemos velocidad en esa dirección
            else:
                velocidadx = self.velocidadCarrera

        # Actualizamos la imagen a mostrar
        self.actualizarPostura()

        # Aplicamos la velocidad en cada eje      
        self.velocidad = (velocidadx, velocidady)

        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo
        #  calcule la nueva posición del Sprite
        MiSprite.update(self, tiempo)
        
        return

# -------------------------------------------------
# Clase Enemigo
class Enemigo(NoJugador):
    "Los enemigos"
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, retardoAnimacion):
        # Primero invocamos al constructor de la clase padre con los parametros pasados
        NoJugador.__init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, retardoAnimacion);

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion por defecto, este metodo deberia de ser implementado en las clases inferiores
    #  mostrando la personalidad de cada enemigo
    def mover_cpu(self, jugador):
        # Por defecto un enemigo no hace nada
        #  (se podria programar, por ejemplo, que disparase al jugador por defecto)
        return

# -------------------------------------------------
# Clase Pajaro

class Pajaro(Enemigo):
    "El enemigo 'Pajaro'"
    def __init__(self, iRecorrido, fRecorrido):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Enemigo.__init__(self,'raven.png','coordPajaro.txt', [13], VELOCIDAD_PAJARO, RETARDO_ANIMACION_PAJARO);
        self.rect = pygame.Rect(100,100,self.rect.width/2,self.rect.height/2)
        self.iRecorrido = iRecorrido
        self.fRecorrido = fRecorrido

    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = self.retardoAnimacion
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0;
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1
            self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if self.mirando == IZQUIERDA:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.mirando == DERECHA:
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)

            self.image = pygame.transform.scale(self.image, (self.image.get_width()/2, self.image.get_height()/2))

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador):

        # Movemos solo a los enemigos que esten en la pantalla
        if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA:

            if self.rect.left <= self.iRecorrido:
                Personaje.mover(self, DERECHA)
            elif self.rect.right >= self.fRecorrido:
                Personaje.mover(self, IZQUIERDA)
            else:
                Personaje.mover(self, QUIETO)

        # Si este personaje no esta en pantalla, no hara nada
        else:
            Personaje.mover(self, QUIETO)
