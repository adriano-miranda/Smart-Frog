class persistentData():

    def __init__(self) -> None:
        self.RAE = {
            "version": "1.00",
            "defaultLives": 3,
        }

    def getKeyBut(self, key, default):
        "Devuelve el valor del par (clave, valor) o \"default\" si este no existe"
        if key in self.RAE:
            return self.RAE[key]
        return default
    
    def checkKey(self, key) -> bool:
        "Comprueba si existe una clave en el diccionario de datos"
        return (key in self.RAE)
    
    def getKey(self, key):
        "Devuelve el valor del par (clave, valor) o una excepción si este no existe"
        return self.RAE[key]
    
    def addKeyValue(self, key, valor):
        "Añade o actualiza un par (clave, valor) en el diccionario"
        self.RAE[key] = valor