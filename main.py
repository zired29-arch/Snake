import pygame
import sys
from random import randint

pygame.init()

class Sprite():
    def __init__(self, filename, x, y, width, height):
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self):
        background.blit(self.image, (self.rect.x, self.rect.y))
    
    def swap_image(self, filename):
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

class Apple(Sprite):
    def random_spawn(self):
        rand_x = randint(0, 9) * 50
        rand_y = randint(0, 9) * 50
        self.rect.x, self.rect.y = rand_x, rand_y

class SnakePart(Sprite):
    # TODO: СОздать новый класс sprite и в нем будет конструктор класса snakepart, создать новый класс apple который наследует sprite
    def __init__(self, filename, x, y, width, height, course):
        super().__init__(filename, x, y, width, height)
        self.course = course
    
    def change_direction(self, direction):
        '''
        Принимает новое направление
        Меняет направление текущей части и поворачивает картинку
        Вовзращает предыдущее направление
        '''
        self.image = pygame.transform.rotate(self.image, self.course - direction)
        temp_course = self.course # сохраняет предыдущий курс
        self.course = direction
        return temp_course


class Snake():
    courses = {
            0: (0, -1), #up
            180: (0, 1), #down
            -90: (-1, 0), #left
            90: (1, 0)} #right

    def __init__(self):
        self.step = 50
        self.snake_parts = [SnakePart("Sprites/Head.png", 250, 100, 50, 50, 90), SnakePart("Sprites/Body.png", 200, 100, 50, 50, 90),
                            SnakePart("Sprites/Tail.png", 150, 100, 50, 50, 90)]
    
    def make_step(self):
        temp_course = self.snake_parts[0].course # сохраняет курс головы
        for snake_part in self.snake_parts:
            snake_part.rect.x += Snake.courses[snake_part.course][0] * self.step # изменяет положение части тела по x
            snake_part.rect.y += Snake.courses[snake_part.course][1] * self.step # изменяет положение части тела по y
            temp_course = snake_part.change_direction(temp_course)
        if self.snake_parts[0].rect.x >= 500 or self.snake_parts[0].rect.x < 0 or self.snake_parts[0].rect.y >= 500 or self.snake_parts[0].rect.y < 0:
            exit()
        for snake_part in self.snake_parts[1:]:
            if self.snake_parts[0].rect.colliderect(snake_part.rect):
                exit()
    
    def draw_snake(self):
        for i in range(len(self.snake_parts)):
            self.snake_parts[i].draw()
    
    def grow(self):
        tail = self.snake_parts[-1]
        course = self.courses[tail.course]
        x = tail.rect.x - course[0] * self.step
        y = tail.rect.y - course[1] * self.step
        new_part = SnakePart("Sprites/Tail.png", x, y, 50, 50, tail.course)
        tail.swap_image("Sprites/Body.png")
        tail.image = pygame.transform.rotate(tail.image, -abs(tail.course - 90)) # 0
        print(tail.course)
        print(-abs(tail.course - 90))
        self.snake_parts.append(new_part)


snake = Snake()

clock = pygame.time.Clock()

background = pygame.display.set_mode((500, 500))
background.fill((65, 96, 159))

counter = 0

apple = Apple("Sprites/Apple.png", 300, 100, 50, 50)

apple.random_spawn()
while True:
    if counter == 15:
        snake.make_step()
        counter = 0
    if snake.snake_parts[0].rect.colliderect(apple.rect):
        apple.random_spawn()
        snake.grow()
    background.fill((65, 96, 159))
    apple.draw()
    snake.draw_snake()
    counter += 1
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and snake.snake_parts[0].course != 180:
                snake.snake_parts[0].change_direction(0)
            if event.key == pygame.K_a and snake.snake_parts[0].course != 90:
                snake.snake_parts[0].change_direction(-90)
            if event.key == pygame.K_s and snake.snake_parts[0].course != 0:
                snake.snake_parts[0].change_direction(180)
            if event.key == pygame.K_d and snake.snake_parts[0].course != -90:
                snake.snake_parts[0].change_direction(90)
        if event.type == pygame.QUIT:
            exit()
    pygame.display.update()
    clock.tick(60)