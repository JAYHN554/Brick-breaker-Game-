import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Brick Breaker')

# Set up the clock for a decent framerate
clock = pygame.time.Clock()

# Set up the font for displaying text
font = pygame.font.SysFont('Arial', 24)
large_font = pygame.font.SysFont('Arial', 48)

class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 10
        self.color = (255, 255, 255)
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - 30
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def move(self, direction):
        if direction == 'left' and self.rect.left > 0:
            self.rect.x -= self.speed
        if direction == 'right' and self.rect.right < screen_width:
            self.rect.x += self.speed

class Ball:
    def __init__(self):
        self.radius = 10
        self.color = (255, 0, 0)
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.speed_x = 5
        self.speed_y = 5
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x - self.radius <= 0 or self.x + self.radius >= screen_width:
            self.speed_x *= -1
        if self.y - self.radius <= 0:
            self.speed_y *= -1

class Brick:
    def __init__(self, x, y):
        self.width = 75
        self.height = 20
        self.color = (0, 255, 0)
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

def main_menu():
    while True:
        screen.fill((0, 0, 0))
        title_text = large_font.render('Brick Breaker', True, (255, 255, 255))
        start_text = font.render('Press S to Start or Q to Quit', True, (255, 255, 255))
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 2 - 100))
        screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 2))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()
        clock.tick(60)

def game_over_menu(score):
    while True:
        screen.fill((0, 0, 0))
        game_over_text = large_font.render('Game Over', True, (255, 255, 255))
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        restart_text = font.render('Press R to Restart or Q to Quit', True, (255, 255, 255))
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 100))
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - 50))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()
        clock.tick(60)

def main_game():
    paddle = Paddle()
    ball = Ball()
    bricks = []
    for i in range(5):
        for j in range(8):
            bricks.append(Brick(j * 80 + 10, i * 30 + 10))

    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move('left')
        if keys[pygame.K_RIGHT]:
            paddle.move('right')
        
        ball.move()
        
        if ball.y + ball.radius >= paddle.rect.top and paddle.rect.left <= ball.x <= paddle.rect.right:
            ball.speed_y *= -1
        
        if ball.y + ball.radius >= screen_height:
            game_over_menu(score)
            return
        
        for brick in bricks[:]:
            if brick.rect.collidepoint(ball.x, ball.y):
                ball.speed_y *= -1
                bricks.remove(brick)
                score += 10
        
        screen.fill((0, 0, 0))
        paddle.draw()
        ball.draw()
        for brick in bricks:
            brick.draw()
        
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)

while True:
    main_menu()
    main_game()
