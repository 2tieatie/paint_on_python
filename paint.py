import pygame, sys
import numpy as np
pygame.init()
sc = pygame.display.set_mode((1280, 720))
draw = False
size = 4
rects = {(size, (0, 0, 0)): set()}
eraser = False
font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()
r_s = 5
c = (0, 0, 0)
x = 17
n_1 = np.array(range(-size, size))

def colors():
    global c, size, x
    mouse_pos = pygame.mouse.get_pos()
    m_x = mouse_pos[0]
    m_y = mouse_pos[1]
    click = pygame.mouse.get_pressed()
    for i in range(0, 255):
        pygame.draw.rect(sc, (i, 0, 0), (22 + i, 515, 1, 40))
        pygame.draw.rect(sc, (0, i, 0), (22 + i, 555, 1, 40))
        pygame.draw.rect(sc, (0, 0, i), (22 + i, 595, 1, 40))
        pygame.draw.rect(sc, (i, i, i), (22 + i, 635, 1, 40))
    if m_y > 515 and m_y < 555:
        if m_x > 22 and m_x < 277:
            if click[0] == 1:
                c = (m_x - 22, 0, 0)
    elif m_y > 555 and m_y < 595:
        if m_x > 22 and m_x < 277:
            if click[0] == 1:
                c = (0, m_x - 22, 0)
    elif m_y > 595 and m_y < 635:
        if m_x > 22 and m_x < 277:
            if click[0] == 1:
                c = (0, 0, m_x - 22)
    elif m_y > 635 and m_y < 675:
        if m_x > 22 and m_x < 277:
            if click[0] == 1:
                c = (m_x - 22, m_x - 22, m_x - 22)
    pygame.draw.line(sc, (0, 0, 0), (22, 450), (272, 450), 3)
    pygame.draw.rect(sc, (75, 75, 75), (x, 430, 10, 40))
    if m_y > 430 and m_y < 470:
        if m_x > 17 and m_x < 272:
            if click[0] == 1:
                size = (m_x - 17)//25
                x = 17 + size * 25

def buttons(x, y, text, file, func1):
    global draw, eraser
    font = pygame.font.SysFont(None, 30)
    image = pygame.image.load(file).convert_alpha()
    sc.blit(image, (x,y))
    mouse_pos = pygame.mouse.get_pos()
    m_x = mouse_pos[0]
    m_y = mouse_pos[1]
    if m_x > x and m_x < (x+50) and m_y > y and m_y < (y+50):
        click = pygame.mouse.get_pressed()
        if click[0] == 1:
            if func1 == eraser:
                eraser, draw = True, False
            elif func1 == draw:
                eraser, draw = False, True
            pygame.draw.rect(sc, (255, 255, 255), (x, y, 50, 50))
        symb = font.render(text, True, (255, 255, 255), (75, 75, 75))
        sc.blit(symb, (m_x, m_y - 15))

def bin(x, y):
    global rects
    font = pygame.font.SysFont(None, 30)
    image = pygame.image.load('bin.png').convert_alpha()
    sc.blit(image, (x, y))
    mouse_pos = pygame.mouse.get_pos()
    m_x = mouse_pos[0]
    m_y = mouse_pos[1]
    click = pygame.mouse.get_pressed()
    if m_x > x and m_x < (x + 50) and m_y > y and m_y < (y + 50):
        if click[0] == 1:
            for key in rects.keys():
                rects[key] = set()
            pygame.draw.rect(sc, (255, 255, 255), (x, y, 50, 50))
        symb = font.render('Очистить (R)', True, (255, 255, 255), (75, 75, 75))
        sc.blit(symb, (m_x, m_y - 15))

def detect():
    global rects, types, types_list, sets, tup
    mouse_pos = pygame.mouse.get_pos()
    m_x = mouse_pos[0]
    m_y = mouse_pos[1]
    koef = size * r_s
    if m_x > 300 and m_x < 1235 and m_y > 45 and m_y < 675:
        r_x = m_x // r_s * r_s
        r_y = m_y // r_s * r_s
        if draw and eraser is not True:
            if rects.get((size, c)) is not None:
                for i in n_1:
                    for i1 in n_1:
                        rects[(size, c)].add((r_x + i * r_s, r_y + i1 * r_s))
            else: rects[(size, c)] = {(-100, 0)}
        pygame.draw.rect(sc, (0, 0, 0), (r_x - koef, r_y - koef, koef * 2, koef * 2), 1)

def drawing():
    n_a = np.array(list(rects.keys()))
    for key in n_a:
        n = np.asarray(list(rects[tuple(key)]))
        for coords in n:
            pygame.draw.rect(sc, key[1], (coords[0], coords[1], r_s, r_s))


def eras():
    global rects
    click = pygame.mouse.get_pressed()
    if click[0] == 1:
        mouse_pos = pygame.mouse.get_pos()
        m_x = mouse_pos[0]
        m_y = mouse_pos[1]
        for key in rects.keys():
            for i in n_1:
                dx = (m_x // r_s) + i
                for i1 in n_1:
                    dy = (m_y//r_s)+i1
                    if (dx*r_s, dy*r_s) in rects[key]:
                        rects[key].remove((dx*r_s, dy*r_s))
                    else: continue


def events():
    global draw, eraser, rects, scale
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if eraser == False:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                draw = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            draw = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                eraser = True
            elif event.key == pygame.K_b:
                eraser = False
            elif event.key == pygame.K_r:
                for key in rects.keys():
                    rects[key] = set()

while True:
    sc.fill((255, 255, 255))
    events()
    drawing()
    buttons(50, 45, 'Ластик (E)', 'eraser.png', eraser)
    buttons(50, 145, 'Кисть (B)', 'brush.jpg', draw)
    bin(50, 245)
    if eraser:
        eras()
    # sc.blit(symb, (640, 0))
    pygame.draw.rect(sc, (0, 0, 0), (300, 45, 935, 630), 2)
    colors()
    detect()
    clock.tick()
    pygame.display.set_caption(f'{clock.get_fps()}')
    pygame.display.flip()

