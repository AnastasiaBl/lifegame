
import os.path
from enum import Enum

from model import Model

import random
import pygame
from pygame.locals import *
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename

class State(Enum):
    Creating = 0,
    Setting = 1,
    Playing = 2,
    GameOver = 3


# Переменные и константы
start_time = 0
screen_size = Rect(0, 0, 1024, 850)
field_size = (18, 15)
cell_size = (32, 32)
field = [[]]

model = 0

folder_path = os.path.split(os.path.abspath(__file__))[0]
app = 0

def open_sprite(path):
    """Открыть картинку из файла"""
    path=os.path.join(folder_path,'data',path)
    try:
        texture=pygame.image.load(path)
    except pygame.error:
        raise SystemExit('Ошибка при загрузке картинки %s' % (path))
    return texture.convert_alpha()


class Cell(pygame.sprite.Sprite):
    def __init__(self, image, image_on):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = image
        self.image_off = image
        self.image_on = image_on
        self.on = False
        self.rect = self.image.get_rect()

    def set_enabled(self, on):
        self.on = on

        if on:
            self.image = self.image_on
        else:
            self.image = self.image_off

    def update(self):
        pass


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos


class Text(pygame.sprite.Sprite):
    def __init__(self, msg):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.font = pygame.font.Font(None, 65)
        self.color = Color('black')
        self.set_text(msg)
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_size.centerx
        self.rect.centery = screen_size.centery

    def set_text(self, msg):
        self.image = self.font.render(msg, 0, self.color)


def main(winstyle=0):
    global field_size
    global field_history

    pygame.init()
    
    screen = pygame.display.set_mode(screen_size.size)
    screen.fill(pygame.Color(255,255,255))
    pygame.display.init()

    # Загружаем все спрайты
    cell_off = open_sprite('cell1.png')
    cell_on = open_sprite('cell2.png')

    cell_off = pygame.transform.scale(cell_off, cell_size)
    cell_on = pygame.transform.scale(cell_on, cell_size)

    bar = open_sprite('bar.png')
    handle = open_sprite('handle.png')

    icon_step = pygame.transform.scale(open_sprite('step.png'), cell_size)
    icon_play = pygame.transform.scale(open_sprite('run.png'), cell_size)
    icon_new = pygame.transform.scale(open_sprite('new.png'), cell_size)
    icon_stop = pygame.transform.scale(open_sprite('stop.png'), cell_size)
    icon_load = pygame.transform.scale(open_sprite('load.png'), cell_size)
    icon_save = pygame.transform.scale(open_sprite('save.png'), cell_size)

    # Задаём параметры окна
    icon = pygame.transform.scale(cell_off, (32, 32))
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Life game')

    # Загружаем фон
    bg = pygame.Surface(screen_size.size)
    bg.fill((255,255,255))
    screen.fill([255,255,255])
    pygame.display.flip()

    all = pygame.sprite.RenderUpdates()

    Cell.containers = all
    Button.containers = all
    Text.containers = all

    timer_started = 0

    state = State.Creating

    global clock
    clock = pygame.time.Clock()

    bar_width = Button(bar, screen_size.center)
    bar_width.rect.centery += 50
    bar_height = Button(bar, screen_size.center)
    handle_width = Button(handle, screen_size.center)
    handle_width.rect.centery += 50
    handle_height = Button(handle, screen_size.center)
    start_button = Button(icon_play, screen_size.center)
    start_button.rect.centery += 100
    text_size = Text("18x15")
    text_size.rect.centery -= 100

    button_load = Button(icon_load, (200, 25))

    text_over = None

    done = 0
    while not done:
        mouse_click = 0
        mouse_move = 0

        # Считываем что нажал пользователь
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                done = 1
                break
            elif e.type == MOUSEMOTION and e.buttons[0] == 1:
                mouse_move = list(e.pos)
            elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                mouse_click = list(e.pos)

        if mouse_move:
            if state == State.Creating:
                if bar_width.rect.collidepoint(mouse_move):
                    field_size = (int((mouse_move[0] - screen_size.centerx + 128) / 256 * 27 + 5), field_size[1])
                    handle_width.rect.centerx = mouse_move[0]
                elif bar_height.rect.collidepoint(mouse_move):
                    field_size = (field_size[0], int((mouse_move[0] - screen_size.centerx + 128) / 256 * 21 + 5))
                    handle_height.rect.centerx = mouse_move[0]
                text_size.set_text(str(field_size[0]) + "x" + str(field_size[1]))

        if mouse_click:
            if state == State.Creating:
                if start_button.rect.collidepoint(mouse_click):
                    # Переход на экран задания состояния
                    bar_width.kill()
                    bar_height.kill()
                    handle_width.kill()
                    handle_height.kill()
                    start_button.kill()
                    text_size.kill()

                    create_field(cell_on, cell_off)
                    button_new = Button(icon_new, (50, 25))
                    button_step = Button(icon_step, (100, 25))
                    button_play = Button(icon_play, (150, 25))
                    button_save = Button(icon_save, (250, 25))

                    state = State.Setting
                elif button_load.rect.collidepoint(mouse_click):
                    # Загрузка поля и переход на экран задания состояния
                    load_field(cell_on, cell_off)
                    
                    bar_width.kill()
                    bar_height.kill()
                    handle_width.kill()
                    handle_height.kill()
                    start_button.kill()
                    text_size.kill()

                    button_new = Button(icon_new, (50, 25))
                    button_step = Button(icon_step, (100, 25))
                    button_play = Button(icon_play, (150, 25))
                    button_save = Button(icon_save, (250, 25))

                    state = State.Setting

            elif state == State.Setting:
                if button_new.rect.collidepoint(mouse_click):
                    # Переход на экран создания поля
                    button_new.kill()
                    button_step.kill()
                    button_play.kill()
                    button_save.kill()
                    for y in range(field_size[1]):
                        for x in range(field_size[0]):
                            field[y][x].kill()

                    bar_width = Button(bar, screen_size.center)
                    bar_width.rect.centery += 50
                    bar_height = Button(bar, screen_size.center)
                    handle_width = Button(handle, screen_size.center)
                    handle_width.rect.centery += 50
                    handle_height = Button(handle, screen_size.center)
                    start_button = Button(icon_play, screen_size.center)
                    start_button.rect.centery += 100
                    text_size = Text("18x15")
                    field_size = (18, 15)
                    text_size.rect.centery -= 100

                    state = State.Creating
                elif button_step.rect.collidepoint(mouse_click):
                    step()
                elif button_play.rect.collidepoint(mouse_click):
                    # Убираем кнопки, начинаем автоматически делать шаги по таймеру
                    button_step.kill()
                    button_play.kill()
                    button_save.kill()

                    button_stop = Button(icon_stop, (150, 25))

                    state = State.Playing
                    model.clear_history() # очистить историю состояний

                    timer_started = pygame.time.get_ticks() - 400 # Заводим таймер для шагов

                elif button_load.rect.collidepoint(mouse_click):
                    load_field(cell_on, cell_off)
                elif button_save.rect.collidepoint(mouse_click):
                    save_field()
                else:
                    # Кликнули на поле
                    at_field = (mouse_click[0] - screen_size.width/2 + cell_size[0]*field_size[0]/2,
                        mouse_click[1] - screen_size.height/2 - 20 + cell_size[1]*field_size[1]/2)
                    x = int(at_field[0] // cell_size[0])
                    y = int(at_field[1] // cell_size[1])

                    if x>=0 and y>=0 and x<field_size[0] and y<field_size[1]:
                        field[y][x].set_enabled(not field[y][x].on)
                        model.field_values[y][x] = field[y][x].on
            elif state == State.Playing or state == State.GameOver:
                if button_new.rect.collidepoint(mouse_click):
                    # Переход на экран создания поля
                    button_new.kill()
                    button_stop.kill()
                    for y in range(field_size[1]):
                        for x in range(field_size[0]):
                            field[y][x].kill()

                    if text_over is not None: text_over.kill()

                    bar_width = Button(bar, screen_size.center)
                    bar_width.rect.centery += 50
                    bar_height = Button(bar, screen_size.center)
                    handle_width = Button(handle, screen_size.center)
                    handle_width.rect.centery += 50
                    handle_height = Button(handle, screen_size.center)
                    start_button = Button(icon_play, screen_size.center)
                    start_button.rect.centery += 100
                    text_size = Text("18x15")
                    field_size = (18, 15)
                    text_size.rect.centery -= 100

                    state = State.Creating
                elif button_load.rect.collidepoint(mouse_click):
                    load_field(cell_on, cell_off)

                    # Возвращаемся к заданию состояния
                    button_stop.kill()
                    button_step = Button(icon_step, (100, 25))
                    button_play = Button(icon_play, (150, 25))
                    button_save = Button(icon_save, (250, 25))

                    if text_over is not None: text_over.kill()

                    state = State.Setting
                elif button_stop.rect.collidepoint(mouse_click):
                    # Возвращаемся к заданию состояния
                    button_stop.kill()
                    button_step = Button(icon_step, (100, 25))
                    button_play = Button(icon_play, (150, 25))
                    button_save = Button(icon_save, (250, 25))

                    if text_over is not None: text_over.kill()

                    state = State.Setting

        if state == State.Playing and pygame.time.get_ticks() - timer_started > 400:
            # Делаем шаг по таймеру
            if step() == True:
                # Состояние повторилось, останавливаем игру
                state = State.GameOver

                text_over = Text("Состояние повторилось")
                text_over.rect.centery = 30
            else:
                if is_field_empty():
                    # Поле пустое, останавливаем игру
                    state = State.GameOver

                    text_over = Text("Поле пустое")
                    text_over.rect.centery = 30
                else:
                    timer_started = pygame.time.get_ticks()

        # Очищаем экран
        all.clear(screen, bg)
        all.update()

        # Рисуем всю сцену
        all.draw(screen)
        pygame.display.flip()

        clock.tick(40)

    pygame.quit()


def save_field():
    app = Tk()
    save_file = asksaveasfilename(parent=app, title='Save as')
    f = open(save_file, "w+")
    for y in range(field_size[1]):
        for x in range(field_size[0]):
            f.write("1" if field[y][x].on else "0")
        if y < field_size[1] - 1:
            f.write("\n")
    f.close()
    app.quit()

def is_field_empty():
    for y in range(field_size[1]):
        for x in range(field_size[0]):
            if field[y][x].on:
                return False

    return True


def load_field(cell_on, cell_off):
    global field_size

    app = Tk()
    save_file = askopenfilename(parent=app, title='Open')
    f = open(save_file, "r")

    field_values = []
    y = 0

    for line in f:
        line = line.strip()
        field_values.append([])
        x = 0
        for char in line:
            field_values[len(field_values)-1].append(char == "1")
            x += 1
        y += 1
        field_size = (x, y)

    create_field(cell_on, cell_off)

    for y in range(field_size[1]):
        for x in range(field_size[0]):
            field[y][x].set_enabled(field_values[y][x])

    model.field_values = field_values

    f.close()
    app.destroy()


def step():
    result = model.step()

    for y in range(field_size[1]):
        for x in range(field_size[0]):
            field[y][x].set_enabled(model.field_values[y][x])

    return result


def create_field(cell_on, cell_off):
    """Создать уровень"""
    global field
    global model

    for line in field:
        for cell in line:
            cell.kill()

    field = [[0] * field_size[0] for x in range(field_size[1])]
    model = Model(field_size[0], field_size[1])

    for y in range(field_size[1]):
        for x in range(field_size[0]):
            # создать карточку в координатах (x, y)
            field[y][x] = Cell(cell_off, cell_on)
            field[y][x].posy = y
            field[y][x].rect.centerx = screen_size.centerx + (x - (field_size[0] - 1) / 2) * cell_size[0]
            field[y][x].rect.centery = screen_size.centery + 20 + (y - (field_size[1] - 1) / 2) * cell_size[1]
            field[y][x].rect.size = cell_size



if __name__ == '__main__':
    main()
