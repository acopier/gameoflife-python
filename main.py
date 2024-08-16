import pygame
import numpy as np
import sys

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 10
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class GameOfLife:
  def __init__(self):
    self.rows = WINDOW_HEIGHT // CELL_SIZE
    self.cols = WINDOW_WIDTH // CELL_SIZE
    self.grid = np.zeros((self.rows, self.cols), dtype=bool)
    self.running = False

    pygame.init()
    self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Conway's Game of Life")
    self.clock = pygame.time.Clock()

  def randomize(self):
    self.grid = np.random.choice([False, True], size=(self.rows, self.cols))

  def update(self):
    neighbors_count = sum(
      np.roll(np.roll(self.grid, i, 0), j, 1)
      for i in [-1, 0, 1]
      for j in [-1, 0, 1]
      if (i, j) != (0, 0)
    )

    self.grid = (neighbors_count == 3) | (self.grid & (neighbors_count == 2))

  def draw_grid(self):
    self.window.fill(BLACK)
    for row in range(self.rows):
      for col in range(self.cols):
        if self.grid[row, col]:
          rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
          pygame.draw.rect(self.window, WHITE, rect)
    pygame.display.flip()

  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
          x, y = event.pos
          col = x // CELL_SIZE
          row = y // CELL_SIZE
          if 0 <= col < self.cols and 0 <= row < self.rows:
            self.grid[row, col] = not self.grid[row, col]
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            self.running = not self.running

      if self.running:
        self.update()

      self.draw_grid()
      self.clock.tick(FPS)


if __name__ == '__main__':
  game = GameOfLife()
  game.run()
