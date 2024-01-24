import pygame
import random

pygame.init()

White = (97, 96, 93)
Pink = (255, 155, 210)
Purple = (64, 43, 58)
Black = (0, 0, 0)
Yellow = (248, 229, 89)

WIDTH, HEIGHT = 1200, 1200
TILE_SIZE = 5
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 120

screen = pygame.display.set_mode((WIDTH, HEIGHT))

CLOCK = pygame.time.Clock()


def draw_grid(positions):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, Yellow, (*top_left, TILE_SIZE, TILE_SIZE))

    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, Black, (0, row * TILE_SIZE),
                         (WIDTH, row * TILE_SIZE))
    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, Black, (col * TILE_SIZE, 0),
                         (col * TILE_SIZE, HEIGHT))


def gen(num):
    return set((random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for i in range(num))


def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbours = get_neighbors(position)
        all_neighbors.update(neighbours)

        neighbours = list(filter(lambda x: x in positions, neighbours))

        if len(neighbours) in [2, 3]:
            new_positions.add(position)

    for position in all_neighbors:
        neighbours = get_neighbors(position)

        neighbours = list(filter(lambda x: x in positions, neighbours))

        if len(neighbours) == 3:
            new_positions.add(position)

    return new_positions


def get_neighbors(pos):
    x, y = pos
    neighbours = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue

            new_x, new_y = x + dx, y + dy

            if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                neighbours.append((new_x, new_y))

    return neighbours


def main():
    running = True
    playing = False
    count = 0
    update_freq = 120

    positions = set()

    while running:

        CLOCK.tick(FPS)

        if playing:
            count += 1

        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)
                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    col = x // TILE_SIZE
                    row = y // TILE_SIZE
                    pos = (col, row)
                    if pos in positions:
                        positions.remove(pos)
                    else:
                        positions.add(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                    count = 0

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                if event.key == pygame.K_z:
                    positions = gen(random.randrange(2, 5) * GRID_WIDTH)

        screen.fill(White)
        draw_grid(positions)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
