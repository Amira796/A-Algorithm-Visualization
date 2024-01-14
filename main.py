from queue import PriorityQueue
import pygame

# Setting the screen window size and caption
WIDTH = 600
SCREEN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# Some Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 244, 208)


# Class for Nodes
class Node:

    def __init__(self, row, column, width, total_rows):
        self.row = row
        self.column = column
        self.x = row * width
        self.y = column * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.tot_rows = total_rows

    def get_position(self):  # return the position of the node
        return self.row, self.column

    def is_closed(self):  # If It's red? we already looked at it
        return self.color == RED

    def is_open(self):  # If it's green? you are in the open set
        return self.color == GREEN

    def is_barrier(self):  # If it's black? it's a barrier
        return self.color == BLACK

    def is_start(self):  # If it's yellow? it's the start
        return self.color == YELLOW

    def is_end(self):  # If it's Purple? it's the end
        return self.color == TURQUOISE

    def reset(self):  # Reset the node to the color white
        self.color = WHITE

    def set_closed(self):  # Set the node to be closed
        self.color = RED

    def set_opened(self):  # Set the node to be opened
        self.color = GREEN

    def set_barrier(self):  # Set the node to be a barrier
        self.color = BLACK

    def set_start(self):  # Set the node to be the start
        self.color = YELLOW

    def set_end(self):  # Set the node to be the end
        self.color = TURQUOISE

    def set_path(self):  # Set the node to be the path
        self.color = PURPLE

    def draw(self, screen):  # Draw the nodes on the screen
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):  # Update the neighbors of the node
        self.neighbors = []
        if self.row < self.tot_rows - 1 and not grid[self.row + 1][self.column].is_barrier():  # Down
            self.neighbors.append(grid[self.row + 1][self.column])

        if self.row > 0 and not grid[self.row - 1][self.column].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.column])

        if self.column < self.tot_rows - 1 and not grid[self.row][self.column + 1].is_barrier():  # Right
            self.neighbors.append(grid[self.row][self.column + 1])

        if self.column > 0 and not grid[self.row][self.column -
                                                  1].is_barrier():  # Left
            self.neighbors.append(grid[self.row][self.column - 1])

    def __lt__(self, other):  # It handles what if we compared 2 Nodes
        return False


# Heuristic Function
def heuristic(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)


# Make a grid
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


# Draw the grid
def draw_grid(screen, rows, width):
    gap = width // rows
    for i in range(rows):  # for the rows
        pygame.draw.line(screen, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):  # for the columns
            pygame.draw.line(screen, GREY, (j * gap, 0), (j * gap, width))


# The Main draw function that will draw every thing
def main_draw(screen, grid, rows, width):
    screen.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(screen)

    draw_grid(screen, rows, width)
    pygame.display.update()


# Function to Know the mouse position
def get_clicked_position(pos, rows, width):
    gap = width // rows
    x, y = pos

    row = x // gap
    column = y // gap

    return row, column


# to draw the shortest path
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.set_path()
        draw()


# A* Algorithm application
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_position(), end.get_position())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:  # we found the shortest path
            reconstruct_path(came_from, current, draw)
            end.set_end()
            start.set_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_position(),
                                                             end.get_position())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.set_opened()

        draw()
        if current != start:
            current.set_closed()

    return False


# Main Loop
def main(screen, width):
    ROWS = 50

    # make the grid
    grid = make_grid(ROWS, width)

    start_node = None
    end_node = None
    running = True

    # Start Loop
    while running:
        main_draw(screen, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Quit the program

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()  # clicks the left mouse button
                row, column = get_clicked_position(pos, ROWS, width)
                node = grid[row][column]

                # Assign the start an end nodes
                if not start_node and node != end_node:
                    start_node = node
                    start_node.set_start()
                elif not end_node and node != start_node:
                    end_node = node
                    end_node.set_end()
                elif node != start_node and node != end_node:
                    node.set_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()  # clicks the right mouse button
                row, column = get_clicked_position(pos, ROWS, width)
                node = grid[row][column]
                node.reset()
                if node == start_node:
                    start_node = None
                elif node == end_node:
                    end_node = None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_node and end_node:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda: main_draw(screen, grid, ROWS, width), grid, end_node, start_node)
                if event.key == pygame.K_c:  # to clear the screen
                    start_node = None
                    end_node = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(SCREEN, WIDTH)
