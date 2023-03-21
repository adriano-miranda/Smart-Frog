from Estados import *

class EstadoCargandoSalto(EstadoJugador):

    def __init__(self) -> None:
        super().__init__()
        # velocidades a 0
        self.contexto().detener()

    def update(self, grupoPlataformas, tiempo) -> None:
        # El usuario quiere seguir cargando el salto
        if(self.contexto().movimiento[4]):
            self.contexto().t0 += tiempo
            self.contexto().notifyListeners(self.contexto().subscribers_jump, self.contexto().t0)


class EstadoNormal(EstadoJugador):
    
    def update(self, grupoPlataformas, tiempo) -> None:
        pass


class EstadoSalto(EstadoJugador):

    def update(self, grupoPlataformas, tiempo) -> None:
        if ((self._contexto.ts <= 0) or (self._contexto.posicion == self._contexto.posicion_anterior)):
            self._contexto.isJumping = False
            self._contexto.detener()
            self._contexto.cambiarEstado(EstadoNormal())
        else:
            self._contexto.ts -= tiempo