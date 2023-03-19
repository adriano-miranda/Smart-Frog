# -*- encoding: utf-8 -*-

from pygame import *
from pygame.locals import *
from escena import *
from gestorRecursos import *
from personajes import *
from fase2 import Fase2

# -------------------------------------------------
# Clase abstracta ElementoGUI

class ElementoGUI:
    def __init__(self, pantalla, rectangulo):
        self.pantalla = pantalla
        self.rect = rectangulo

    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.left = posicionx
        self.rect.bottom = posiciony

    def posicionEnElemento(self, posicion):
        (posicionx, posiciony) = posicion
        if (posicionx>=self.rect.left) and (posicionx<=self.rect.right) and (posiciony>=self.rect.top) and (posiciony<=self.rect.bottom):
            return True
        else:
            return False

    def dibujar(self):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")
    def accion(self):
        raise NotImplemented("Tiene que implementar el metodo accion.")


# -------------------------------------------------
# Clase Boton y los distintos botones
class Boton(ElementoGUI):
    def __init__(self, pantalla, nombreImagen, posicion):
        # Se carga la imagen del boton
        self.imagen = GestorRecursos.CargarImagen(nombreImagen,-1)
        self.imagen = pygame.transform.scale(self.imagen, (170, 75))
        # Se llama al método de la clase padre con el rectángulo que ocupa el botón
        ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

class BotonFase2(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'next.png', (180,570))
    def accion(self):
        self.pantalla.victory.salirPrograma()

class BotonSalir(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'exit.png', (450,570))
    def accion(self):
        self.pantalla.victory.ejecutarFase2()

# -------------------------------------------------
# Clase TextoGUI y los distintos textos


class TextoGUI(ElementoGUI):
    def __init__(self, pantalla, fuente, color, texto, posicion):
        # Se crea la imagen del texto
        self.imagen = fuente.render(texto, True, color)
        # Se llama al método de la clase padre con el rectángulo que ocupa el texto
        ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

class TextoPuntuacion1(TextoGUI):
    def __init__(self, pantalla):
        self.jugador = Jugador()
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('arial', 26)
        puntuacion = "PUNTUACION: " 
        TextoGUI.__init__(self, pantalla, fuente, (0, 0, 0), puntuacion , (100, 500))

class TextoPuntuacion(TextoGUI):
    def __init__(self, pantalla, score):
        self.jugador = Jugador()
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('arial', 26)
        self.score = score
        puntuacion = str(self.score) 
        TextoGUI.__init__(self, pantalla, fuente, (0, 0, 0), puntuacion , (300, 500))

class TextoSalir(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('arial', 26);
        TextoGUI.__init__(self, pantalla, fuente, (0, 0, 0), 'Salir', (610, 565))
    def accion(self):
        self.pantalla.victory.salirPrograma()

class TextoFase2(TextoGUI):
    def __init__(self, pantalla):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('arial', 26);
        TextoGUI.__init__(self, pantalla, fuente, (0, 0, 0), 'nivel 2', (610, 505))
    def accion(self):
        self.pantalla.victory.ejecutarFase2()

# -------------------------------------------------
# Clase PantallaGUI y las distintas pantallas

class PantallaGUI:
    def __init__(self, victory, nombreImagen):
        self.victory = victory
        # Se carga la imagen de fondo
        self.imagen = GestorRecursos.CargarImagen(nombreImagen)
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
        # Se tiene una lista de elementos GUI
        self.elementosGUI = []

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == MOUSEBUTTONDOWN:
                self.elementoClic = None
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        self.elementoClic = elemento
            if evento.type == MOUSEBUTTONUP:
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        if (elemento == self.elementoClic):
                            elemento.accion()

    def dibujar(self, pantalla):
        # Dibujamos primero la imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())
        # Después los botones
        for elemento in self.elementosGUI:
            elemento.dibujar(pantalla)

class PantallaInicialGUI(PantallaGUI):
    def __init__(self, victory, score):
        PantallaGUI.__init__(self, victory, 'victory.png')
        # Creamos los botones y los metemos en la lista
        botonSalir = BotonSalir(self)
        botonFase2 = BotonFase2(self)
        self.elementosGUI.append(botonSalir)
        self.elementosGUI.append(botonFase2)
        # Creamos el texto y lo metemos en la lista
        textoSalir = TextoSalir(self)
        self.score = score
        textoPuntuacion = TextoPuntuacion(self, self.score)
        textoPuntuacion1 = TextoPuntuacion1(self)
        textoFase2 = TextoFase2(self)
        self.elementosGUI.append(textoSalir)
        self.elementosGUI.append(textoPuntuacion)
        self.elementosGUI.append(textoPuntuacion1)
        self.elementosGUI.append(textoFase2)
# -------------------------------------------------
# Clase victory, la escena en sí

class Victory(Escena):

    def __init__(self, director, score):
        # Llamamos al constructor de la clase padre
        Escena.__init__(self, director);
        # Creamos la lista de pantallas
        self.listaPantallas = []
        #Puntuacion para el texto de puntuacion
        self.score = score
        # Creamos las pantallas que vamos a tener
        #   y las metemos en la lista
        self.listaPantallas.append(PantallaInicialGUI(self, self.score))
        # En que pantalla estamos actualmente
        self.mostrarPantallaInicial()
        

    def update(self, *args):
        return

    def eventos(self, lista_eventos):
        # Se mira si se quiere salir de esta escena
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    self.salirPrograma()
            elif evento.type == pygame.QUIT:
                self.director.salirPrograma()

        # Se pasa la lista de eventos a la pantalla actual
        self.listaPantallas[self.pantallaActual].eventos(lista_eventos)

    def dibujar(self, pantalla):
        self.listaPantallas[self.pantallaActual].dibujar(pantalla)

    #--------------------------------------
    # Metodos propios del Victory

    def salirPrograma(self):
        self.director.salirPrograma()

    def ejecutarJuego(self):
        fase = Fase(self.director)
        self.director.apilarEscena(fase)

    def ejecutarFase2(self):
        fase2 = Fase2(self.director)
        self.director.apilarEscena(fase2)

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0

    # def mostrarPantallaConfiguracion(self):
    #    self.pantallaActual = ...
