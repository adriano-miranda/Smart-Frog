# -*- coding: utf-8 -*-

from hud import *
import pygame, sys, os
from pygame.locals import *
from escena import *
from gestorRecursos import *
from typing import List
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

VELOCIDAD_CALAMAR = 0.1 # Pixeles por milisegundo
RETARDO_ANIMACION_CALAMAR = 5 # updates que durará cada imagen del personaje
                             # debería de ser un valor distinto para cada postura

VELOCIDAD_LIZARD = 0.1
RETARDO_ANIMACION_LIZARD = 1

VELOCIDAD_FIREBALL = 6
RETARDO_ANIMACION_FIREBALL = 2


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
        self.movimientoPasado = [0, 0, 0, 0, 0]
        
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
                self.numImagenPostura = 0
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1
            self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            # Si esta mirando a la izquierda, cogemos la porcion de la hoja
            if self.mirando == IZQUIERDA:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.mirando == DERECHA:
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)


    def detener(self):
        "Detiene al jugador y se queda \"idle\" mirando hacia la dirección en la que estaba"
        self.velocidad = (0,0)
        if self.mirando == ARRIBA:
            self.numPostura = IDLE_UP_SPRITE
        elif self.mirando == ABAJO:
            self.numPostura = IDLE_DOWN_SPRITE
        else:
            self.numPostura = IDLE_SIDE_SPRITE

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

            # Si no estamos en el aire
            if self.numPostura != SPRITE_SALTANDO:
                # La postura actual sera estar caminando
                self.numPostura = SPRITE_ANDANDO
                # Ademas, si no estamos encima de ninguna plataforma, caeremos
                if pygame.sprite.spritecollideany(self, grupoPlataformas) == None:
                    self.numPostura = SPRITE_SALTANDO

        # Si queremos saltar
        elif self.movimiento == ARRIBA:
            # La postura actual sera estar saltando
            self.numPostura = SPRITE_SALTANDO
            # Le imprimimos una velocidad en el eje y
            velocidady = -self.velocidadSalto

        # Si no se ha pulsado ninguna tecla
        elif self.movimiento == QUIETO:
            # Si no estamos saltando, la postura actual será estar quieto
            if not self.numPostura == SPRITE_SALTANDO:
                self.numPostura = SPRITE_QUIETO
            velocidadx = 0



        # Además, si estamos en el aire
        if self.numPostura == SPRITE_SALTANDO:

            # Miramos a ver si hay que parar de caer: si hemos llegado a una plataforma
            #  Para ello, miramos si hay colision con alguna plataforma del grupo
            plataforma = pygame.sprite.spritecollideany(self, grupoPlataformas)
            #  Ademas, esa colision solo nos interesa cuando estamos cayendo
            #  y solo es efectiva cuando caemos encima, no de lado, es decir,
            #  cuando nuestra posicion inferior esta por encima de la parte de abajo de la plataforma
            if (plataforma != None) and (velocidady>0) and (plataforma.rect.bottom>self.rect.bottom):
                # Lo situamos con la parte de abajo un pixel colisionando con la plataforma
                #  para poder detectar cuando se cae de ella
                self.establecerPosicion((self.posicion[0], plataforma.posicion[1]-plataforma.rect.height+1))
                # Lo ponemos como quieto
                self.numPostura = SPRITE_QUIETO
                # Y estará quieto en el eje y
                velocidady = 0

            # Si no caemos en una plataforma, aplicamos el efecto de la gravedad
            else:
                velocidady += GRAVEDAD * tiempo

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
    def __init__(self, max_time = 1, max_jump_distance = 160, jump_v = 0.15, lives = 3, score = 0):
        self.score = score         # Puntuación de la rana
        self.lives = lives         # Vidas restantes de la rana
        self.max_Time = max_time   # Tiempo[s] tras el cual seguir cargando el salto, no tiene efecto
        self.jump_velocity = jump_v
        self.max_jump_distance = max_jump_distance

        self.subscribers_lives = []
        self.subscribers_score = []
        self.subscribers_jump = []

        self.isLoadingJump = False
        self.isJumping = False

        self.t0 = 0 # Tiempo (aprox.) que el usuario ha mantenido la tecla de salto
        self.ts = 0 # Tiempo que el jugador va a saltar hasta que se detenga, sino se detiene antes

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


    # Getters y setters
    def getLives(self):
        return self.lives
    

    def getScore(self):
        return self.score
    

    def resetAtPosition(self, position):
        "Se coloca al jugador en una posición concreta y se resetean los movimientos"
        self.establecerPosicion(position)
        self.isJumping = False
        self.isLoadingJump = False
        self.mirando = ARRIBA
        self.numPostura = IDLE_UP_SPRITE


    def addScore(self, quantity):
        "Añade puntuación a la rana, se lo notifica a los subscriptores y devuelve la cantidad tras eso"
        self.score += quantity
        self.notifyListeners(self.subscribers_score, self.score)
        return self.score


    def damage(self):
        "Le resta una vida al jugador, se lo notifica a los subscriptores y devuelve la cantidad a quien llama este método"
        self.lives = max(0, self.lives-1)
        self.notifyListeners(self.subscribers_lives, self.lives)
        return self.lives


    def isLoadingJump(self):
        "Está la rana preparándose para saltar?"
        return self.isLoadingJump


    def isJumping(self):
        "La rana está saltando?"
        return self.isJumping
    

    def notifyListeners(self, listenerList: list[Listener], dato):
        "Notificar a los listeners de una lista específica de listeners"
        for listerine in listenerList:
            listerine.run(dato)

    def addListenersLives(self, listener: Listener):
        "Añadir un listener a la lista de suscriptores para conocer cambios en las vidas"
        self.subscribers_lives.append(listener)

    def addListenersScore(self, listener: Listener):
        "Añadir un listener a la lista de suscriptores para conocer cambios en la puntuación"
        self.subscribers_lives.append(listener)

    def addListenersJump(self, listener: Listener):
        "Añadir un listener a la lista de suscriptores para saber el tiempo que el salto lleva cargando"
        self.subscribers_jump.append(listener)


    def sumav(self, a: list, b: list):
        "Suma dos vectores y devuelve el resultado"
        c = b.copy()
        for n in range(b.__len__()):
            c[n] = a[n] + b[n]
        return c
    
    def diff(self, a:list, b:list) -> list:
        "la lista A, debería ser la más grande, sino podrían quedar valores negativos"
        c = a.copy()
        for n in range(a.__len__()):
                c[n] -= b[n]
        return c

    def update(self, grupoPlataformas, tiempo):
    
        # Las velocidades a las que iba hasta este momento
        (velocidadx, velocidady) = self.velocidad

        ##  self.movimiento and self.movimientoPasado
        if (self.isJumping):
            if ((self.ts <= 0) or (self.posicion == self.posicion_anterior)):
                self.isJumping = False
                self.detener()
            else:
                self.ts -= tiempo
        else:
            if (self.isLoadingJump and (not self.movimiento[4])): # Ahora si salto
                self.isLoadingJump = False
                self.isJumping = True
                self.notifyListeners(self.subscribers_jump, 0)
                if(self.mirando == ARRIBA):
                    self.numPostura = JUMPING_UP_SPRITE
                    velocidadx = 0
                    velocidady = -self.jump_velocity
                elif(self.mirando == ABAJO):
                    self.numPostura = JUMPING_DOWN_SPRITE
                    velocidadx = 0
                    velocidady = self.jump_velocity
                else:
                    if(self.mirando == IZQUIERDA):
                        velocidadx = -self.jump_velocity
                    else:
                        velocidadx = self.jump_velocity
                    velocidady = 0
                    self.numPostura = JUMPING_SIDE_SPRITE
                jump_distance = (((self.t0) / 1000) / self.max_Time) * self.max_jump_distance
                jump_distance = min(self.max_jump_distance, jump_distance)
                # Math: T_s = \frac{\min(\Delta_{max}, \frac{T_p}{T_{p max}} \times \Delta_{max})}{V_s}
                self.ts = (min(self.max_jump_distance, self.max_jump_distance * (self.t0 / 1000)/self.max_Time)) / self.jump_velocity
            else:
                if (not self.isLoadingJump and self.movimiento[4]): # Quiero cargar salto
                    self.isLoadingJump = True
                    velocidadx = velocidady = 0
                    self.detener()
                    self.t0 = tiempo
                    self.notifyListeners(self.subscribers_jump, self.t0)
                elif (self.isLoadingJump and self.movimiento[4]):   # Estoy cargando el salto
                    self.t0 += tiempo
                    self.notifyListeners(self.subscribers_jump, self.t0)
                    if self.movimiento[ARRIBA]:
                        self.mirando = ARRIBA
                        self.numPostura = 0
                    if self.movimiento[IZQUIERDA]:
                        self.mirando = IZQUIERDA
                        self.numPostura = 2
                    if self.movimiento[DERECHA]:
                        self.mirando = DERECHA
                        self.numPostura = 2
                    if self.movimiento[ABAJO]:
                        self.mirando = ABAJO
                        self.numPostura = 1
                
                # DIAGONAL
                elif (self.movimiento == self.sumav(M_IZQUIERDA, M_ARRIBA)):
                    self.movimiento = self.movimientoPasado

                # DIAGONAL
                elif (self.movimiento == self.sumav(M_IZQUIERDA, M_ABAJO)):
                    self.movimiento = self.movimientoPasado

                # DIAGONAL
                elif (self.movimiento == self.sumav(M_DERECHA, M_ARRIBA)):
                    self.movimiento = self.movimientoPasado
                    
                # DIAGONAL
                elif (self.movimiento == self.sumav(M_DERECHA, M_ABAJO)):
                    self.movimiento = self.movimientoPasado

                elif (self.movimiento == M_ARRIBA):
                    # La postura actual sera estar saltando
                    self.mirando = ARRIBA
                    if not self.isLoadingJump:
                        self.numPostura = MOVING_UP_SPRITE
                        # Le imprimimos una velocidad en el eje y
                        velocidady = -self.velocidadCarrera
                        velocidadx = 0
                        self.moviendose = 1

                elif (self.movimiento == M_ABAJO):
                    # La postura actual sera estar saltando
                    self.mirando = ABAJO
                    if not self.isLoadingJump:
                        self.numPostura = MOVING_DOWN_SPRITE
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
                    self.mirando = DERECHA
                    if not self.isLoadingJump:
                        velocidadx = self.velocidadCarrera
                        velocidady = 0
                        self.numPostura = MOVING_SIDE_SPRITE
                        self.moviendose = 1

                elif (self.movimiento == M_IZQUIERDA):
                    self.mirando = IZQUIERDA
                    if not self.isLoadingJump:
                        velocidadx = -self.velocidadCarrera
                        velocidady = 0
                        self.numPostura = MOVING_SIDE_SPRITE
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

        self.posicion_anterior = self.posicion

        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo
        #  calcule la nueva posición del Sprite
        MiSprite.update(self, tiempo)
        
        return


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

        if self.rect.left <= self.iRecorrido:
            NoJugador.mover(self, DERECHA)
        elif self.rect.right >= self.fRecorrido:
            NoJugador.mover(self, IZQUIERDA)
        else:
            NoJugador.mover(self, QUIETO)

# -------------------------------------------------
# Clase Calamar

class Calamar(Enemigo):
    "El enemigo 'Calamar'"
    def __init__(self, iRecorrido, fRecorrido, grupoPlataformas):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Enemigo.__init__(self,'squid.png','coordCalamar.txt', [1, 1], VELOCIDAD_CALAMAR, RETARDO_ANIMACION_CALAMAR);
        self.rect = pygame.Rect(100,100,self.rect.width/2,self.rect.height/2)
        self.original_scale = (self.rect.width, self.rect.height)
        self.iRecorrido = iRecorrido
        self.fRecorrido = fRecorrido
        self.grupoPlataformas = grupoPlataformas

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

            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador):

        if pygame.sprite.spritecollideany(self, self.grupoPlataformas):
            self.numPostura = IZQUIERDA
        else:
            self.numPostura = DERECHA

        if self.rect.left <= self.iRecorrido:
            NoJugador.mover(self, DERECHA)
        elif self.rect.right >= self.fRecorrido:
            NoJugador.mover(self, IZQUIERDA)
        else:
            NoJugador.mover(self, QUIETO)

# -------------------------------------------------
# Clase Lizard
class Lizard(Enemigo):
    def __init__(self, fireBall, derecha=False):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Enemigo.__init__(self,'lava_enemy.png','coordLava.txt', [13, 1], VELOCIDAD_LIZARD, RETARDO_ANIMACION_LIZARD);
        self.fireBall = fireBall
        self.derecha = derecha

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

            self.image = pygame.transform.scale(self.image, (self.image.get_width()*2.5, self.image.get_height()*2.5))

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador):
        if(self.derecha):
            self.mirando = DERECHA
            if (self.fireBall.posicion[0] >= 760):
                self.numPostura = IZQUIERDA
            else:
                self.numPostura = DERECHA
        else:
            if (self.fireBall.posicion[0] <= 0):
                self.numPostura = IZQUIERDA
            else:
                self.numPostura = DERECHA

# -------------------------------------------------
# Clase FireBall
class FireBall(Enemigo):
    def __init__(self, inicio, fin, derecha=False):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Enemigo.__init__(self,'lava_enemy.png','coordFireBall.txt', [4], VELOCIDAD_FIREBALL, RETARDO_ANIMACION_FIREBALL);
        self.rect = pygame.Rect(100,100,self.rect.width*1.5,self.rect.height*1.5)
        self.inicio = inicio
        self.fin = fin
        self.derecha = derecha

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

            self.image = pygame.transform.scale(self.image, (self.image.get_width()*2, self.image.get_height()*2))

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador):
        if(self.derecha):
            self.mirando = DERECHA
            if(self.rect.left >= self.fin):
                self.posicion = (self.inicio, self.posicion[1])
            else:
                self.posicion = ((self.posicion[0] + VELOCIDAD_FIREBALL), self.posicion[1])
        else:
            if(self.rect.right <= self.fin):
                self.posicion = (self.inicio, self.posicion[1])
            else:
                self.posicion = ((self.posicion[0] - VELOCIDAD_FIREBALL), self.posicion[1])