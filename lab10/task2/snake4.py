import pygame
import random
import time
import psycopg2

# === Database configuration ===
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = '12345678910'

def init_db():
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_score (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            score INTEGER,
            level INTEGER,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_or_create_user(username):
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    row = cur.fetchone()
    if row:
        user_id = row[0]
    else:
        cur.execute(
            "INSERT INTO users (username) VALUES (%s) RETURNING id",
            (username,)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
    cur.close()
    conn.close()
    return user_id

def get_last_score_level(user_id):
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT score, level
          FROM user_score
         WHERE user_id = %s
         ORDER BY saved_at DESC
         LIMIT 1
    """, (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return row[0], row[1]
    return 0, 1

def save_progress(user_id, score, level):
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)",
        (user_id, score, level)
    )
    conn.commit()
    cur.close()
    conn.close()

# === Запрос имени и загрузка прогресса ===
username = input("Enter your username: ")
init_db()
user_id = get_or_create_user(username)
last_score, last_level = get_last_score_level(user_id)
print(f"Welcome, {username}! Last score: {last_score}, last level: {last_level}")

# === Pygame setup ===
CELL_SIZE = 20
GRID_WIDTH = 32
GRID_HEIGHT = 22

colors = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'RED':   (255, 0, 0),
}

pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE + 60))
pygame.display.set_caption("Snake with DB")
clock = pygame.time.Clock()

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y
    def out_of_bounds(self):
        return not (0 <= self.x < GRID_WIDTH and 0 <= self.y < GRID_HEIGHT)

class Snake:
    def __init__(self, score=0, level=1):
        # безопасная зона спавна: верхний левый угол
        self.body = [Point(5, 5), Point(5, 6), Point(5, 7)]
        # стартовое движение вправо (по умолчанию вправо) :contentReference[oaicite:2]{index=2}
        self.dx, self.dy = 1, 0
        self.score = score
        self.level = level

    def move(self):
        new_head = Point(self.body[0].x + self.dx, self.body[0].y + self.dy)
        if new_head.out_of_bounds() or new_head in self.body:
            return False
        if self.level in walls and new_head in walls[self.level]:
            return False
        self.body.insert(0, new_head)
        if new_head != food.pos:
            self.body.pop()
        else:
            self.score += random.randint(1, 2)
            self.level = 1 + self.score // 4
            food.respawn(self)
        return True

    def draw(self):
        for seg in self.body:
            pygame.draw.rect(
                screen, colors['BLACK'],
                (seg.x * CELL_SIZE, seg.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

class Food:
    def __init__(self, color, snake):
        self.color = color
        self.pos = self._get_random_pos(snake)
    def _get_random_pos(self, snake):
        while True:
            p = Point(random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
            if p not in snake.body:
                return p
    def draw(self):
        pygame.draw.rect(
            screen, self.color,
            (self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )
    def respawn(self, snake):
        self.pos = self._get_random_pos(snake)

# уровни со стенами
walls = {}

def generate_walls(level):
    if level % 2 == 0:
        # Пример: горизонтальная полоса посередине
        return [Point(x, GRID_HEIGHT // 2) for x in range(5, GRID_WIDTH - 5)]
    return []

# инициализация объектов
snake = Snake(score=last_score, level=last_level)
food = Food(colors['RED'], snake)
paused = False

# —————— ПЕРВОНАЧАЛЬНАЯ ОТРИСОВКА + ПАУЗА ——————
screen.fill(colors['WHITE'])
for lvl, segs in walls.items():
    if lvl == snake.level:
        for w in segs:
            pygame.draw.rect(
                screen, colors['BLACK'],
                (w.x * CELL_SIZE, w.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
food.draw()
snake.draw()
font = pygame.font.SysFont('Verdana', 20)
info = font.render(
    f"{username} | Score: {snake.score} | Level: {snake.level}",
    True, colors['RED']
)
screen.blit(info, (10, GRID_HEIGHT * CELL_SIZE + 5))
pygame.display.flip()
pygame.event.pump()  # даём окну шанс отрисоваться :contentReference[oaicite:3]{index=3}
time.sleep(1)

# главный цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_p:
                paused = not paused
                if paused:
                    save_progress(user_id, snake.score, snake.level)
                    print("Game paused and saved.")
                else:
                    print("Resuming game.")
            elif not paused:
                if event.key == pygame.K_a and snake.dx == 0:
                    snake.dx, snake.dy = -1, 0
                elif event.key == pygame.K_d and snake.dx == 0:
                    snake.dx, snake.dy = 1, 0
                elif event.key == pygame.K_w and snake.dy == 0:
                    snake.dx, snake.dy = 0, -1
                elif event.key == pygame.K_s and snake.dy == 0:
                    snake.dx, snake.dy = 0, 1

    if paused:
        screen.fill(colors['WHITE'])
        snake.draw()
        food.draw()
        pygame.display.flip()
        clock.tick(5)
        continue

    if not snake.move():
        break

    if snake.level not in walls:
         walls[snake.level] = generate_walls(snake.level)

    screen.fill(colors['WHITE'])
    for lvl, segs in walls.items():
        if lvl == snake.level:
            for w in segs:
                pygame.draw.rect(
                    screen, colors['BLACK'],
                    (w.x * CELL_SIZE, w.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
    food.draw()
    snake.draw()

    fps = 5 + (snake.level - 1) * 2
    font = pygame.font.SysFont('Verdana', 20)
    info = font.render(
        f"{username} | Score: {snake.score} | Level: {snake.level}",
        True, colors['RED']
    )
    screen.blit(info, (10, GRID_HEIGHT * CELL_SIZE + 5))

    pygame.display.flip()
    clock.tick(fps)

# Game Over
font = pygame.font.SysFont('Verdana', 60)
go_surf = font.render("GAME OVER", True, colors['RED'])
screen.blit(go_surf, (
    (GRID_WIDTH * CELL_SIZE - go_surf.get_width()) // 2,
    (GRID_HEIGHT * CELL_SIZE - go_surf.get_height()) // 2
))
pygame.display.flip()

save_progress(user_id, snake.score, snake.level)
time.sleep(3)
pygame.quit()