"""
Credit: 
Font by Neale Davidson (jaynz@pixelsagas.com)

All other assets including images, sprites and other related things are owned by Thura Soe.
Do not distribute or copy without owner permission.
"""

import sys,os,random,math,pygame

WIDTH = 640
HEIGHT = 340

assetsfolder = "E:\\Python\\Dino Run\\assets"

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = [pygame.image.load(os.path.join(assetsfolder,f"dino ({i}).png")).convert_alpha() for i in range(3)]
        self.walkcount = 0 
        self.image = self.sprites[self.walkcount]
        self.rect = self.image.get_rect(bottomleft=(80,HEIGHT-40))
        self.isJump = False
        self.velocity = 0

    def walk(self):
        if self.walkcount< 2:
            self.walkcount += 1   
            self.image = self.sprites[self.walkcount]
        else:
            self.walkcount = 0
            self.image = self.sprites[self.walkcount]
    
    def jump(self):
        if not self.isJump:
            self.velocity = 15
            self.isJump = True
           
    def update(self):
        if self.isJump:
            self.rect.y -= self.velocity//2
            self.velocity -= 0.3 #downward gravity
        
        #check if dino lands on ground
        if self.rect.bottom > HEIGHT - 40:
            self.rect.bottom = HEIGHT - 40
            self.velocity = 0
            self.isJump = False
    
    def reset(self):
        self.rect.bottomleft = (80,HEIGHT-40)
    
class Ground:
    def __init__(self):
        self.leftground = pygame.image.load(os.path.join(assetsfolder,"ground.png"))
        self.rightground = pygame.image.load(os.path.join(assetsfolder,"ground.png"))
        self.leftground_rect = self.leftground.get_rect(topleft=(0,HEIGHT-40))
        self.rightground_rect = self.rightground.get_rect(topleft=(700,HEIGHT-40))

    def update(self):
        #moving ground from right to left
        if self.leftground_rect.right <= 0:
            #refresh backgounds to its initiate position
            self.leftground_rect.left = 0
            self.rightground_rect.left = 700
        else:
            self.leftground_rect.x -= 2
            self.rightground_rect.x -= 2

    def draw(self,screen):
        screen.blit(self.leftground,self.leftground_rect)
        screen.blit(self.rightground,self.rightground_rect)

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(assetsfolder,"cloud ({}).png".format(random.randint(0,2)))).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.right = random.randint(50,WIDTH-50)
        self.rect.top = random.randint(10,HEIGHT-250)

class KinematicBody(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = ["building (1).png","building (2).png","building (3).png","stone.png","tree.png"]
        self.image = pygame.image.load(os.path.join(assetsfolder,random.choice(self.sprites))).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT - 38
        self.rect.left = WIDTH + random.randrange(0,600)
        self.counts = 0
    
    def update(self):
        #animate to left
        self.rect.left -= 2
        if self.rect.right < 0:
            self.image = pygame.image.load(os.path.join(assetsfolder,random.choice(self.sprites))).convert_alpha()            
            self.rect.left = WIDTH + random.randrange(0,300)
    
    def reset(self):
        self.rect.left = WIDTH + random.randrange(0,600)

class Car(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(assetsfolder,"car (1).png")).convert_alpha()        
        self.rect = self.image.get_rect()  
        self.rect.bottom = HEIGHT - 38
        self.rect.left = WIDTH
        self.velocity = random.randint(3,5)
        self.trigged = False
    
    def update(self):
        #animate to left
        if self.trigged:
            self.rect.left -= self.velocity        
            if self.rect.right < 0:    
                self.reset()
    
    def reset(self):
        self.rect.left = WIDTH
        self.velocity = random.randint(3,5)
        self.trigged = False

class GameScreen:
    def __init__(self):
        pygame.init()

        #game screen
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Dino Run")
        pygame.display.set_icon(pygame.image.load(os.path.join(assetsfolder,"dino (1).png")))

        #score
        self.highscore = 0
        self.score = 0
        self.relife = 0

        #game fonts
        self.font = pygame.font.Font(os.path.join(assetsfolder,"PixelEmulator.ttf"), 80)
        self.font1 = pygame.font.Font(os.path.join(assetsfolder,"PixelEmulator.ttf"), 20)
        self.font2 = pygame.font.Font(os.path.join(assetsfolder,"PixelEmulator.ttf"), 15)

        #sprites and sprite groups
        self.dino = Dino()
        self.ground = Ground()
        self.movingobj = KinematicBody()
        self.movingobj1 = KinematicBody()
        self.car = Car()
        self.all_sprites = pygame.sprite.Group()
        self.moving_sprites = pygame.sprite.Group()

        #add sprites to their coresponding sprite groups
        for _ in range(5):
            cloud = Cloud()
            cloud.add(self.all_sprites)

        self.all_sprites.add(self.dino,self.movingobj,self.movingobj1,self.car)
        self.moving_sprites.add(self.movingobj,self.movingobj1)
    
    def run(self):
        #define a new event for dino walk animation
        DINORUN = pygame.USEREVENT
        pygame.time.set_timer(DINORUN,100)
        CARMOVE = pygame.USEREVENT +1
        pygame.time.set_timer(CARMOVE,1000*15)
        time = pygame.time.Clock()

        #game loop
        playing = True
        gameover = False
        start = False
        eggfound = False
        while playing:    
            if not start:
                #event queue
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        playing = False
                    if e.type == pygame.KEYDOWN:
                        start = True

                self.ground.update()

                self.screen.fill((80,168,218))
                self.ground.draw(self.screen)
                self.displayText(self.font,"Dino Run",(WIDTH//2,HEIGHT//3))
                self.displayText(self.font2,"Press any key to play!",(WIDTH//2,HEIGHT//2))

            if start and not gameover:
                #event queue
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        playing = False
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_SPACE or e.key == pygame.K_UP or e.key == pygame.K_w:
                            self.dino.jump()
                        if e.key == pygame.K_ESCAPE:
                            playing = False
                    if e.type == DINORUN:
                        self.dino.walk()
                    if e.type == CARMOVE:
                        self.car.trigged = True

                    #check if dino collides 
                    hit = pygame.sprite.spritecollide(self.dino,self.moving_sprites,False)
                    if hit:
                        gameover = True
                        self.highscore = self.score
                        self.score = 0
                    
                    #check other game conditions
                    if self.dino.rect.top <= 0:
                        gameover = True
                        self.highscore = self.score
                        self.score = 0

                    #calculate score                    
                    if self.movingobj.rect.right < 70 or self.movingobj1.rect.right < 70:
                        self.score += 1
                    
                    #check if two obj are overlaping each other
                    if pygame.sprite.collide_rect(self.movingobj,self.movingobj1):
                        self.movingobj.reset()
                    
                    #easter egg condition
                    if pygame.sprite.collide_rect(self.dino,self.car):
                        if 100 < self.score < 150:
                            if self.relife ==1:
                                gameover = True
                                eggfound = True
                            else:
                                self.relife +=1                           
                        else:
                            gameover = True
                            self.highscore = self.score
                            self.score = 0
                    
                self.all_sprites.update()
                self.ground.update()

                self.screen.fill((80,168,218))
                self.ground.draw(self.screen)
                self.all_sprites.draw(self.screen)
                self.displayText(self.font2,"High Score: {}".format(str(self.highscore)),(20,10),False)
                self.displayText(self.font2,"Score: {}".format(str(self.score)),(20,30),False)
                    
            if gameover:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        playing = False
                    if e.type == pygame.KEYDOWN:
                        gameover = False
                        self.dino.reset()
                        self.car.reset()
                        for moving_obj in self.moving_sprites.sprites():
                            moving_obj.reset()

                self.ground.update()

                self.screen.fill((80,168,218))
                self.ground.draw(self.screen)
                self.displayText(self.font,"Game Over",(WIDTH//2,HEIGHT//2))
                self.displayText(self.font1,"Press any key to play again!",(WIDTH//2,HEIGHT//1.5))
                self.displayText(self.font2,"Your HighScore: {}".format(self.highscore),(WIDTH//2,HEIGHT//1.3))
            
            if gameover and eggfound:
                """
                Easter egg screen
                """
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        playing = False

                self.screen.fill((80,168,218))
                self.ground.draw(self.screen)
                self.displayText(self.font1,"You Found Easter EGG!",(WIDTH//2,HEIGHT//2))
                self.displayText(self.font2,"Game Finished! You win!",(WIDTH//2,HEIGHT//1.5))
                self.displayText(self.font2,"Have a great egg day.",(WIDTH//2,HEIGHT//1.3))
                self.displayText(self.font2,"Developed by Thura Soe!",(20,30),False)

            pygame.display.flip()
            time.tick(120)
            
        pygame.quit()
        sys.exit()
    
    def displayText(self,font,text,pos,flag=True):
        anykey_screen = font.render(text,True,(0,0,0))
        if flag:
            anykey_rect = anykey_screen.get_rect(center=pos)
        else:
            anykey_rect = anykey_screen.get_rect(topleft=pos)
        self.screen.blit(anykey_screen,anykey_rect)
    


if __name__ == "__main__":
    game = GameScreen()
    game.run()
