import pygame
import random

ANCHO = 800
ALTO = 600
NEGRO = [0, 0, 0]
ROJO = [255, 0, 0]
VERDE = [0, 255, 0]
AMARILLO = [255, 255, 0]
BLANCO = [255, 255, 255]


class Jugador(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('player.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = (ALTO - self.rect.height) - 10
        self.velx = 0
        self.vely=0

    def RetPos(self):
        x = self.rect.x
        y = self.rect.y - 20
        return [x, y]

    def update(self):
        self.rect.x += self.velx
        self.rect.y +=self.vely


class Rival(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('NAVE.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velx = 0
        self.vely = 0

    def update(self):
        # self.rect.x+=self.velx
        # self.rect.y+=self.vely
        pass


class Bala(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('misil1.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.vely = 0

    def update(self):
        self.rect.y += self.vely


if __name__ == '__main__':
    pygame.init()
    # Definicion de variables
    ventana = pygame.display.set_mode([ANCHO, ALTO])
    jugadores = pygame.sprite.Group()
    rivales = pygame.sprite.Group()
    balas = pygame.sprite.Group()

    j = Jugador([300, 200])
    jugadores.add(j)

    n = 10
    for i in range(n):
        x = random.randrange(ANCHO)
        y = random.randrange((ALTO - 150))
        vx = random.randrange(10)
        r = Rival([x, y])
        r.velx = vx
        rivales.add(r)

    puntos=0
    reloj = pygame.time.Clock()
    fin = False
    while not fin:
        # Gestion eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    j.velx = 5
                    j.vely = 0
                if event.key == pygame.K_a:
                    j.velx = -5
                    j.vely = 0
                if event.key == pygame.K_w:
                    j.vely = -5
                    j.velx = 0
                if event.key == pygame.K_s:
                    j.vely = 5
                    j.velx = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                p = j.RetPos()
                b = Bala(p)
                b.vely = -10
                balas.add(b)
            if event.type == pygame.KEYUP:
                j.vely = 0
                j.velx = 0
        # Control
        if j.rect.x > ANCHO:
            j.rect.x = 0 - j.rect.width
        # Colision
        ls_col = pygame.sprite.spritecollide(j, rivales, True)
        for e in ls_col:
            puntos += 1
        print(puntos)

        # Limpieza de memoria
        for b in balas:
            ls_r = pygame.sprite.spritecollide(b, rivales, True)
            if b.rect.y < -50:
                balas.remove(b)
        # Refresco
        jugadores.update()
        rivales.update()
        balas.update()
        ventana.fill(NEGRO)
        jugadores.draw(ventana)
        rivales.draw(ventana)
        balas.draw(ventana)
        pygame.display.flip()
        reloj.tick(40)