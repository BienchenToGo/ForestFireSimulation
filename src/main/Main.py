import pygame
import random

# Size of window
SCREEN_SIZE = 500
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

# Size of a tree
TREE_COUNT = 200
TREE_SIZE = SCREEN_SIZE  / TREE_COUNT

SPREAD_POSSIBILITY = 0.25

# Color
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Tree:
    def __init__(self, x, y):
        # Neighbours
        self.neighbours = []

        # Koordinates
        self.x = x
        self.y = y

        self.isOnFire = False

        # Draw the tree
        pygame.draw.rect(screen, GREEN, (self.x * TREE_SIZE, self.y * TREE_SIZE, TREE_SIZE, TREE_SIZE))

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours

    def is_on_fire(self):
        return self.isOnFire

    def set_on_fire(self):
        self.isOnFire = True
        pygame.draw.rect(screen, RED, (self.x * TREE_SIZE, self.y * TREE_SIZE, TREE_SIZE, TREE_SIZE))


    def update(self):
        for neighbour in self.neighbours:
            if neighbour.is_on_fire():
                self.set_on_fire()
                return

    def spread(self):
        if self.isOnFire and random.choice(range(int(1 / SPREAD_POSSIBILITY))) == 0:
            self.neighbours[random.choice(range(4))].set_on_fire()


def flatten_matrix(matrix):
    flat = []
    for row in matrix:
        for x in row:
            flat.append(x)
    return flat


def main():
    pygame.init()

    screen.fill((255, 255, 255))

    # Generate enough trees
    trees = [[Tree(x, y) for x in range(TREE_COUNT)] for y in range(TREE_COUNT)]

    # Assemble neighbourhood
    for x in range(TREE_COUNT):
        for y in range(TREE_COUNT):
            neighbours = []
            if y - 1 >= 0: # North
                neighbours.append(trees[x][y - 1])
            else:
                neighbours.append(trees[x][y])
            if x + 1 < TREE_COUNT: # East
                neighbours.append(trees[x + 1][y])
            else:
                neighbours.append(trees[x][y])
            if y + 1 < TREE_COUNT: # South
                neighbours.append(trees[x][y + 1])
            else:
                neighbours.append(trees[x][y])
            if x - 1 >= 0: # West
                neighbours.append(trees[x - 1][y])
            else:
                neighbours.append(trees[x][y])
            trees[x][y].set_neighbours(neighbours)

    # Convert matrix to list
    trees = flatten_matrix(trees)

    # Set three trees on fire
    for i in range(10):
        random_tree = int(random.choice(range(TREE_COUNT * TREE_COUNT)))
        trees[random_tree].set_on_fire()

    trees_on_fire = []

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update trees_on_fire
        for tree in trees:
            if tree.is_on_fire() and not tree in trees_on_fire:
                trees_on_fire.append(tree)

        # Update spread
        for tree in trees_on_fire:
            tree.spread()

        # Refresh
        pygame.display.update()

        # Set fps
        clock.tick(30)
    pygame.quit()

# Run application
main()

