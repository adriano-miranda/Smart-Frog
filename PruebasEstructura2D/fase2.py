import pygame, escena
from director import Director
from pygame.locals import *
from escena import *
from personajes import *
from plataformas import *
from gameOver import GameOver
from victory import Victory
from fase3 import Fase3
from hud import *
from persistentData import *
# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

# Los bordes de la pantalla para hacer scroll
MINIMO_X_JUGADOR = 5
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR
MINIMO_Y_JUGADOR = 5
MAXIMO_Y_JUGADOR = ALTO_PANTALLA - MINIMO_Y_JUGADOR

MINIMO_Y_SCROLL = 250
MAXIMO_Y_SCROLL = ALTO_PANTALLA - MINIMO_Y_SCROLL

POS_INI_JUGADOR = (380, 1980)

# -------------------------------------------------
# Clase Fase

class Fase2(Escena):
    def __init__(self, director:Director):
        # cargamos sonidos
        pygame.mixer.pre_init(44100, 16, 2, 512)   # el archivo tiene que estar formateado con exactamente la misma
                                                    # frecuencia, bitrate y canales para que pueda abrirlo
        pygame.mixer.init()
        self.caidaLava = GestorRecursos.CargarSonido("burnt_lava.ogg")
        self.croak = GestorRecursos.CargarSonido("croak.ogg")
        self.kaorc = GestorRecursos.CargarSonido("kaorc.ogg")
        pygame.mixer.set_reserved(4) # reservamos canales para efectos de sonido
        self.canal_reservado_0 = pygame.mixer.Channel(0)
        self.canal_reservado_1 = pygame.mixer.Channel(1)
        self.canal_reservado_2 = pygame.mixer.Channel(2)

        # musiquita
        pygame.mixer.music.load("sonidos/death_mountain_twilight.ogg")
        pygame.mixer.music.set_volume(0.3) # valores entre 0.0 y 1.0
        pygame.mixer.music.play(-1) # el -1 hace que suene en bucle

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

        # Recuperamos los datos persistentes que se desee saber
        vidas_rana = director.persistentData.getKeyBut(persistentData.KEY_REMAINING_LIVES, 3)

        # Creamos el fondo
        self.fondo = Fondo('lava.gif', 2000)

        # Que parte del fondo estamos visualizando
        self.scrollx = 0
        self.scrolly = 0

        # Creamos los sprites de los jugadores
        self.jugador = Jugador(lives=vidas_rana)
        self.grupoJugadores = pygame.sprite.Group(self.jugador)

        # Ponemos a los jugadores en sus posiciones iniciales
        self.jugador.establecerPosicion(POS_INI_JUGADOR)

        # Creamos las plataformas del decorado
        # (MoverIzq->Derecha, moverArriba->Abajo, Ancho, Largo)
        #Escalado de la imagen debe ser igual que el largo y el ancho!

        plataformaBase = Plataforma(pygame.Rect(-50, 1800, 900, 300),'large_stone.png', 900, 260)
        plataforma1 = Plataforma(pygame.Rect(60, 1600, 300, 100),'squared_stone.png', 300, 100)
        plataforma2 = Plataforma(pygame.Rect(170, 1400, 300, 75),'squared_stone.png', 300, 75)
        plataforma3 = Plataforma(pygame.Rect(200, 1230, 500, 75),'squared_stone.png', 500, 75)
        plataforma4 = Plataforma(pygame.Rect(610, 980, 150, 150),'squared_stone.png', 150, 150)
        plataforma5 = Plataforma(pygame.Rect(210, 860, 300, 100),'squared_stone.png', 300, 100)
        plataforma6 = Plataforma(pygame.Rect(120, 460, 500, 100),'squared_stone.png', 500, 100)
        plataforma7 = Plataforma(pygame.Rect(350, 320, 100, 100),'squared_stone.png', 100, 100)
        plataforma8 = Plataforma(pygame.Rect(350, 190, 100, 100),'squared_stone.png', 100, 100)
        plataforma9 = Plataforma(pygame.Rect(350, 60, 100, 100),'squared_stone.png', 100, 100)
        self.roca1 = TPlatform(pygame.Rect(645, 1550, 50, 50), 'little_stone.png')
        self.roca2 = TPlatform(pygame.Rect(600, 1670, 50, 50), 'little_stone.png')
        self.roca3 = TPlatform(pygame.Rect(690, 1670, 50, 50), 'little_stone.png')
        self.roca4 = TPlatform(pygame.Rect(550, 1410, 50, 50), 'little_stone.png')
        self.roca5 = TPlatform(pygame.Rect(200, 1050, 50, 50), 'little_stone.png')
        self.roca6 = TPlatform(pygame.Rect(50, 1050, 50, 50), 'little_stone.png')
        self.roca7 = TPlatform(pygame.Rect(50, 890, 50, 50), 'little_stone.png')
        self.roca8 = TPlatform(pygame.Rect(50, 670, 50, 50), 'little_stone.png')
        self.roca9 = TPlatform(pygame.Rect(280, 670, 50, 50), 'little_stone.png')
        self.roca10 = TPlatform(pygame.Rect(500, 670, 50, 50), 'little_stone.png')
        self.roca11 = TPlatform(pygame.Rect(700, 670, 50, 50), 'little_stone.png')
        self.roca12 = TPlatform(pygame.Rect(700, 480, 50, 50), 'little_stone.png')
        #plataforma final
        self.plataformaFinal= Plataforma(pygame.Rect(0, 0, 800, 30),'Black.png', 800, 30)

        self.hud = HUD((16, 56), 'rectangulo_blanco.jpeg', 148, 37)
        self.progress_bar = BarraCarga((16, 50), 'PasoBarra.png', 148, 48, self.jugador.max_Time)
        #position: Tuple[int], archivoImagen, scaleX, scaleY
        self.hud_vidas = HUDVidas((0, 0), 'corazon1.png', 70, 50, 55, self.jugador.getLives())

        # El grupo de los HUDS
        self.grupoHuds = pygame.sprite.Group(self.hud, self.progress_bar)
        self.hud_vidas.addToGroup(self.grupoHuds)

        self.jugador.addListenersJump(self.progress_bar)
        self.jugador.addListenersLives(self.hud_vidas)
        

        # El grupo de las plataformas
        self.grupoPlataformas = pygame.sprite.Group(plataformaBase, plataforma1, plataforma2, plataforma3, plataforma4, plataforma5, plataforma6, plataforma7, plataforma8, plataforma9, self.plataformaFinal)
        self.grupoRocas = pygame.sprite.Group(self.roca1, self.roca2, self.roca3, self.roca4, self.roca5, self.roca6, self.roca7, self.roca8, self.roca9, self.roca10, self.roca11, self.roca12)

        # Y los enemigos
        fireball1 = FireBall(670, self.fondo.rect.left)
        fireball1.establecerPosicion((0,1450))
        fireball2 = FireBall(80, self.fondo.rect.right, True)
        fireball2.establecerPosicion((80,520))

        enemigo1 = Pajaro(20, 400)
        enemigo1.establecerPosicion((20, 1600))
        enemigo2 = Lizard(fireball1)
        enemigo2.establecerPosicion((670, 1420))
        enemigo3 = Pajaro(20, 390)
        enemigo3.establecerPosicion((20, 1220))
        enemigo4 = Pajaro(410, 780)
        enemigo4.establecerPosicion((410, 1220))
        enemigo5 = Lizard(fireball2, True)
        enemigo5.establecerPosicion((30, 500))
        enemigo6 = Pajaro(175, 625)
        enemigo6.establecerPosicion((175, 280))
        # Creamos un grupo con los enemigostrofeo
        self.grupoEnemigos = pygame.sprite.Group(fireball1, fireball2, enemigo1, enemigo2, enemigo3, enemigo4, enemigo5, enemigo6)
        
        #Creo las moscas    rectangulo, image,scaleX, scaleY, score
        mosca1 = Insecto(pygame.Rect(645, 1550, 50, 50),'mosca.png', 50, 50, 100)
        mosca2 = Insecto(pygame.Rect(660, 1030, 50, 50),'mosca.png', 50, 50, 100)
        mosca3 = Insecto(pygame.Rect(50, 1050, 50, 50),'mosca.png', 50, 50, 100)
        mosca4 = Insecto(pygame.Rect(375, 90, 50, 50),'mosca.png', 50, 50, 100)
        
        #Creo hormigas
        hormiga1 = Insecto(pygame.Rect(560, 1410, 25, 35),'hormiga.png', 35, 35, 50)
        hormiga2 = Insecto(pygame.Rect(190, 1630, 25, 35),'hormiga.png', 35, 35, 50)
        hormiga3 = Insecto(pygame.Rect(710, 480, 25, 35),'hormiga.png', 35, 35, 50)
        
        self.grupoInsectos = pygame.sprite.Group(mosca1, mosca2, mosca3, mosca4, hormiga1, hormiga2, hormiga3)

        # Creamos un grupo con los Sprites que se mueven
        #  En este caso, solo los personajes, pero podría haber más (proyectiles, etc.)
        self.grupoSpritesDinamicos = pygame.sprite.Group(self.jugador, self.grupoEnemigos)
        # Creamos otro grupo con todos los Sprites
       
        self.grupoSprites = pygame.sprite.Group(self.grupoPlataformas, self.grupoInsectos, self.grupoJugadores, self.grupoEnemigos)

    def scrollHorizontal(self, jugador):
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
        elif (jugador.rect.right>MAXIMO_X_JUGADOR):

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

        
    # Devuelve True o False según se ha tenido que desplazar el scroll
    def actualizarScrollOrdenados(self, jugador):
        # Si el jugador se encuentra más allá del scroll superior
        if (jugador.rect.top < MINIMO_Y_SCROLL):

            # Se calcula cuantos pixeles esta fuera del scroll
            desplazamiento = MINIMO_Y_SCROLL - jugador.rect.top

            # Si el escenario ya está arriba del todo, no lo movemos mas
            if self.scrolly <= 0:
                self.scrolly = 0

                # Si el jugador está arriba del todo
                if(jugador.rect.top < MINIMO_Y_JUGADOR):
                    # Colocamos al jugador arriba de todo
                    jugador.establecerPosicion((jugador.posicion[0], MINIMO_Y_JUGADOR + jugador.rect.height))

                return self.scrollHorizontal(jugador); # No se ha actualizado el scroll

            # Si se puede hacer scroll arriba
            else:
                # Calculamos el nivel de scroll actual: el anterior - desplazamiento
                #  (desplazamos arriba)
                self.scrolly = self.scrolly - desplazamiento;

                return True; # Se ha actualizado el scroll

        # Si el jugador se encuentra más allá del scroll inferior
        elif (jugador.rect.bottom > MAXIMO_Y_SCROLL):

            # Se calcula cuantos pixeles esta fuera del scroll
            desplazamiento = jugador.rect.bottom - MAXIMO_Y_SCROLL
            # Si el escenario ya está abajo del todo, no lo movemos mas
            if self.scrolly + ALTO_PANTALLA >= self.fondo.rect.bottom:
                self.scrolly = self.fondo.rect.bottom - ALTO_PANTALLA

                # Si el jugador está abajo del todo
                if(jugador.rect.bottom > MAXIMO_Y_JUGADOR):
                    # Colocamos al jugador abajo de todo
                    jugador.establecerPosicion((jugador.posicion[0], self.scrolly + MAXIMO_Y_JUGADOR))
                    desplazamiento = jugador.rect.bottom - MAXIMO_Y_JUGADOR

                return self.scrollHorizontal(jugador); # No se ha actualizado el scroll


            # Si se puede hacer scroll abajo
            else:

                # Calculamos el nivel de scroll actual: el anterior + desplazamiento
                #  (desplazamos abajo)
                if(self.scrolly + desplazamiento < self.fondo.rect.bottom - ALTO_PANTALLA):
                    self.scrolly = self.scrolly + desplazamiento;
                else:
                    self.scrolly = self.fondo.rect.bottom - ALTO_PANTALLA

                return True; # Se ha actualizado el scroll

            return False

        self.scrollHorizontal(jugador)


    def actualizarScroll(self, jugador):
        # Se ordenan los jugadores según el eje x, y se mira si hay que actualizar el scroll
        cambioScroll = self.actualizarScrollOrdenados(jugador)

        # Si se cambio el scroll, se desplazan todos los Sprites y el fondo
        if cambioScroll:
            # Actualizamos la posición en pantalla de todos los Sprites según el scroll actual
            for sprite in iter(self.grupoSprites):
                sprite.establecerPosicionPantalla((self.scrollx, self.scrolly))

            # Ademas, actualizamos el fondo para que se muestre una parte distinta
            self.fondo.update(self.scrolly)

    def hitEnemy(self, jugador):
        return pygame.sprite.spritecollideany(jugador, self.grupoEnemigos)

    def isOnWater(self, entidad1: pygame.sprite.Sprite, ground_platforms: pygame.sprite.Group) -> bool:
        aux = (pygame.sprite.spritecollideany(entidad1, ground_platforms))
        #si no es ninguna de las plataformas
        return (aux is None)

    def eatInsect(self, entidad1: pygame.sprite.Sprite, insectos: pygame.sprite.Group) -> bool:
        aux = (pygame.sprite.spritecollideany(entidad1, insectos))
        #si es un insecto
        return (aux)

    def isFinalPlatform(self, jugador):
        return pygame.sprite.spritecollide(self.jugador, [self.plataformaFinal], False)
    
    
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
        self.grupoHuds.update() # ADriano dice que falla aqui
        #self.grupoSpritesDinamicos.update(self.grupoInsectos, tiempo)

        # actualizar estado plataformas temporales
        for elemento in iter(self.grupoRocas):
            elemento.update(self.jugador)

            # si elemento está como no visible
            if(not elemento.visible):
                self.grupoPlataformas.remove(elemento)
                self.grupoSprites.remove(elemento)
            elif(elemento not in self.grupoPlataformas):
                self.grupoPlataformas.add(elemento)
                self.grupoSprites = pygame.sprite.Group(elemento, self.grupoSprites)

        
        # Dentro del update ya se comprueba que todos los movimientos son válidos
        #  (que no choque con paredes, etc.)

        # Los Sprites que no se mueven no hace falta actualizarlos,
        #  si se actualiza el scroll, sus posiciones en pantalla se actualizan más abajo
        # En cambio, sí haría falta actualizar los Sprites que no se mueven pero que tienen que
        #  mostrar alguna animación

        # Comprobamos si hay colision entre algun jugador y algun enemigo
        # Se comprueba la colision entre ambos grupos
        # Si la hay, indicamos que se ha finalizado la fase
        #if pygame.sprite.groupcollide(self.grupoJugadores, self.grupoEnemigos, False, False)!={}:
            # Se le dice al director que salga de esta escena y ejecute la siguiente en la pila
        #    self.director.salirEscena()

        # Actualizamos el scroll
        self.actualizarScroll(self.jugador)

        # Comprobamos colisiones
        if(self.hitEnemy(self.jugador)):
            self.canal_reservado_1.play(self.kaorc)
            self.jugador.establecerPosicion(POS_INI_JUGADOR)
            self.jugador.damage()
        
        if(self.isOnWater(self.jugador,self.grupoPlataformas) and  not self.jugador.isJumping):
            self.canal_reservado_0.play(self.caidaLava)
            print("ESTOY EN EL AGUA")
            self.jugador.establecerPosicion(POS_INI_JUGADOR)
            self.jugador.damage()

        if(self.eatInsect(self.jugador,self.grupoInsectos) and  not self.jugador.isJumping):
            self.canal_reservado_2.play(self.croak)
            print("COMIENDO INSECTO")
            insecto = pygame.sprite.spritecollideany(self.jugador, self.grupoInsectos)
            self.jugador.addScore(insecto.score)
            self.jugador.addLife()
            pygame.sprite.Sprite.kill(insecto)
            print("PUNTUACION1 = ",str(self.jugador.getScore()))
                
        if(self.jugador.lives ==0):
            print('MUERTO')
            self.gameOver()

        if self.isFinalPlatform(self.jugador):
            print('Estoy en la plataforma final')
            self.director.persistentData.addKeyValue(persistentData.KEY_REMAINING_LIVES, self.jugador.getLives())
            #paso a la pantalla de victoria
            self.victory()
            pass
        #print("Estoy en la posicion: ",self.jugador.posicion )        

    def gameOver(self):
        gameOver = GameOver(self.director)
        self.director.cambiarEscena(gameOver)

    def victory(self):
        victory = Victory(self.director, self.jugador.getScore(), Fase3(self.director))
        self.director.cambiarEscena(victory)            

    def dibujar(self, pantalla):
        # Ponemos primero el fondo
        self.fondo.dibujar(pantalla)
        # Luego los Sprites
        self.grupoSprites.draw(pantalla)
        # Por último, los HUD's
        self.grupoHuds.draw(pantalla)


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
