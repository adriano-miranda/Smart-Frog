import pygame
import random

# Definir constantes del juego
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
FROGGER_SPEED = 5
WATER_SPEED = 2
MAX_FLY_SPEED = 5
MIN_FLY_DELAY = 2000
MAX_FLY_DELAY = 5000


class Frog(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.is_swimming = False

    def move_left(self):
        self.rect.x -= FROGGER_SPEED

    def move_right(self):
        self.rect.x += FROGGER_SPEED

    def move_up(self):
        self.rect.y -= FROGGER_SPEED

    def move_down(self):
        self.rect.y += FROGGER_SPEED

    def swim_up(self):
        self.is_swimming = True
        self.rect.y -= WATER_SPEED

    def swim_down(self):
        self.is_swimming = True
        self.rect.y += WATER_SPEED

    def stop_swimming(self):
        self.is_swimming = False

    def use_tongue(self):
        tongue_rect = pygame.Rect(self.rect.x + self.width, self.rect.y, self.width, self.height)
        return tongue_rect

    def update(self):
        if self.is_swimming:
            if self.rect.y <= 0:
                self.rect.y = 0
            elif self.rect.y + self.height >= WINDOW_HEIGHT:
                self.rect.y = WINDOW_HEIGHT - self.height


class Fly(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.randint(1, MAX_FLY_SPEED)

    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= WINDOW_WIDTH:
            self.rect.x = -self.rect.width
            self.rect.y = random.randint(0, WINDOW_HEIGHT - self.rect.height)


class Log(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface([100, 30])
        self.image.fill((153, 76, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.speed > 0 and self.rect.x > WINDOW_WIDTH:
            self.rect.x = -self.rect.width
        elif self.speed < 0 and self.rect.x < -self.rect.width:
            self.rect.x = WINDOW_WIDTH

class Game:
    def __init__(self):
        # Inicializar Pygame
        pygame.init()

        # Configurar ventana
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Frogger")

        # Inicializar reloj
        self.clock = pygame.time.Clock()

        # Crear objetos del juego
        self.all_sprites = pygame.sprite.Group()
        for i in range(NUM_FLIES):
            fly_x = random.randint(0, WINDOW_WIDTH - FLY_WIDTH)
            fly_y = random.randint(0, WINDOW_HEIGHT - FLY_HEIGHT)
            self.flies.append(Fly(fly_x, fly_y, FLY_WIDTH, FLY_HEIGHT))
        for i in range(NUM_LOGS):
            log_x = random.randint(0, WINDOW_WIDTH - LOG_WIDTH)
            log_y = random.randint(0, WATER_HEIGHT - LOG_HEIGHT)
            speed = random.randint(LOG_MIN_SPEED, LOG_MAX_SPEED)
            self.logs.append(Log(log_x, log_y, LOG_WIDTH, LOG_HEIGHT, speed))

    def run(self):
        # Inicializar juego
        running = True
        while running:
            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.frog.move_up()
                    elif event.key == pygame.K_DOWN:
                        self.frog.move_down()
                    elif event.key == pygame.K_LEFT:
                        self.frog.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.frog.move_right()

            # Actualizar objetos del juego
            self.frog.update()

            for fly in self.flies:
                if self.frog.collides_with(fly):
                    self.flies.remove(fly)
                    self.frog.score += 1
                fly.update()

            for log in self.logs:
                if self.frog.collides_with(log):
                    self.frog.attach_to(log)
                log.update()

            if not self.frog.on_log:
                self.frog.detach()

            # Dibujar objetos del juego
            self.window.fill(BACKGROUND_COLOR)

            for fly in self.flies:
                fly.draw(self.window)

            for log in self.logs:
                log.draw(self.window)

            self.frog.draw(self.window)

            # Actualizar pantalla
            pygame.display.update()

            # Esperar un tick
            self.clock.tick(FRAME_RATE)

        # Cerrar Pygame
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()