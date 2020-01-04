# dark blue for end nodes
# light blue for path
# dark green for currently searched nodes
# light green for already searched nodes
# white for empty
import pygame, math
pygame.init()
display = pygame.display.set_mode((500, 400), 0, 32)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

display.fill(WHITE)
pygame.draw.rect(display, BLUE, (10, 10, 10, 10))
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

start_point = [1, 1]
end_point = [50, 50]
rows = 40
cols = 40

class Node:
    def __init__(self, grid, x, y, dist_from_start):
        self.x = x
        self.y = y
        self.grid = grid
        self.g = dist_from_start

    def get_neighbors():
        # Collection of arrays representing the x and y displacement
        directions = [[1, 0], [1, 1], [0, 1], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        neighbors = []
        for direction in directions:
            neighbor_x = self.x + direction[0]
            neighbor_y = self.y + direction[1]
            if neighbor_x > 0 && neighbor_y > 0 && neighbor_x <= cols && neighbor_y <= rows:
                dist_from_neighbor = math.sqrt(math.pow(neighbor_x - x, 2) + math.pow(neighbor_y - y, 2))
                neighbors.append(Node(self.grid, neighbor_x, neighbor_y, self.g + dist_from_neighbor))

# Measures distance from node to endpoint with nodes only being able to travel vertically, horizontally, or diagonally
def h(node, end):
    x_dist = abs(end.x - node.x)
    y_dist = abs(end.y - node.y)
    diagonal_steps = min(x_dist, y_dist)
    straight_steps = y_dist + x_dist - 2 * diagonal_steps
    return diagonal_steps * math.sqrt(2) + straight_steps


def a_star(start, end):
