import pygame
import time
import random

snake_speed = 15

# размер окна
window_x = 720
window_y = 480

# определение цветов
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# инициализация
pygame.init()

# Инициализирование игрового окна
pygame.display.set_caption('Змейка')
game_window = pygame.display.set_mode((window_x, window_y))

# Контроллер FPS (кадры в секунду)
fps = pygame.time.Clock()

# определение положения змеи по умолчанию
snake_position = [100, 50]

# определение первых 4 блоков тела змеи
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]

# начальное положение фрукта
fruit_position = [random.randrange(1, (window_x // 10)) * 10, 
                  random.randrange(1, (window_y // 10)) * 10]
fruit_spawn = True
fruit_lifetime = 5  # время жизни фрукта в секундах
fruit_spawn_time = time.time()  # время появления фрукта

# установка направления змеи по умолчанию к право
direction = 'RIGHT'
change_to = direction

# начальная оценка
level = 1
score = 0
score2 = 0

# отображение функции Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score) + "     Level :" + str(level), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

# функция завершения игры
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

# Основной цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Исключаем возможность движения в противоположном направлении
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Перемещение змеи
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Обновление тела змеи
    snake_body.insert(0, list(snake_position))
    
    # Если змея съела фрукт
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        ans = random.randint(10, 20)
        score += ans
        score2 += ans
        # Изменение скорости при повышении уровня
        if score2 > 30:
            level += 1
            score2 = 0
            snake_speed += 15
        fruit_spawn = False  # фрукт съеден, сброс флага
    else:
        snake_body.pop()

    # Проверка истечения времени жизни фрукта
    if fruit_spawn and (time.time() - fruit_spawn_time >= fruit_lifetime):
        fruit_spawn = False

    # Если фрукта нет (или он был съеден/исчез)
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]
        fruit_spawn = True
        fruit_spawn_time = time.time()  # новый таймер для нового фрукта

    game_window.fill(black)

    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    # Проверка на столкновение со стенами
    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()

    # Проверка на столкновение с собственным телом
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    show_score(1, white, 'times new roman', 20)
    pygame.display.update()
    fps.tick(snake_speed)
