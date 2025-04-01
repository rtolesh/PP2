import pygame
import math

pygame.init()
FPS = 120
FramePerSec = pygame.time.Clock()
# Setting window size
win_x = 500
win_y = 500

win = pygame.display.set_mode((win_x, win_y))
pygame.display.set_caption('Paint')

# Class for drawing
class Drawing(object):

    def __init__(self):
        self.color = (0, 0, 0)
        self.width = 10
        self.height = 10
        self.rad = 5
        self.tick = 0
        self.time = 0
        self.play = False
        
        self.draw_circle_mode = False
        self.draw_rect_mode = False
        self.draw_square_mode = False
        self.draw_right_triangle_mode = False
        self.draw_equilateral_triangle_mode = False
        self.draw_rhombus_mode = False

        self.rect_start_pos = None
        self.circle_start_pos = None
        self.square_start_pos = None
        self.right_triangle_start_pos = None
        self.equilateral_triangle_start_pos = None
        self.rhombus_start_pos = None

    # Drawing Circle Function
    def draw_circle_shape(self, win, start_pos, end_pos, rad):
        center = start_pos  # Центр круга — это точка, где нажали
        pygame.draw.circle(win, self.color, center, rad)

    # Drawing Rectangle Function
    def draw_rect_shape(self, win, start_pos, end_pos):
        rect = pygame.Rect(start_pos[0], start_pos[1],
                           end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
        pygame.draw.rect(win, self.color, rect)

    # Drawing Square Function
    def draw_square_shape(self, win, start_pos, end_pos):
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        side = min(abs(dx), abs(dy))
        if dx >= 0 and dy >= 0:
            rect = pygame.Rect(start_pos[0], start_pos[1], side, side)
        elif dx < 0 and dy >= 0:
            rect = pygame.Rect(start_pos[0] - side, start_pos[1], side, side)
        elif dx >= 0 and dy < 0:
            rect = pygame.Rect(start_pos[0], start_pos[1] - side, side, side)
        else:
            rect = pygame.Rect(start_pos[0] - side, start_pos[1] - side, side, side)
        pygame.draw.rect(win, self.color, rect)

    # Drawing Right Triangle Function (прямоугольный треугольник, где прямой угол в точке нажатия)
    def draw_right_triangle(self, win, start_pos, end_pos):
        p1 = start_pos
        p2 = (start_pos[0], end_pos[1])
        p3 = (end_pos[0], start_pos[1])
        pygame.draw.polygon(win, self.color, [p1, p2, p3])

    # Drawing Equilateral Triangle Function
    def draw_equilateral_triangle(self, win, start_pos, end_pos):
        x1, y1 = start_pos
        x2, y2 = end_pos
        dx = x2 - x1
        dy = y2 - y1
        # Вычисляем длину стороны
        L = math.sqrt(dx**2 + dy**2)
        # Находим середину отрезка
        midx = (x1 + x2) / 2
        midy = (y1 + y2) / 2
        # Вычисляем координаты третьей вершины:
        # Поворачиваем вектор (dx, dy) на 90° и масштабируем до высоты равностороннего треугольника
        x3 = midx - (math.sqrt(3) * dy) / 2
        y3 = midy + (math.sqrt(3) * dx) / 2
        pygame.draw.polygon(win, self.color, [start_pos, end_pos, (x3, y3)])

    # Drawing Rhombus Function (ромб, рисуемый как ромб с вершинами в серединах сторон ограничивающего прямоугольника)
    def draw_rhombus(self, win, start_pos, end_pos):
        x1, y1 = start_pos
        x2, y2 = end_pos
        # Центр диагонали
        midx = (x1 + x2) / 2
        midy = (y1 + y2) / 2
        dx = (x2 - x1) / 2
        dy = (y2 - y1) / 2
        # Коэффициент вытягивания
        elongation = 1.2
        # Остальные вершины получаются смещением от центра перпендикулярно диагонали с учетом коэффициента
        p2 = (midx + elongation * dy, midy - elongation * dx)
        p4 = (midx - elongation * dy, midy + elongation * dx)
        pygame.draw.polygon(win, self.color, [start_pos, p2, end_pos, p4])



    def draw(self, win, pos):
        pygame.draw.circle(win, self.color, (pos[0], pos[1]), self.rad)
        if self.color == (255, 255, 255):
            pygame.draw.circle(win, self.color, (pos[0], pos[1]), 20)

    # detecting clicks
    def click(self, win, list_buttons, list2_buttons):
        pos = pygame.mouse.get_pos()
        left_button_down = pygame.mouse.get_pressed()[0]

        if left_button_down and pos[0] < 400:
            if self.draw_circle_mode:
                if self.circle_start_pos is None:
                    self.circle_start_pos = pos
                else:
                    rad = int(((pos[0] - self.circle_start_pos[0]) ** 2 + (pos[1] - self.circle_start_pos[1]) ** 2) ** 0.5)
                    self.draw_circle_shape(win, self.circle_start_pos, pos, rad)
            elif self.draw_rect_mode:
                if self.rect_start_pos is None:
                    self.rect_start_pos = pos
                else:
                    self.draw_rect_shape(win, self.rect_start_pos, pos)
            elif self.draw_square_mode:
                if self.square_start_pos is None:
                    self.square_start_pos = pos
                else:
                    self.draw_square_shape(win, self.square_start_pos, pos)
            elif self.draw_right_triangle_mode:
                if self.right_triangle_start_pos is None:
                    self.right_triangle_start_pos = pos
                else:
                    self.draw_right_triangle(win, self.right_triangle_start_pos, pos)
            elif self.draw_equilateral_triangle_mode:
                if self.equilateral_triangle_start_pos is None:
                    self.equilateral_triangle_start_pos = pos
                else:
                    self.draw_equilateral_triangle(win, self.equilateral_triangle_start_pos, pos)
            elif self.draw_rhombus_mode:
                if self.rhombus_start_pos is None:
                    self.rhombus_start_pos = pos
                else:
                    self.draw_rhombus(win, self.rhombus_start_pos, pos)
            else:
                self.draw(win, pos)
        elif not left_button_down:
            if self.draw_rect_mode and self.rect_start_pos is not None:
                self.draw_rect_mode = False
                self.rect_start_pos = None
            if self.draw_circle_mode and self.circle_start_pos is not None:
                self.circle_start_pos = None
            if self.draw_square_mode and self.square_start_pos is not None:
                self.square_start_pos = None
            if self.draw_right_triangle_mode and self.right_triangle_start_pos is not None:
                self.right_triangle_start_pos = None
            if self.draw_equilateral_triangle_mode and self.equilateral_triangle_start_pos is not None:
                self.equilateral_triangle_start_pos = None
            if self.draw_rhombus_mode and self.rhombus_start_pos is not None:
                self.rhombus_start_pos = None
        elif left_button_down:
            for button in list_buttons:
                if button.x < pos[0] < button.x + button.width and button.y < pos[1] < button.y + button.height:
                    self.color = button.color2
            for button in list2_buttons:
                if button.x < pos[0] < button.x + button.width and button.y < pos[1] < button.y + button.height:
                    if self.tick == 0:
                        if button.action == 1:
                            win.fill((255, 255, 255))
                            self.tick += 1
                        if button.action == 2 and self.rad > 4:
                            self.rad -= 1
                            self.tick += 1
                        if button.action == 3 and self.rad < 20:
                            self.rad += 1
                            self.tick += 1
                        if button.action == 5 and not self.play:
                            self.play = True
                            self.time += 1
                        if button.action == 6:
                            self.play = False
                            self.time = 0
        for button in list2_buttons:
            if button.action == 4:
                button.text = str(self.rad)
            if button.action == 7:
                button.text = str(40 - (self.time // 100)) if self.play else 'Time'

# Class for buttons
class Button(object):

    def __init__(self, x, y, width, height, color, color2, outline=0, action=0, text=''):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.outline = outline
        self.color2 = color2
        self.action = action
        self.text = text

    # Class for drawing buttons
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y,
                                             self.width, self.height), self.outline)
        font = pygame.font.SysFont('comicsans', 30)
        text = font.render(self.text, True, self.color2)
        pygame.draw.rect(win, (255, 255, 255), (410, 446, 80, 35))
        win.blit(text, (int(self.x + self.width / 2 - text.get_width() / 2),
                        int(self.y + self.height / 2 - text.get_height() / 2)))

def drawHeader(win):
    # Drawing header space
    pygame.draw.rect(win, (175, 171, 171), (0, 0, 500, 25))
    pygame.draw.rect(win, (0, 0, 0), (0, 0, 400, 25), 2)
    pygame.draw.rect(win, (0, 0, 0), (400, 0, 100, 25), 2)

    # Printing header
    font = pygame.font.SysFont('comicsans', 30)

    canvasText = font.render('Пэйнт', True, (0, 0, 0))
    win.blit(canvasText, (int(200 - canvasText.get_width() / 2),
                          int(26 / 2 - canvasText.get_height() / 2) + 2))

    toolsText = font.render('Tools', True, (0, 0, 0))
    win.blit(toolsText, (int(450 - toolsText.get_width() / 2),
                         int(26 / 2 - toolsText.get_height() / 2 + 2)))

def draw(win):
    player1.click(win, Buttons_color, Buttons_other)

    pygame.draw.rect(win, (0, 0, 0), (400, 0, 100, 500), 2)  # Drawing button space
    pygame.draw.rect(win, (255, 255, 255), (400, 0, 100, 500))
    pygame.draw.rect(win, (0, 0, 0), (0, 0, 400, 500), 2)  # Drawing canvas space
    drawHeader(win)

    for button in Buttons_color:
        button.draw(win)

    for button in Buttons_other:
        button.draw(win)

    pygame.display.update()

def main_loop():
    run = True
    while run:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False
            if event.type == pygame.KEYDOWN:
                # Сброс всех режимов по нажатию SPACE
                if event.key == pygame.K_SPACE:
                    player1.draw_circle_mode = False
                    player1.draw_rect_mode = False
                    player1.draw_square_mode = False
                    player1.draw_right_triangle_mode = False
                    player1.draw_equilateral_triangle_mode = False
                    player1.draw_rhombus_mode = False
                    player1.rect_start_pos = None
                    player1.circle_start_pos = None
                    player1.square_start_pos = None
                    player1.right_triangle_start_pos = None
                    player1.equilateral_triangle_start_pos = None
                    player1.rhombus_start_pos = None
                elif event.key == pygame.K_c:
                    player1.draw_circle_mode = True
                    player1.draw_rect_mode = False
                    player1.draw_square_mode = False
                    player1.draw_right_triangle_mode = False
                    player1.draw_equilateral_triangle_mode = False
                    player1.draw_rhombus_mode = False
                elif event.key == pygame.K_r:
                    player1.draw_rect_mode = True
                    player1.draw_circle_mode = False
                    player1.draw_square_mode = False
                    player1.draw_right_triangle_mode = False
                    player1.draw_equilateral_triangle_mode = False
                    player1.draw_rhombus_mode = False
                elif event.key == pygame.K_q:  # Рисуем квадрат
                    player1.draw_square_mode = True
                    player1.draw_circle_mode = False
                    player1.draw_rect_mode = False
                    player1.draw_right_triangle_mode = False
                    player1.draw_equilateral_triangle_mode = False
                    player1.draw_rhombus_mode = False
                elif event.key == pygame.K_w:  # Рисуем прямоугольный (правый) треугольник
                    player1.draw_right_triangle_mode = True
                    player1.draw_square_mode = False
                    player1.draw_circle_mode = False
                    player1.draw_rect_mode = False
                    player1.draw_equilateral_triangle_mode = False
                    player1.draw_rhombus_mode = False
                elif event.key == pygame.K_e:  # Рисуем равносторонний треугольник
                    player1.draw_equilateral_triangle_mode = True
                    player1.draw_square_mode = False
                    player1.draw_right_triangle_mode = False
                    player1.draw_circle_mode = False
                    player1.draw_rect_mode = False
                    player1.draw_rhombus_mode = False
                elif event.key == pygame.K_d:  # Рисуем ромб
                    player1.draw_rhombus_mode = True
                    player1.draw_equilateral_triangle_mode = False
                    player1.draw_square_mode = False
                    player1.draw_right_triangle_mode = False
                    player1.draw_circle_mode = False
                    player1.draw_rect_mode = False

        draw(win)

        if 0 < player1.tick < 40:
            player1.tick += 1
        else:
            player1.tick = 0

        if 0 < player1.time < 4001:
            player1.time += 1
        elif 4000 < player1.time < 4004:
            player1.time = 4009
        else:
            player1.time = 0
            player1.play = False

    pygame.quit()

player1 = Drawing()
# Fill colored to our paint
win.fill((255, 255, 255))
pos = (0, 0)

# Defining color buttons
redButton = Button(453, 30, 40, 40, (255, 0, 0), (255, 0, 0))
blueButton = Button(407, 30, 40, 40, (0, 0, 255), (0, 0, 255))
greenButton = Button(407, 76, 40, 40, (0, 255, 0), (0, 255, 0))
orangeButton = Button(453, 76, 40, 40, (255, 192, 0), (255, 192, 0))
yellowButton = Button(407, 122, 40, 40, (255, 255, 0), (255, 255, 0))
purpleButton = Button(453, 122, 40, 40, (112, 48, 160), (112, 48, 160))
blackButton = Button(407, 168, 40, 40, (0, 0, 0), (0, 0, 0))
whiteButton = Button(453, 168, 40, 40, (0, 0, 0), (255, 255, 255), 1)

# Defining other buttons
clrButton = Button(407, 214, 86, 40, (201, 201, 201), (0, 0, 0), 0, 1, 'Clear')
smallerButton = Button(407, 260, 40, 40, (201, 201, 201), (0, 0, 0), 0, 2, '-')
biggerButton = Button(453, 260, 40, 40, (201, 201, 201), (0, 0, 0), 0, 3, '+')
sizeDisplay = Button(407, 306, 86, 40, (0, 0, 0), (0, 0, 0), 1, 4, 'Size')

Buttons_color = [blueButton, redButton, greenButton, orangeButton,
                 yellowButton, purpleButton, blackButton, whiteButton]
Buttons_other = [clrButton, smallerButton, biggerButton,
                 sizeDisplay]

main_loop()
FramePerSec.tick(FPS)
