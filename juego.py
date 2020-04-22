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
        self.vida=2

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
        self.velx = 5
        self.vely = random.randrange(0,10)
        self.tmp=random.randrange(40,90)

    def RetPos(self):
        x=self.rect.x
        y=self.rect.bottom
        return[x,y]

    def update(self):
        self.tmp-=1
        self.rect.x+=self.velx
        if self.rect.x>(ANCHO-self.rect.width):
            self.rect.x=ANCHO-self.rect.width
            self.velx=-5

        if self.rect.x<0:
            self.rect.x=0
            self.velx=5

        if self.rect.y>(ALTO-self.rect.width):
            self.rect.y=ALTO-self.rect.width
            self.vely=-5


        if self.rect.y<0:
            self.rect.y=0
            self.vely=5

        self.rect.y+=self.vely
        pass


class Bala(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('bullets.png')
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

    #seccion antes del juego
    pygame.mixer.init()
    sonido_Balas = pygame.mixer.Sound('machine_gun.ogg')
    sonido_Misil = pygame.mixer.Sound('misil.ogg')
    msc=pygame.mixer.Sound('Heroic_Intrusion.ogg')
    fuente_prev=pygame.font.Font(None,46)
    txt_titulo=fuente_prev.render('JUEGO EJEMPLO',True,BLANCO)
    msc.play()

    #carga sonidos



    fin = False
    fin_prev=False
    while (not fin) and (not fin_prev):
        # Gestion eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.KEYDOWN:
                fin_prev=True
        ventana.blit(txt_titulo,[350,300])
        pygame.display.flip()
    msc.stop()

    #Seccion del juego
    jugadores = pygame.sprite.Group()
    rivales = pygame.sprite.Group()
    balas = pygame.sprite.Group()
    balas_r=pygame.sprite.Group()

    fuente_j=pygame.font.Font(None,32)
    j = Jugador([300, 200])
    jugadores.add(j)

    n = 5
    for i in range(n):
        x = random.randrange(ANCHO)
        y = random.randrange((ALTO - 150))
        #vx = random.randrange(10)
        r = Rival([x, y])
        #r.velx = vx
        rivales.add(r)

    puntos=0
    reloj = pygame.time.Clock()
    fin = False
    fin_juego=False
    while (not fin) and (not fin_juego):
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
                if event.button==1:
                    sonido_Balas.play()
                    p = j.RetPos()
                    b = Bala(p)
                    b.vely = -10
                    balas.add(b)
                    reloj.tick(120)
                    sonido_Balas.stop()
                if event.button== 2 :
                    sonido_Misil.play(0,2000)
                    reloj.tick(120)
                    sonido_Misil.stop()

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
            '''if puntos>3:
                fin=True'''
        print(puntos)

        # control rivales

        for r in rivales:
            if r.tmp<0:
                print ('disparo')
                pos=r.RetPos()
                b=Bala(pos)
                b.vely=10
                balas_r.add(b)
                r.tmp=random.randrange(0,50)

        # Limpieza de memoria
        for b in balas:
            ls_r = pygame.sprite.spritecollide(b, rivales, True)
            if b.rect.y < -50:
                balas.remove(b)
            for r in ls_r:
                balas.remove(b)


        for b in balas_r:
            ls_j=pygame.sprite.spritecollide(b,jugadores,False)
            #elimina bala al salir de pantalla
            if b.rect.y>ALTO:
                balas_r.remove(b)
            contacto=True
            #elimina bala si contacto con jugador
            for j in ls_j:
                if contacto:
                    j.vida-=1
                    balas_r.remove(b)
                    contacto=False

        for j in jugadores:
            if j.vida<0:
                fin_juego=True

        # Refresco
        mjs='vidas: '+ str(j.vida)
        info=fuente_j.render(mjs,True,BLANCO)
        jugadores.update()
        rivales.update()
        balas.update()
        balas_r.update()
        ventana.fill(NEGRO)
        ventana.blit(info,[10,10])
        jugadores.draw(ventana)
        rivales.draw(ventana)
        balas_r.draw(ventana)
        balas.draw(ventana)
        pygame.display.flip()
        reloj.tick(40)



#Después del juego
    final = pygame.image.load('game_over.jpg')
    while not fin:
        # Gestion eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
        ventana.fill(NEGRO)
        ventana.blit(final, (0, 0))
        pygame.display.update()

