# dark blue for end nodes
# light blue for path
# dark green for currently searched nodes
# light green for already searched nodes
# white for empty
import pygame, math, sys
from a_star import Node, a_star

pygame.init()
pygame.font.init()

HEIGHT = 600
WIDTH = 600
display = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

font = pygame.font.SysFont('Arial', 10)
text1 = font.render('Start/End Node (Right Click)', False, BLACK)
text2 = font.render('Wall Node (Left Click)', False, BLACK)
text3 = font.render('Press Space to Start', False, BLACK)
text4 = font.render('Press \'c\' to Clear', False, BLACK)


display.fill(WHITE)
pygame.display.set_caption('Pathfinder')
pygame.draw.rect(display, BLUE, (10, 5, 10, 10))
pygame.draw.rect(display, BLACK, (200, 5, 10, 10))
display.blit(text1, (30, 5))
display.blit(text2, (220, 5))
display.blit(text3, (360, 5))
display.blit(text4, (500, 5))

rows = 40
cols = 40
grid = []
start = None
end = None

for i in range(rows):
    row_nodes = []
    for j in range(cols):
        node = Node(grid, j, i)
        row_nodes.append(node)
    grid.append(row_nodes)
    
def update_grid(display, grid):
    rect_width = (WIDTH - 1)/cols
    rect_height = (HEIGHT - 21)/cols
    for i in range(len(grid) + 1):
        pygame.draw.rect(display, BLACK, (i * rect_width, 20, 1, HEIGHT))
        pygame.draw.rect(display, BLACK, (0, i * rect_height + 20, WIDTH, 1))

    for i in range(rows):
        for j in range(cols):
            color = None
            if grid[i][j].type == 'wall':
                color = BLACK
            elif grid[i][j] == start or grid[i][j] == end:
                color = BLUE
            if color:
                pygame.draw.rect(display, color, (j * rect_width + 1, i * rect_height + 21, rect_width, rect_height))

    pygame.display.update()
update_grid(display, grid)

def draw_tile(x, y, tile_type):
    global start, end
    
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
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Right click adds start/end node
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
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

