import random
import numpy as np
import pygame as pygame

# Constants
DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 400
BLOCK_SIZE = 20
SNAKE_SPEED = 15  
TRAINING_SPEED = 10  


pygame_initialized = False
display = None
clock = None

def initialize_pygame():
    global pygame, pygame_initialized, display, clock
    if not pygame_initialized:
        import pygame
        pygame.init()
        display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption('Snake Game for Reinforcement Learning')
        clock = pygame.time.Clock()
        pygame_initialized = True

class Snake:
    def __init__(self):
        self.reset()

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.size > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * BLOCK_SIZE)) ), (cur[1] + (y * BLOCK_SIZE)))
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.size:
                self.positions.pop()

    def reset(self):
        self.size = 1
        self.positions = [((DISPLAY_WIDTH // 2), (DISPLAY_HEIGHT // 2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.score = 0

    def get_observation(self, food):
        head_x, head_y = self.get_head_position()
        direction = self.direction
        food_x, food_y = food.position
        snake_body = self.positions

        observation = {
            "head_x": head_x,
            "head_y": head_y,
            "direction_0": direction[0],
            "direction_1":direction[1],
            "food_x": food_x,
            "food_y": food_y,
            "body_parts":len(snake_body)
            #"snake_body": snake_body
        }
        return observation

    def handle_key_event(self, key):
        if key == 0:  # UP
            self.turn((0, -1))
        elif key == 1:  # DOWN
            self.turn((0, 1))
        elif key == 2:  # LEFT
            self.turn((-1, 0))
        elif key == 3:  # RIGHT
            self.turn((1, 0))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (DISPLAY_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                         random.randint(0, (DISPLAY_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(surface, (213, 50, 80), r)

class SnakeGameEnv:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.game_over = False

    def reset(self):
        self.snake.reset()
        self.food.randomize_position()
        self.game_over = False
        return self.snake.get_observation(self.food)

    def step(self, action):
        self.snake.handle_key_event(action)
        self.snake.move()

        reward = 0
        if self.snake.get_head_position() == self.food.position:
            self.snake.size += 1
            self.snake.score += 1
            reward = 1  # Reward for eating food
            self.food.randomize_position()
        #print(self.snake.get_head_position())
        elif self.snake.get_head_position() in self.snake.positions[1:] or self.snake.get_head_position()[0] >= DISPLAY_WIDTH or  self.snake.get_head_position()[1] >= DISPLAY_HEIGHT or self.snake.get_head_position()[0]<0 or self.snake.get_head_position()[1]<0:
            
            self.game_over = True
            reward = -1  
        #else:
            #reward = -0.01

        observation = self.snake.get_observation(self.food)
        return observation, reward, self.game_over, {}

    def render(self):
        if not pygame_initialized:
            initialize_pygame()
        display.fill((0, 0, 0))
        for pos in self.snake.positions:
            pygame.draw.rect(display, (0, 255, 0), pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        self.food.draw(display)
        pygame.display.update()
        clock.tick(SNAKE_SPEED)

# Example training loop
def training_loop(env, num_episodes=1000, render=False):
    scores = []
    for episode in range(num_episodes):
        observation = env.reset()
        done = False
        score = 0
        while not done:
            action = random.randint(0, 3) 
            observation, reward, done, info = env.step(action)
            score += reward
            if render:
                env.render()
        scores.append(score)
        if not render:
            print(f"Episode {episode + 1}: Score {score}")
    return scores

if __name__ == "__main__":
    # initialize_pygame()
    env = SnakeGameEnv()
    # env.reset()
    # done = False
    # while not done:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             quit()
    #         elif event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_UP:
    #                 action = 0
    #             elif event.key == pygame.K_DOWN:
    #                 action = 1
    #             elif event.key == pygame.K_LEFT:
    #                 action = 2
    #             elif event.key == pygame.K_RIGHT:
    #                 action = 3
    #             observation, reward, done, info = env.step(action)
    #             env.render()
    #             if done:
    #                 break

    scores = training_loop(env, num_episodes=10, render=True) 
    print("Training completed.")