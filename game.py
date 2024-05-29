import pygame
import random

pygame.init()

#set display
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH , WINDOW_HEIGHT))
pygame.display.set_caption("Monster Wrangler")

#set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#game class
class Game():
    def __init__(self , player , monster_group):
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.frame_count = 0

        self.player = player
        self.monster_group = monster_group

        self.next_level = pygame.mixer.Sound('Assets/next_level.wav')

        #set font
        self.font = pygame.font.Font('Assets/custom.ttf' , 24)

        #set images
        blue_image = pygame.image.load('Assets/blue_monster.png')
        orange_image = pygame.image.load('Assets/orange_monster.png')
        green_image = pygame.image.load('Assets/green_monster.png')
        purple_image = pygame.image.load('Assets/purple_monster.png')

        self.target_monster_images = [blue_image , green_image , purple_image , orange_image]

        self.target_monster_type = random.randint(0 , 3)
        self.target_monster_image = self.target_monster_images[self.target_monster_type]
        
        self.target_monster_rect = self.target_monster_image.get_rect()
        self.target_monster_rect.centerx = WINDOW_WIDTH // 2
        self.target_monster_rect.top = 30

    def update(self):
        self.frame_count += 1
        if self.frame_count == FPS:
            self.round_time += 1
            self.frame_count = 0

        #check collision
        self.check_collisions()

    def draw(self):
        #set colors
        WHITE = (255 ,255 ,255)
        BLUE = (20 , 176 , 235)
        GREEN = (87 , 201 , 47)
        PURPLE = (246 , 73 ,243)
        ORANGE = (243 , 157 , 20)

        #add colors to the list where the color matches the target monster type
        color = [BLUE , GREEN , PURPLE , ORANGE ]

        #set text
        catch_text = self.font.render('Current Catch' , 1, WHITE)
        catch_rect = catch_text.get_rect()
        catch_rect.centerx = WINDOW_WIDTH // 2
        catch_rect.top =  5

        score_text = self.font.render('Score ' + str(self.score) , 1, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (5 , 5)

        lives_text = self.font.render("Lives " + str(player.lives) , 1, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (2 , 35)

        round_text = self.font.render("Current Round:" + str(self.round_number) , 1, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (5 , 65)

        time_text  = self.font.render("Round time: " + str(self.round_time) , 1, WHITE)
        time_rect = time_text.get_rect()
        time_rect.topright = (WINDOW_WIDTH - 10 , 5)

        wrap_text = self.font.render("Wraps " + str(player.wraps) , 1, WHITE)
        wrap_rect = wrap_text.get_rect()
        wrap_rect.topright = (WINDOW_WIDTH - 10 , 35)

        #blit the hub
        display_surface.blit(catch_text , catch_rect)
        display_surface.blit(score_text ,score_rect)
        display_surface.blit(round_text , round_rect)
        display_surface.blit(lives_text , lives_rect)
        display_surface.blit(time_text , time_rect)
        display_surface.blit(wrap_text , wrap_rect)
        display_surface.blit(self.target_monster_image , self.target_monster_rect)
        
        pygame.draw.rect(display_surface , color[self.target_monster_type] , (WINDOW_WIDTH // 2 -32 , 30 , 64 , 64) , 2)
        pygame.draw.rect(display_surface , color[self.target_monster_type] , (0 , 100 , WINDOW_WIDTH , WINDOW_HEIGHT - 200) , 2)
    def check_collisions(self):
        collided_monster = pygame.sprite.spritecollideany(self.player , self.monster_group)
        if collided_monster:
            if collided_monster.type ==  self.target_monster_type:
                self.score += 100 * self.round_number

                #remove caught monster
                collided_monster.remove(self.monster_group)
                if self.monster_group:
                    #there are monsters to catch
                    self.player.catch_sound.play()
                    self.choose_new_target()
                else:
                    self.player.reset()
                    self.start_new_round()
            else:
                self.player.die_sound.play()
                self.player.lives -= 1
                if self.player.lives <= 0:
                    self.pause_game("Final Score: " + str(self.score) , "Press enter to play again")
                    self.reset_game()
                self.player.reset()

    def start_new_round(self):
        self.score += int(10000 * self.round_number / (1 + self.round_time))

        #reset round values
        self.round_time = 0
        self.frame_count = 0
        self.round_number += 1
        self.player.wraps += 1

        for monster in self.monster_group:
            self.monster_group.remove(monster)

        for i in range(self.round_number):
            self.monster_group.add(Monster(random.randint(0 , WINDOW_WIDTH - 64) , random.randint(100 , WINDOW_HEIGHT - 164) , self.target_monster_images[0] , 0))
            self.monster_group.add(Monster(random.randint(0 , WINDOW_WIDTH - 64) , random.randint(100 , WINDOW_HEIGHT - 164) , self.target_monster_images[1] , 1))
            self.monster_group.add(Monster(random.randint(0 , WINDOW_WIDTH - 64) , random.randint(100 , WINDOW_HEIGHT - 164) , self.target_monster_images[2] , 2))
            self.monster_group.add(Monster(random.randint(0 , WINDOW_WIDTH - 64) , random.randint(100 , WINDOW_HEIGHT - 164) , self.target_monster_images[3] , 3))
        
        self.choose_new_target()
        self.next_level.play()
    def choose_new_target(self):
        target_monster = random.choice(self.monster_group.sprites())
        self.target_monster_type = target_monster.type
        self.target_monster_image = target_monster.image
        
    def pause_game(self , main_text , sub_text):
        #set color
        WHITE = (255 ,255 ,255)
        BLACK = (0 , 0, 0)
        #create text 
        main_text = self.font.render(main_text , 1, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH // 2 , WINDOW_HEIGHT //2)

        sub_text = self.font.render(sub_text , 1, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH // 2 , WINDOW_HEIGHT //2 + 64)

        display_surface.fill(BLACK)
        display_surface.blit(sub_text , sub_rect)
        display_surface.blit(main_text , main_rect)
        pygame.display.update()
        global running
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                if event.type == pygame.QUIT:
                    running = False
                    is_paused = False

    def reset_game(self):
        self.score = 0
        self.round_number = 0

        self.player.lives = 5
        self.player.wraps = 2
        self.player.reset()

        self.start_new_round()

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Assets/knight.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT

        self.lives = 3
        self.wraps = 2
        self.velocity = 8

        self.catch_sound = pygame.mixer.Sound('Assets/catch.wav')
        self.die_sound = pygame.mixer.Sound('Assets/die.wav')
        self.wrap_sound = pygame.mixer.Sound('Assets/wrap.wav')

    def update(self):
        keys = pygame.key.get_pressed()

        #move
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and self.rect.top > 100:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT - 100:
            self.rect.y += self.velocity
    def wrap(self):
        if self.wraps > 0:
            
            self.wraps -= 1
            self.wrap_sound.play()
            self.rect.bottom = WINDOW_HEIGHT

    def reset(self):
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT

#monster class
class Monster(pygame.sprite.Sprite):
    def __init__(self , x , y , image , monster_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x , y)

        #monster type 0->blue 1->green 2->purple 3->orange
        self.type = monster_type

        self.dx = random.choice([-1 , 1])
        self.dy = random.choice([-1 , 1])
        self.velocity = random.randint(1 , 5)
    
    def update(self):
        self.rect.x += self.dx * self.velocity
        self.rect.y += self.dy * self.velocity

        #bounce the monster of the edges
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.dx = -1 * self.dx
        if self.rect.top <= 100 or self.rect.bottom >= WINDOW_HEIGHT - 100:
            self.dy =  -1 * self.dy

#player group
player_group = pygame.sprite.Group()
player = Player()
player_group.add(player)

#monster group
monster_group = pygame.sprite.Group()


#game object
my_game = Game(player , monster_group)
my_game.pause_game("Pause game" , "Press eenter to begin")
my_game.start_new_round()

#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.wrap()
    #fill the display
    display_surface.fill((0 , 0, 0))
    
    #update sprite groups
    player_group.update()
    player_group.draw(display_surface)
    
    monster_group.update()
    monster_group.draw(display_surface)

    #update and draw the game
    my_game.update()
    my_game.draw()
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
