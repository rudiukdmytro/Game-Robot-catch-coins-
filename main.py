import pygame 
from random import randint 
from datetime import datetime

WIDTH = 640
HEIGHT = 480

class Robot:
    def __init__(self):
        self.robot = pygame.image.load("robot.png")
        self.x = 0
        self.y = HEIGHT - self.robot.get_height()
        self.coins = 0
        self.health = 100
        self.to_left, self.to_right = False, False 

    def move(self):
        if self.to_left and self.x - 3 >= 0:
            self.x -= 4 
        if self.to_right and self.x + 3 <= WIDTH - self.robot.get_width():
            self.x += 4

    def middle(self):
        return self.x + self.robot.get_width()/2
 

class Character:
    def __init__(self, image: str, speed: int):
        self.image = pygame.image.load(image)
        self.name = image[:-4]
        self.speed = speed
        self.new_coordinates()

    def new_coordinates(self):
        self.x = randint(0, WIDTH - self.image.get_width())
        self.y = -randint(100, 200)

    def move(self):
        if self.y + self.speed <= HEIGHT - self.image.get_height():
            self.y += self.speed 
        else: 
            self.new_coordinates()

    def catch(self, robot: Robot):
        if self.y + self.image.get_height() >= robot.y:
            middle = self.x + self.image.get_width()/2 
            if abs(middle - robot.middle()) <= (self.image.get_width() + robot.robot.get_width())/2:
                if self.name == "coin":
                    robot.coins += 1 
                elif self.name == "monster":
                    robot.health -= 10
                elif self.name == "rock":
                    robot.health -= 5  
                
                self.new_coordinates()



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("ROBOT CATCH COINS")
        self.clock = pygame.time.Clock()
        self.robot = Robot()

        self.game_font = pygame.font.SysFont("Arial", 24)
        self.text_health = self.game_font.render("HEALTH: ", True, (255,0,0))
        self.text_coins = self.game_font.render("COINS: ", True, (255,0,0))

        self.masive_coins = [Character("coin.png", 3) for i in range(5)] 
        self.masive_monsters = [Character("monster.png", 4) for i in range(3)]
        self.masive_rocks = [Character("rock.png", 2) for i in range(2)]

        self.start_ticks = pygame.time.get_ticks()
        self.main()

    def main(self):
        while True:
            self.events()
            self.draw()
            if self.robot.health <= 0:
                exit()
            self.clock.tick(60)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.robot.to_left = True 
                if event.key == pygame.K_RIGHT:
                    self.robot.to_right = True 


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.robot.to_left = False 
                if event.key == pygame.K_RIGHT:
                    self.robot.to_right = False 

    def draw_masive(self, masive: list):
        for i in range(len(masive)):
            masive[i].move()
            masive[i].catch(self.robot)
            self.screen.blit(masive[i].image, (masive[i].x, masive[i].y))

    def health_color(self):
        if self.robot.health >= 70:
            return (0,204,16)
        elif self.robot.health >= 40:
            return (255,151,0)
        else:
            return (255,17,0)

    def draw(self):
        self.screen.fill((159, 227, 207))
        self.robot.move()
        self.screen.blit(self.robot.robot, (self.robot.x, self.robot.y))
  

        self.draw_masive(self.masive_coins)
        self.draw_masive(self.masive_monsters)
        self.draw_masive(self.masive_rocks)
        pygame.draw.rect(self.screen, (255,255,255), (0,0, WIDTH, 25))

        self.screen.blit(self.text_health, (30, 0))
        persent = self.game_font.render(f"{self.robot.health} %", True, self.health_color())
        self.screen.blit(persent, (140, 0))
        self.screen.blit(self.text_coins, (450, 0))
        coins = self.game_font.render(f"{self.robot.coins}", True, (0,0,0))
        self.screen.blit(coins, (550, 0))
  
        elapsed_ms = pygame.time.get_ticks() - self.start_ticks
        minutes = elapsed_ms // 60000
        seconds = (elapsed_ms % 60000) // 1000
        timer_surface = self.game_font.render(f"{minutes:02}:{seconds:02}", True, (0, 0, 0))
        self.screen.blit(timer_surface, (WIDTH/2 - 50, 0))

        pygame.display.flip()


if __name__ == "__main__":
    Game()