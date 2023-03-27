from logics import *
import pygame
import sys
from data_base import get_best, cur, insert_result
import json
import os

GAMERS_DB = get_best()


def draw_top_gamers():
    font_top = pygame.font.SysFont('impact', 20)
    font_gamer = pygame.font.SysFont('impact', 24)
    text_head = font_top.render("Best tries: ", True, COLOR_TEXT)
    screen.blit(text_head, (270, 5))
    for index, gamer in enumerate(GAMERS_DB):
        name, score = gamer
        s = f"{index + 1}. {name} - {score}"
        text_gamer = font_gamer.render(s, True, BLACK)
        screen.blit(text_gamer, (270, 30 + 25 * index))
        print(index, name, score)


def draw_interfase(score, delta=0):
    pygame.draw.rect(screen, WHITE, TITLE_REC)
    font = pygame.font.SysFont("impact", 70)  # Заводим шрифт
    font_score = pygame.font.SysFont('impact', 42)
    font_delta = pygame.font.SysFont('impact', 24)
    text_score = font_score.render("Score: ", True, COLOR_TEXT)
    text_score_value = font_score.render(f"{score}", True, COLOR_TEXT)
    screen.blit(text_score, (20, 35))  # При помощи метода blit прикрепляем текст рекорда к экрану
    screen.blit(text_score_value, (150, 35))
    if delta > 0:
        text_delta = font_delta.render(f"+{delta}", True, COLOR_TEXT)
        screen.blit(text_delta, (205, 80))
    pretty_print(mas)
    draw_top_gamers()
    for row in range(BLOCKS):
        for column in range(BLOCKS):
            value = mas[row][column]  # Значение, которое хранится в массиве
            text = font.render(f'{value}', True,
                               BLACK)  # [0] - Текст, который будет отображаться [1] - обтекание текста [2] - цвет
            w = column * BLOCK_SIZE + (column + 1) * MARGIN
            h = row * BLOCK_SIZE + (row + 1) * MARGIN + BLOCK_SIZE
            pygame.draw.rect(screen, COLORS[value], (w, h, BLOCK_SIZE, BLOCK_SIZE))
            if value != 0:
                font_w, font_h = text.get_size()  # get_size Возвращает две координаты: ширину и высоту
                text_x = w + (BLOCK_SIZE - font_w) / 2
                text_y = h + (BLOCK_SIZE - font_h) / 2
                screen.blit(text, (text_x, text_y))



COLOR_TEXT = (255, 127, 0)
COLORS = {
    0: (130, 130, 130),
    2: (0, 255, 0),
    4: (0, 210, 0),
    8: (130, 170, 0),
    16: (255, 170, 0),
    32: (255, 255, 35),
    64: (255, 255, 100),
    128: (185, 255, 100),
    256: (185, 255, 15),
    512: (185, 110, 15),
    1024: (185, 55, 15),
    2048: (255, 0, 0),
    4096: (70, 210, 170),
    8192: (70, 115, 170),
    16384: (70, 0, 170),
    32768: (140, 0, 170),
    65536: (130, 0, 90),
}

WHITE = (255, 255, 255)
GRAY = (130, 130, 130)
BLACK = (0, 0, 0)
GREEN = (54, 240, 22)
RED = (255, 0, 0)
BLOCKS = 4
BLOCK_SIZE = 110
MARGIN = 10
WIDTH = BLOCKS * BLOCK_SIZE + (BLOCKS + 1) * MARGIN
HEIGTH = WIDTH + 110
TITLE_REC = pygame.Rect(0, 0, WIDTH, 110)


def init_const():
    global score, mas
    mas = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    empty = get_empty_list(mas)  # Отсюда и по ___ код рандомной генерации цифр в начале игры
    random.shuffle(empty)
    random_num1 = empty.pop()
    random_num2 = empty.pop()
    x1, y1 = get_index_from_number(random_num1)
    mas = insert_2_or_4(mas, x1, y1)
    x2, y2 = get_index_from_number(random_num2)
    mas = insert_2_or_4(mas, x2, y2)  # ___
    score = 0


mas = None
score = None
USER_NAME = None
path = os.getcwd()
if 'data.txt' in os.listdir():
    with open('data.txt') as file:
        data = json.load(file)
        mas = data['mas']
        score = data['score']
        USER_NAME = data['user']
    full_path = os.path.join(path, 'data.txt')
    os.remove(full_path)
else:
    init_const()



print(get_empty_list(mas))
pretty_print(mas)

# for gamer in get_best():
#    print(gamer)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("2048")


def draw_intro():
    img2048 = pygame.image.load('og_image.png')
    font = pygame.font.SysFont("impact", 55)  # Заводим шрифт
    desc_font = pygame.font.SysFont("impact", 48)  # Шрифт для ограничения количества букв никнэйма
    text_welcome = font.render("Welcome!", True, WHITE)
    name = 'Enter your name'
    description = 'No more than 10 letters!'
    is_find_name = False
    while not is_find_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():  # Если является буквой
                    if name == "Enter your name":  # Эти if/else отвечают за корректный ввод имени
                        name = event.unicode
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:  # Удаление символов
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(name) > 1 and len(name) < 10:
                        global USER_NAME
                        USER_NAME = name
                        is_find_name = True
                        break

        screen.fill(BLACK)  # Заливаем весь экран чёрным цветом
        text_name = font.render(name, True, WHITE)
        rec_name = text_name.get_rect()
        rec_name.center = screen.get_rect().center  # Центрируем текст

        text_desc = desc_font.render(description, True, RED)

        screen.blit(pygame.transform.scale(img2048, [200, 200]), [10, 10])
        screen.blit(text_welcome, (230, 80))
        screen.blit(text_name, rec_name)
        screen.blit(text_desc, (15, 350))
        pygame.display.update()
    screen.fill(BLACK)


def draw_game_over():
    global USER_NAME, mas, GAMERS_DB
    img2048 = pygame.image.load('og_image.png')
    font = pygame.font.SysFont("impact", 55)  # Заводим шрифт
    text_game_over = font.render("GAME OVER!", True, WHITE)
    text_score = font.render(f"You received: {score}", True, WHITE)
    best_score = GAMERS_DB[0][1]
    if score > best_score:
        text = "New Best Score!"
    else:
        text = f"Best score: {best_score}"
    text_record = font.render(text, True, GREEN)
    insert_result(USER_NAME, score)
    GAMERS_DB = get_best()
    make_decision = False
    while not make_decision:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # restart game with name
                    make_decision = True
                    init_const()
                elif event.key == pygame.K_RETURN:
                    # restart game without name
                    USER_NAME = None
                    make_decision = True
                    init_const()
        screen.fill(BLACK)
        screen.blit(text_game_over, (220, 80))
        screen.blit(text_score, (30, 350))
        screen.blit(text_record, (30, 250))
        screen.blit(pygame.transform.scale(img2048, [200, 200]), [10, 10])
        pygame.display.update()
    screen.fill(BLACK)

def save_game():
    data = {
        'user': USER_NAME,
        'score': score,
        'mas': mas
    }
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)  # Указываем какой объект сохраняем и куда сохраняем


def game_loop():
    global score, mas
    draw_interfase(score)
    pygame.display.update()  # обновление "экрана"
    is_mas_move = False
    while is_zero_in_mas(mas) or can_move(mas):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game()
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                delta = 0
                if event.key == pygame.K_LEFT:  # Если нажимаем на "ЛЕВО"
                    mas, delta, is_mas_move = move_left(mas)
                elif event.key == pygame.K_RIGHT:  # Если нажимаем на "ПРАВО"
                    mas, delta, is_mas_move = move_right(mas)
                elif event.key == pygame.K_UP:
                    mas, delta, is_mas_move = move_up(mas)
                elif event.key == pygame.K_DOWN:
                    mas, delta, is_mas_move = move_down(mas)
                score += delta

                if is_zero_in_mas(mas) and is_mas_move:
                    empty = get_empty_list(mas)
                    random.shuffle(empty)
                    random_num = empty.pop()
                    x, y = get_index_from_number(random_num)
                    mas = insert_2_or_4(mas, x, y)
                    print(f'Мы заполнили элемент под номером {random_num}')
                    is_mas_move = False

                draw_interfase(score, delta)
                pygame.display.update()

        print(USER_NAME)


while True:
    if USER_NAME is None:
        draw_intro()
    game_loop()
    draw_game_over()
