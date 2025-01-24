import pygame
import random
import math
import colorsys

# 初始化 Pygame
pygame.init()

# 游戏窗口设置
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 创建游戏窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("炫酷贪吃蛇")
clock = pygame.time.Clock()

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.lifetime = 30
        self.color = (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self, screen):
        alpha = int((self.lifetime / 30) * 255)
        surf = pygame.Surface((4, 4))
        surf.set_alpha(alpha)
        surf.fill(self.color)
        screen.blit(surf, (int(self.x), int(self.y)))

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow = False
        self.particles = []
        self.hue = 0

    def update(self):
        # 更新蛇的位置
        new_head = (
            (self.body[0][0] + self.direction[0]) % GRID_WIDTH,
            (self.body[0][1] + self.direction[1]) % GRID_HEIGHT
        )
        
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
            # 添加粒子效果
            x = new_head[0] * GRID_SIZE
            y = new_head[1] * GRID_SIZE
            for _ in range(10):
                self.particles.append(Particle(x, y))

        # 更新粒子
        self.particles = [p for p in self.particles if p.update()]
        
        # 更新色相
        self.hue = (self.hue + 0.01) % 1.0

    def draw(self, screen):
        # 绘制粒子
        for particle in self.particles:
            particle.draw(screen)

        # 绘制蛇身
        for i, (x, y) in enumerate(self.body):
            hue = (self.hue + i * 0.02) % 1.0
            rgb = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1, 1)]
            pygame.draw.rect(screen, rgb, 
                           (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2),
                           border_radius=8)

class Food:
    def __init__(self):
        self.position = self.random_position()
        self.color = (255, 50, 50)
        self.glow = 0
        self.glow_direction = 1

    def random_position(self):
        return (random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1))

    def draw(self, screen):
        self.glow = (self.glow + 0.1 * self.glow_direction)
        if self.glow >= 1:
            self.glow_direction = -1
        elif self.glow <= 0:
            self.glow_direction = 1

        # 绘制食物光晕
        radius = GRID_SIZE // 2 + self.glow * 5
        pos = (self.position[0] * GRID_SIZE + GRID_SIZE // 2,
               self.position[1] * GRID_SIZE + GRID_SIZE // 2)
        
        surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, 50), (radius, radius), radius)
        screen.blit(surf, (pos[0] - radius, pos[1] - radius))
        
        # 绘制食物主体
        pygame.draw.circle(screen, self.color, pos, GRID_SIZE // 2)

def main():
    snake = Snake()
    food = Food()
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)
            elif event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    snake = Snake()
                    food = Food()
                    game_over = False

        if not game_over:
            # 渐变背景
            for y in range(HEIGHT):
                color = [int(c * 255) for c in colorsys.hsv_to_rgb(y/HEIGHT, 0.2, 0.1)]
                pygame.draw.line(screen, color, (0, y), (WIDTH, y))

            # 更新游戏状态
            snake.update()

            # 检测吃到食物
            if snake.body[0] == food.position:
                snake.grow = True
                food.position = food.random_position()
                while food.position in snake.body:
                    food.position = food.random_position()

            # 检测碰撞
            if snake.body[0] in snake.body[1:]:
                game_over = True

            # 绘制游戏元素
            food.draw(screen)
            snake.draw(screen)

        else:
            # 游戏结束画面
            font = pygame.font.Font(None, 74)
            text = font.render('Game Over!', True, WHITE)
            text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(text, text_rect)

            font = pygame.font.Font(None, 36)
            text = font.render('Press SPACE to restart', True, WHITE)
            text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()