import pygame
import os
import datetime
_image_library = {}
def get_image(path):
    global _image_library
    if path not in _image_library:
        if not os.path.exists(path):
            print(f"Ошибка: файл {path} не найден.")
            return None
        _image_library[path] = pygame.image.load(path)
    return _image_library[path]

def blitRotate(screen, img, pos, angle):
    if img is None:
        return
    rotated_img = pygame.transform.rotate(img, angle)
    new_rect = rotated_img.get_rect(center=img.get_rect(center=pos).center)
    screen.blit(rotated_img, new_rect.topleft)

pygame.init()
screen = pygame.display.set_mode((1200, 800))
w, h = screen.get_size()
pygame.display.set_caption("Mickey's Clock")
bg = pygame.transform.scale(get_image(r"C:/Users/user/Desktop/lab1/lab7/clock.png"), (w, h))
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_ESCAPE:
                done = True

    today = datetime.datetime.now()
    minutes = today.minute
    seconds = today.second
    pos = (w // 2, h // 2)
    angle_min = -6 * minutes - 53
    angle_sec = -6 * seconds
    screen.blit(bg, (0, 0))
    blitRotate(screen, get_image(r"C:/Users/user/Desktop/lab1/lab7/leftarm.png"), pos, angle_sec)
    blitRotate(screen, get_image(r"C:/Users/user/Desktop/lab1/lab7/rightarm.png"), pos, angle_min)
    pygame.display.flip()

pygame.quit()
