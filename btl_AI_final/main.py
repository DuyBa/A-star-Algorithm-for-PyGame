import pygame
import math
from queue import PriorityQueue
import button

pygame.init()

WIDTH = 800
WIN = pygame.display.set_mode((1100, 800))
pygame.display.set_caption("A* Path Finding Algorithm")

status = 'menu'

# load button images
menu = pygame.image.load('picture/menu.jpg').convert_alpha()
huongdan = pygame.image.load('picture/huongdan.png').convert_alpha()
about_img = pygame.image.load('picture/about_btn.png').convert_alpha()
exit_img = pygame.image.load('picture/exit_btn.png').convert_alpha()
menu_img = pygame.image.load('picture/menu_btn.png').convert_alpha()
hard_img = pygame.image.load('picture/hard.png').convert_alpha()
easy_img = pygame.image.load('picture/easy.png').convert_alpha()
kho_img = pygame.image.load('picture/kho.png').convert_alpha()
de_img = pygame.image.load('picture/de.png').convert_alpha()

matbien = pygame.image.load('picture/matbien.jpg').convert_alpha()
cuuho = pygame.image.load("picture/cuuho.png").convert_alpha()
nannhan = pygame.image.load("picture/nannhan.png").convert_alpha()
sanho = pygame.image.load("picture/sanho.png").convert_alpha()
thu = pygame.image.load("picture/thu.png").convert_alpha()
ket = pygame.image.load("picture/ket.png").convert_alpha()
trong = pygame.image.load("picture/trong.png").convert_alpha()
trung = pygame.image.load("picture/trung.png").convert_alpha()
cat = pygame.image.load("picture/cat.png").convert_alpha()

do = pygame.image.load("picture/do.png").convert_alpha()
vang = pygame.image.load("picture/vang.png").convert_alpha()

# create button instances
about_button = button.Button(440, 400, about_img, 0.2)
exit_button = button.Button(450, 500, exit_img, 0.2)
menu_button = button.Button(850, 600, menu_img, 0.2)
hard_button = button.Button(440, 200, hard_img, 0.2)
easy_button = button.Button(440, 300, easy_img, 0.2)
kho_button = button.Button(440, 490, kho_img, 0.2)
de_button = button.Button(440, 590, de_img, 0.2)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = trong
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == do

    def is_open(self):
        return self.color == vang

    def is_barrier(self):
        return self.color == sanho

    def is_start(self):
        return self.color == cuuho

    def is_end(self):
        return self.color == nannhan

    def is_try(self):
        return self.color == thu

    def is_path(self):
        self.color == ket

    def reset(self):
        self.color = trong

    def make_start(self):
        self.color = cuuho

    def make_barrier(self):
        self.color = sanho

    def make_end(self):
        self.color = nannhan

    def make_path(self):
        self.color = ket

    def make_try(self):
        self.color = thu

    def make_trung(self):
        self.color = trung

    def make_closed(self):
        self.color = do

    def make_open(self):
        self.color = vang

    def draw(self, win):
        win.blit(self.color, (self.x, self.y))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        if not current.is_start():
            current.make_path()

        draw()


def algorithm(draw, grid, start, end, path):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return came_from

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if not neighbor.is_end() and len(path)==0:
                        neighbor.make_open()

        draw()
        if current != start and len(path)==0:
            current.make_closed()

    return 0

def algorithm0(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            return f_score[end]

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

        draw()

    return 0


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    WIN.blit(matbien, (0, 0))
    for row in grid:
        for spot in row:
            if spot.color != trong:
                spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    WIN.blit(img, (x, y))


def main(win, width, status):
    ROWS = 25
    grid = make_grid(ROWS, width)
    start = None
    end = None
    path = []
    path_end = {}
    font = pygame.font.SysFont("Times New Roman", 20)
    font_muc = pygame.font.SysFont("Times New Roman", 30)
    font_win = pygame.font.SysFont("Times New Roman",60)
    font_over = pygame.font.SysFont("Times New Roman", 40)
    TEXT_COL = RED
    goal = 0
    mucdo = ''

    run = True
    while run:
        if status == "menu":
            WIN.blit(menu, (0, 0))

            if about_button.draw(WIN):
                status = 'huongdan'

            if hard_button.draw(WIN):
                status = 'play'
                mucdo = 'hard'

            if easy_button.draw(WIN):
                status = 'play'
                mucdo = 'easy'

            if exit_button.draw(WIN):
                run = False
        else:
            if status == 'huongdan':
                WIN.blit(huongdan, (0, 0))

                if kho_button.draw(WIN) and status == 'huongdan':
                    status = 'play'
                    mucdo = 'hard'
                if de_button.draw(WIN) and status == 'huongdan':
                    status = 'play'
                    mucdo = 'easy'

        if status == 'play' :
            draw(win, grid, ROWS, width)
            WIN.blit(cat, (800, 0))

            if mucdo == 'hard':draw_text("Hard", font_muc, TEXT_COL, 910, 100)
            if mucdo == 'easy':draw_text("Easy", font_muc, TEXT_COL, 910, 100)
            if start and end and mucdo == 'hard':

                if abs(len(path) - goal) == 0 and goal != 0 and not end in start.neighbors:
                    draw_text("Gameover", font_over, TEXT_COL, 880, 300)

                elif end in start.neighbors:
                    draw_text("Win", font_win, TEXT_COL, 900, 300)
                else:
                    draw_text("Duong di cua ban: " + str(len(path)), font, TEXT_COL, 810, 250)
                    draw_text("Duong di A*: " + str(goal), font, TEXT_COL, 810, 300)
                    draw_text("Duong di chenh lech: " + str(abs(len(path) - goal)), font, TEXT_COL, 810, 350)




            if start and end and mucdo == 'easy':
                if goal == 0 and len(path) != 0 and not end in start.neighbors:
                    draw_text("Khong co duong di", font, TEXT_COL, 880, 300)

                elif end in start.neighbors:
                    draw_text("Win", font_win, TEXT_COL, 900, 300)
                else:
                    draw_text("Duong di cua ban: " + str(len(path)), font, TEXT_COL, 810, 250)
                    draw_text("Duong di A*: " + str(goal), font, TEXT_COL, 810, 300)
                    draw_text("Duong di chenh lech: " + str(abs(len(path) - goal)), font, TEXT_COL, 810, 350)

            if menu_button.draw(WIN):
                status = 'menu'
                path = []
                path_end = {}
                goal = 0
                start = None
                end = None
                grid = make_grid(ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if status == 'menu' or status == 'huongdan': continue

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)

                if row > 24 or col > 24:
                    continue
                else:
                    spot = grid[row][col]

                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()





            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)

                if row > 24 or col > 24:
                    continue
                else:
                    spot = grid[row][col]

                if spot.is_try():continue
                elif spot == start and len(path)>0:continue
                else:spot.reset()

                if spot == start :
                    start = None
                elif spot == end:
                    end = None



            if event.type == pygame.KEYDOWN:
                if start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    if len(path) == 0:
                        goal = algorithm0(lambda: draw(win, grid, ROWS, width), grid, start, end)


                    if event.key == pygame.K_SPACE:
                        if len(path_end)>0:
                            for i in path_end:
                                if i.color==ket:
                                    i.reset()
                        path_end = {}
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        path_end = algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end, path)

                    if goal - len(path) == 0 and mucdo == 'hard':
                        pass

                    else:
                        if event.key == pygame.K_d:
                            right = grid[start.row + 1][start.col]
                            if len(path) > 0 and path[-1].row == right.row and path[-1].col == right.col:
                                path.remove(right)
                                start.reset();
                                start = right;
                                start.make_start();

                            elif right.color == trong:
                                start.make_try();
                                path.append(start);
                                start = right;
                                start.make_start();
                            elif right.color == ket:
                                start.make_try();
                                path.append(start);
                                start = right;
                                start.make_start();

                        if event.key == pygame.K_s:
                            bottom = grid[start.row][start.col + 1]
                            if len(path) > 0 and path[-1].row == bottom.row and path[-1].col == bottom.col:
                                path.remove(bottom)
                                start.reset();
                                start = bottom;
                                start.make_start();
                            elif bottom.color == trong:
                                start.make_try();
                                path.append(start);
                                start = bottom;
                                start.make_start();
                            elif bottom.color == ket:
                                start.make_try();
                                path.append(start);
                                start = bottom;
                                start.make_start();
                        if event.key == pygame.K_w:
                            above = grid[start.row][start.col - 1]
                            if len(path) > 0 and path[-1].row == above.row and path[-1].col == above.col:
                                path.remove(above)

                                start.reset();
                                start = above;
                                start.make_start();
                            elif above.color == trong:
                                start.make_try();
                                path.append(start);
                                start = above;
                                start.make_start();
                            elif above.color == ket:
                                start.make_try();
                                path.append(start);
                                start = above;
                                start.make_start();
                        if event.key == pygame.K_a:
                            left = grid[start.row - 1][start.col]
                            if len(path) > 0 and path[-1].row == left.row and path[-1].col == left.col:
                                path.remove(left)
                                start.reset();
                                start = left;
                                start.make_start();
                            elif left.color == trong:
                                start.make_try();
                                path.append(start);
                                start = left;
                                start.make_start()
                            elif left.color == ket:
                                start.make_try();
                                path.append(start);
                                start = left;
                                start.make_start();

                if event.key == pygame.K_c:
                    path=[]
                    path_end={}
                    goal = 0
                    status = 'play'
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)



        pygame.display.update()

    pygame.quit()


main(WIN, WIDTH, status)
