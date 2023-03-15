import pygame
import random

# definir colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# definir tamaño de pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# definir tamaño de sprite
SPRITE_WIDTH = 50
SPRITE_HEIGHT = 50

# definir velocidad de movimiento
MOVEMENT_SPEED = 5
WATER_SPEED = 3

# definir distancia máxima de lanzamiento de lengua
TONGUE_DISTANCE = SPRITE_WIDTH

class Fly(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # cargar imagen
        self.image = pygame.image.load("fly.png").convert_alpha()

        # escalar imagen
        self.image = pygame.transform.scale(self.image, (SPRITE_WIDTH, SPRITE_HEIGHT))

        # definir rectángulo de sprite
        self.rect = self.image.get_rect()

        # definir posición aleatoria
        self.rect.x = random.randint(0, SCREEN_WIDTH - SPRITE_WIDTH)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - SPRITE_HEIGHT)

class Frog(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # cargar imagen
        self.image = pygame.image.load("frog.png").convert_alpha()

        # escalar imagen
        self.image = pygame.transform.scale(self.image, (SPRITE_WIDTH, SPRITE_HEIGHT))

        # definir rectángulo de sprite
        self.rect = self.image.get_rect()

        # definir posición inicial
        self.rect.x = (SCREEN_WIDTH - SPRITE_WIDTH) // 2
        self.rect.y = SCREEN_HEIGHT - SPRITE_HEIGHT

        # definir velocidad de movimiento
        self.speed = MOVEMENT_SPEED

        # definir dirección de movimiento
        self.direction = "none"

        self.tongue = None

        self.score = 0

    def move(self):
        # mover sprite en la dirección actual
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed

        # comprobar si la rana se encuentra en el agua
        if self.rect.y < SCREEN_HEIGHT // 2:
            self.speed = WATER_SPEED
        else:
            self.speed = MOVEMENT_SPEED

        # comprobar si la rana ha llegado al borde de la pantalla
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - SPRITE_WIDTH:
            self.rect.x = SCREEN_WIDTH - SPRITE_WIDTH
        elif self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > SCREEN_HEIGHT - SPRITE_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - SPRITE_HEIGHT
       
    def shoot_tongue(self):
        # definir la posición de la punta de la lengua
        if self.direction == "left":
            tongue_x = self.rect.x - TONGUE_DISTANCE
            tongue_y = self.rect.y + SPRITE_HEIGHT // 2
        elif self.direction == "right":
            tongue_x = self.rect.x + SPRITE_WIDTH + TONGUE_DISTANCE
            tongue_y = self.rect.y + SPRITE_HEIGHT // 2
        elif self.direction == "up":
            tongue_x = self.rect.x + SPRITE_WIDTH // 2
            tongue_y = self.rect.y - TONGUE_DISTANCE
        elif self.direction == "down":
            tongue_x = self.rect.x + SPRITE_WIDTH // 2
            tongue_y = self.rect.y + SPRITE_HEIGHT + TONGUE_DISTANCE

        # crear un sprite para la lengua
        tongue = pygame.sprite.Sprite()
        tongue.image = pygame.Surface((TONGUE_DISTANCE, 2))
        tongue.image.fill(GREEN)
        tongue.rect = tongue.image.get_rect()
        tongue.rect.x = tongue_x
        tongue.rect.y = tongue_y

        # buscar si la lengua golpea una mosca
        for fly in fly_list:
            if tongue.rect.colliderect(fly.rect):
                fly_list.remove(fly)
                all_sprites_list.remove(fly)

    def update(self):
        # mover la rana
        self.move()

        # actualizar la imagen de la rana
        if self.direction == "left":
            self.image = pygame.transform.flip(pygame.image.load("frog.png").convert_alpha(), True, False)
        elif self.direction == "right":
            self.image = pygame.image.load("frog.png").convert_alpha()
        elif self.direction == "up":
            self.image = pygame.transform.rotate(pygame.image.load("frog.png").convert_alpha(), 90)
        elif self.direction == "down":
            self.image = pygame.transform.rotate(pygame.image.load("frog.png").convert_alpha(), -90)

        # comprobar si la rana golpea una mosca
        if pygame.sprite.spritecollide(self, fly_list, True):
            self.score += 1

        # actualizar la posición de la lengua
        if self.tongue is not None:
            self.tongue.rect.x = self.rect.x + SPRITE_WIDTH // 2
            self.tongue.rect.y = self.rect.y + SPRITE_HEIGHT // 2
            if self.tongue_timer <= 0:
                all_sprites_list.remove(self.tongue)
                self.tongue = None
            else:
                self.tongue_timer -= 1

        # comprobar si la rana ha alcanzado la meta
        if self.rect.y < SPRITE_HEIGHT:
            self.score += 10
            self.rect.x = (SCREEN_WIDTH - SPRITE_WIDTH) // 2
            self.rect.y = SCREEN_HEIGHT - SPRITE_HEIGHT
            self.direction = "none"

    def reset(self):
        self.rect.x = (SCREEN_WIDTH - SPRITE_WIDTH) // 2
        self.rect.y = SCREEN_HEIGHT - SPRITE_HEIGHT
        self.direction = "none"
        self.score = 0

# inicializar pygame
pygame.init()

# crear pantalla
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# crear listas de sprites
all_sprites_list = pygame.sprite.Group()
fly_list = pygame.sprite.Group()

# crear rana
frog = Frog()
all_sprites_list.add(frog)

# crear moscas
# crear moscas
for i in range(10):
    fly = Fly()
    all_sprites_list.add(fly)
    fly_list.add(fly)

# inicializar reloj
clock = pygame.time.Clock()

# definir fuente para mostrar puntuación
font = pygame.font.SysFont('Calibri', 25, True, False)

# definir bandera para salir del bucle principal
done = False

# bucle principal
while not done:
    # procesar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                frog.direction = "left"
            elif event.key == pygame.K_RIGHT:
                frog.direction = "right"
            elif event.key == pygame.K_UP:
                frog.direction = "up"
            elif event.key == pygame.K_DOWN:
                frog.direction = "down"
            elif event.key == pygame.K_SPACE and frog.tongue is None:
                frog.shoot_tongue()
                frog.tongue_timer = 10
                frog.tongue = all_sprites_list.add(frog.tongue)

    # actualizar la pantalla
    screen.fill(WHITE)

    # actualizar sprites
    all_sprites_list.update()

    # dibujar sprites
    all_sprites_list.draw(screen)

    # mostrar puntuación
    score_text = font.render("Score: " + str(frog.score), True, BLACK)
    screen.blit(score_text, [10, 10])

    # actualizar pantalla
    pygame.display.flip()

    # limitar el número de fotogramas por segundo
    clock.tick(60)

# salir del juego
pygame.quit()

