from generator import *
class Food:
    def __init__(self): #инициализация пиваа
        self.img = pygame.image.load('food.png').convert_alpha() #переводим в пиксели
        self.img = pygame.transform.scale(self.img, (TILE - 10, TILE - 10)) #масштабируем
        self.rect = self.img.get_rect() #делаем квадрат
        self.set_pos() #задаем позиции

    def set_pos(self):
        self.rect.topleft = randrange(cols) * TILE + 5, randrange(rows) * TILE + 5

    def draw(self):
        game_surface.blit(self.img, self.rect)


def is_collide(x, y): #столкновения
    tmp_rect = player_rect.move(x, y)
    if tmp_rect.collidelist(walls_collide_list) == -1:
        return False
    return True


def eat_food(): #функция настижения цели
    for food in food_list:
        if player_rect.collidepoint(food.rect.center):
            food.set_pos()
            return True
    return False


def is_game_over():
    global time, score, record, FPS
    if time < 0:
        pygame.time.wait(700)
        player_rect.center = TILE // 2, TILE // 2
        [food.set_pos() for food in food_list]
        set_record(record, score)
        record = get_record()
        time, score, FPS = 60, 0, 60


def get_record(): #создаем запись очков
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')
            return 0


def set_record(record, score): #записываем очки
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


FPS = 60
pygame.init()
game_surface = pygame.Surface(RES)
surface = pygame.display.set_mode((WIDTH + 300, HEIGHT))
clock = pygame.time.Clock()

#загружаем картинки
bg_game = pygame.image.load('bg-1.jpg').convert()
bg = pygame.image.load('bg-main.png').convert()

#создаем лабиринт
maze = generate_maze()

#настройки дэнчика
player_speed = 5
player_img = pygame.image.load('0.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
player_rect = player_img.get_rect()
player_rect.center = TILE // 2, TILE // 2
directions = {'a': (-player_speed, 0), 'd': (player_speed, 0), 'w': (0, -player_speed), 's': (0, player_speed)}
keys = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
direction = (0, 0)

food_list = [Food() for i in range(3)]

# столкновения
walls_collide_list = sum([cell.get_rects() for cell in maze], [])

pygame.time.set_timer(pygame.USEREVENT, 1000)
time = 60
score = 0
record = get_record()

font = pygame.font.SysFont('Helvetica', 90)
text_font = pygame.font.SysFont('Helvetica', 50)

while True:
    surface.blit(bg, (WIDTH, 0))
    surface.blit(game_surface, (0, 0))
    game_surface.blit(bg_game, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.USEREVENT:
            time -= 1

    # движение
    pressed_key = pygame.key.get_pressed()
    for key, key_value in keys.items():
        if pressed_key[key_value] and not is_collide(*directions[key]):
            direction = directions[key]
            break
    if not is_collide(*direction):
        player_rect.move_ip(direction)

    #рисуем лабиринт
    [cell.draw(game_surface) for cell in maze]

    # игра
    if eat_food():
        FPS += 10
        score += 1
    is_game_over()

    #рисуем дэнчика
    game_surface.blit(player_img, player_rect)

    #рисуем пивасик
    [food.draw() for food in food_list]

    #рисуем таблички
    surface.blit(text_font.render('TIME', True, pygame.Color('red'), True), (WIDTH + 70, 30))
    surface.blit(font.render(f'{time}', True, pygame.Color('red')), (WIDTH + 70, 100))
    surface.blit(text_font.render('score:', True, pygame.Color('mediumvioletred'), True), (WIDTH + 60, 250))
    surface.blit(font.render(f'{score}', True, pygame.Color('mediumvioletred')), (WIDTH + 90, 300))
    surface.blit(text_font.render('record:', True, pygame.Color('gold'), True), (WIDTH + 50, 450))
    surface.blit(font.render(f'{record}', True, pygame.Color('gold')), (WIDTH + 70, 500))

    #рисуем счетчик
    pygame.display.flip()
    clock.tick(FPS)