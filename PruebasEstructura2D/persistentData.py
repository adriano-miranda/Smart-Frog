class persistentData():

    KEY_REMAINING_LIVES = "actual_lives"
    KEY_GAME_VERSION    = "version"
    KEY_DEFAULT_LIVES   = "default_lives"

    def __init__(self) -> None:
        self.rae = {
            "version": "1.00",
            "defaultLives": 3,
        }

    def getKeyBut(self, key, default):
        "Devuelve el valor del par (clave, valor) o \"default\" si este no existe"
        if key in self.rae:
            return self.rae[key]
        return default
    
    def checkKey(self, key) -> bool:
        "Comprueba si existe una clave en el diccionario de datos"
        return (key in self.rae)
    
    def getKey(self, key):
        "Devuelve el valor del par (clave, valor) o una excepción si este no existe"
        return self.rae[key]
    
    def addKeyValue(self, key, valor):
        "Añade o actualiza un par (clave, valor) en el diccionario"
        self.rae[key] = valor
        print("Almacen: Almacenando " + key + " con valor: " + valor.__str__())