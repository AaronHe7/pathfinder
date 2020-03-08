# dark blue for end nodes
# light blue for path
# dark green for currently searched nodes
# light green for already searched nodes
# white for empty
import pygame, math, sys
from a_star import *

pygame.init()
pygame.font.init()

HEIGHT = 600
WIDTH = 600

display = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHT_BLUE = (135, 206, 250)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

font = pygame.font.SysFont('Arial', 10)
text1 = font.render('Start/End Node (Right Click)', False, BLACK)
text2 = font.render('Wall Node (Left Click)', False, BLACK)
text3 = font.render('Start', False, WHITE)
text4 = font.render('Clear', False, WHITE)

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Pathfinder')

def update_display():
    display.fill(WHITE)

    pygame.draw.rect(display, BLUE, (10, 5, 10, 10))
    pygame.draw.rect(display, BLACK, (200, 5, 10, 10))
    display.blit(text1, (25, 5))
    display.blit(text2, (215, 5))

    # Buttons
    pygame.draw.rect(display, BLACK, (355, 8, 40, 10))
    pygame.draw.rect(display, BLACK, (445, 8, 40, 10))

    display.blit(text3, (360, 6))
    display.blit(text4, (450, 6))

rows = 40
cols = 40
grid = []
start = None
end = None

def reset_grid():
    global grid, start, end
    grid = []
    start, end = None, None
    for i in range(rows):
        row_nodes = []
        for j in range(cols):
            node = Node(grid, j, i)
            row_nodes.append(node)
        grid.append(row_nodes)
    update_grid(display, grid)

def update_grid(display, grid):
    update_display()
    rect_width = (WIDTH - 1)/cols
    rect_height = (HEIGHT - 21)/cols

    for i in range(rows):
        for j in range(cols):
            color = None
            node = grid[i][j]
            if node.type == 'wall':
                color = BLACK
            elif node == start or node == end:
                color = BLUE
            elif node.type == 'path':
                color = LIGHT_BLUE

            if color:
                pygame.draw.rect(display, color, (j * rect_width + 1, i * rect_height + 21, rect_width, rect_height))
                
    for i in range(len(grid) + 1):
        pygame.draw.rect(display, GRAY, (i * rect_width, 20, 1, HEIGHT))
        pygame.draw.rect(display, GRAY, (0, i * rect_height + 20, WIDTH, 1))

    pygame.display.update()
reset_grid()
update_grid(display, grid)

def draw_tile(x, y, tile_type):
    global start, end
    clear_path_nodes()
    
    row = ((y - 20) * rows)//(HEIGHT - 20)
    col = (x * cols)//WIDTH
    node = grid[row][col]

    if row < 0 or col < 0 or row >= rows or col >= cols or node.type == 'wall' or node == start or node == end:
        return

    if tile_type == 'wall':
        grid[row][col].type = 'wall'
    elif tile_type == 'endpoint':
        if not start:
            start = node
        elif not end:
            end = node
    update_grid(display, grid)

def pathfind():
    if not start or not end:
        print('Please mark both endpoint nodes.')
        return
    path = a_star(grid, start, end)
    if not path:
        print('No possible paths.')
        return
    for node in path:
        if node != start and node != end:
            node.type = 'path'
    update_grid(display, grid)

def clear_path_nodes():
    for i in range(rows):
        for j in range(cols):
            node = grid[i][j]
            if node.type == 'path':
                node.type = 'road'
            

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Test for click on start and clear button
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            x = mouse_pos[0]
            y = mouse_pos[1]
            # Start button
            if x >= 355 and x <= 395 and y >= 8 and y <= 18:
                pathfind()
            # Clear button
            elif x >= 445 and x <= 485 and y >= 8 and y <= 18:
                reset_grid()

        # Right click adds start/end node
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouse_pos = pygame.mouse.get_pos()
            x = mouse_pos[0]
            y = mouse_pos[1]
            draw_tile(x, y, 'endpoint')

        # Left click adds wall node
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            x = mouse_pos[0]
            y = mouse_pos[1]
            draw_tile(x, y, 'wall')
