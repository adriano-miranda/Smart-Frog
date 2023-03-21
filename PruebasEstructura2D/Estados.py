from __future__ import annotations
from abc import ABC, abstractmethod


class Contexto():

    _estado: EstadoJugador

    def cambiarEstado(self, estado: EstadoJugador) -> None:
        self._estado = estado
        self._estado.contexto(self) # Ponemos el contexto dentro del estado


class EstadoJugador(ABC):

    _contexto : Contexto

    def contexto(self) -> Contexto:
        return self._contexto
    
    def establecerContexto(self, contexto: Contexto) -> None:
        self._contexto = contexto
    
    def update(self, grupoPlataformas, tiempo) -> None:
        pass