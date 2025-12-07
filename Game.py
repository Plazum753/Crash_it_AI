import pygame
from sys import exit
import numpy as np

pygame.init()

largeur = 900
hauteur = 700

terrain = pygame.display.set_mode((largeur,hauteur))
pygame.display.set_caption("Crash it")

SPEED = 60
clock = pygame.time.Clock()



def affiche(objets, largeur=900, hauteur=700):
    color = (150,150,0)
    terrain.fill(color)
    pygame.draw.rect(terrain, (100,200,255),(50,50, largeur-100, hauteur-100), border_radius=100)
    
# ============================= obstacles =====================================
    pygame.draw.rect(terrain, color,(100,100,100, 100), border_radius=20)
    pygame.draw.rect(terrain, color,(largeur-200,100,100, 100), border_radius=20)
# =============================================================================

    for e in objets :
        terrain.blit(e.img,e.rect.topleft)

    
class Car :
    def __init__(self, team=0, position=[400,300]):
        self.position = np.array([position[0], position[1]], dtype=np.float64)
        self.team = team
        
        self.voitureLargeur=610//5
        self.voitureHauteur=300//5
        self.clock = pygame.time.Clock()
        self.img=pygame.image.load('Vb.png') if team==0 else  pygame.image.load('Vr.png')
        self.img_origine = pygame.transform.scale(self.img, (self.voitureLargeur, self.voitureHauteur))
        
        self.img = self.img_origine
        
        self.rect = self.img.get_rect(center=self.position)
        
        self.vitesse = np.array([0, 0], dtype=np.float64)
        self.acceleration = 2.0
        self.frottement = 0.9
        self.gravite = 9.81
        
        self.angle = np.pi * self.team

        
        
    def move(self):
        direction = np.array([np.cos(self.angle), np.sin(self.angle)], dtype=np.float64)
        
        keys = pygame.key.get_pressed()
        self.vitesse += self.acceleration * direction if keys[pygame.K_RIGHT] else 0
        self.vitesse -= self.acceleration * direction if keys[pygame.K_LEFT] else 0
        self.vitesse *= self.frottement
        
        self.position += self.vitesse
        
        self.rect = self.img.get_rect(center=self.position)
        
        
        
    def dead(self):
        return False
    


        
def game(hauteur=700,players=("hu","hu")):
    p0 = Car(team=0, position=[largeur//2-250,hauteur-80])
    p1 = Car(team=1, position=[largeur//2+250,hauteur-80])
    GO = -1
    
    while GO == -1 :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        p0.move()
        p1.move()
        
        affiche([p0, p1])
        pygame.display.update()
        clock.tick(SPEED)     
        
        GO = 0 if p0.dead() else 1 if p1.dead() else -1
    
    return GO




game()


pygame.display.update()

pygame.quit()
exit()