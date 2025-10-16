import pygame
import random
import sys
from typing import List, Tuple, Optional

class Game2048:
    def __init__(self, size: int = 4):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.score = 0
        self.game_over = False
        self.won = False
        
        pygame.init()
        
        self.BG_COLOR = (187, 173, 160)
        self.EMPTY_COLOR = (205, 193, 180)
        self.FONT_COLOR = (119, 110, 101)
        self.LIGHT_FONT_COLOR = (249, 246, 242)
        
        self.TILE_COLORS = {
            0: (205, 193, 180),
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46)
        }
        
        self.cell_size = 100
        self.cell_padding = 10
        self.width = size * (self.cell_size + self.cell_padding) + self.cell_padding
        self.height = self.width + 100  
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("2048 Game")
        self.font = pygame.font.SysFont("Arial", 36, bold=True)
        self.score_font = pygame.font.SysFont("Arial", 24)
        
        self.add_random_tile()
        self.add_random_tile()
    
    def add_random_tile(self) -> None:
        """Add a random tile (2 or 4) to an empty cell"""
        empty_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    empty_cells.append((i, j))
        
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4
    
    def move(self, direction: str) -> bool:
        """
        Move tiles in the specified direction
        Returns True if the move changed the grid
        """
        if self.game_over:
            return False
        
        old_grid = [row[:] for row in self.grid]
        
        if direction == "left":
            self.move_left()
        elif direction == "right":
            self.move_right()
        elif direction == "up":
            self.move_up()
        elif direction == "down":
            self.move_down()
        
        if old_grid != self.grid:
            self.add_random_tile()
            self.check_game_state()
            return True
        return False
    
    def move_left(self) -> None:
        """Move and merge tiles to the left"""
        for i in range(self.size):
            row = [cell for cell in self.grid[i] if cell != 0]
            merged = []
            
            j = 0
            while j < len(row):
                if j + 1 < len(row) and row[j] == row[j + 1]:
                    merged_value = row[j] * 2
                    merged.append(merged_value)
                    self.score += merged_value
                    j += 2
                else:
                    merged.append(row[j])
                    j += 1
            
            merged.extend([0] * (self.size - len(merged)))
            self.grid[i] = merged
    
    def move_right(self) -> None:
        """Move and merge tiles to the right"""
        for i in range(self.size):
            row = [cell for cell in self.grid[i] if cell != 0]
            merged = []
            
            j = len(row) - 1
            while j >= 0:
                if j - 1 >= 0 and row[j] == row[j - 1]:
                    merged_value = row[j] * 2
                    merged.insert(0, merged_value)
                    self.score += merged_value
                    j -= 2
                else:
                    merged.insert(0, row[j])
                    j -= 1
            
            merged = [0] * (self.size - len(merged)) + merged
            self.grid[i] = merged
    
    def move_up(self) -> None:
        """Move and merge tiles upward"""
        self.transpose_grid()
        self.move_left()
        self.transpose_grid()
    
    def move_down(self) -> None:
        """Move and merge tiles downward"""
        self.transpose_grid()
        self.move_right()
        self.transpose_grid()
    
    def transpose_grid(self) -> None:
        """Transpose the grid (swap rows and columns)"""
        self.grid = [list(row) for row in zip(*self.grid)]
    
    def can_move(self) -> bool:
        """Check if any moves are possible"""
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return True
        
        for i in range(self.size):
            for j in range(self.size):
                current = self.grid[i][j]
                if j < self.size - 1 and self.grid[i][j + 1] == current:
                    return True
                if i < self.size - 1 and self.grid[i + 1][j] == current:
                    return True
        
        return False
    
    def check_game_state(self) -> None:
        """Check if game is won or lost"""
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 2048:
                    self.won = True
        
        if not self.can_move():
            self.game_over = True
    
    def draw(self) -> None:
        """Draw the game board"""
        self.screen.fill(self.BG_COLOR)
        score_text = self.score_font.render(f"Score: {self.score}", True, self.FONT_COLOR)
        self.screen.blit(score_text, (20, 20))
        
        restart_text = self.score_font.render("Restart (R)", True, self.FONT_COLOR)
        self.screen.blit(restart_text, (self.width - 120, 20))
        
        for i in range(self.size):
            for j in range(self.size):
                value = self.grid[i][j]
                
                x = j * (self.cell_size + self.cell_padding) + self.cell_padding
                y = i * (self.cell_size + self.cell_padding) + self.cell_padding + 80
                
                color = self.TILE_COLORS.get(value, (60, 58, 50))
                pygame.draw.rect(self.screen, color, 
                               (x, y, self.cell_size, self.cell_size), 
                               0, 5)  
                
                if value != 0:
                    font_color = self.LIGHT_FONT_COLOR if value > 4 else self.FONT_COLOR
                    
                    font_size = 36 if value < 1000 else 30 if value < 10000 else 24
                    value_font = pygame.font.SysFont("Arial", font_size, bold=True)
                    
                    value_text = value_font.render(str(value), True, font_color)
                    text_rect = value_text.get_rect(center=(x + self.cell_size // 2, 
                                                          y + self.cell_size // 2))
                    self.screen.blit(value_text, text_rect)
        
        if self.game_over:
            self.draw_message("Game Over!", "Press R to restart")
        elif self.won:
            self.draw_message("You Win!", "Press R to restart or continue playing")
    
    def draw_message(self, title: str, subtitle: str) -> None:
        """Draw a message overlay"""
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((255, 255, 255))
        self.screen.blit(overlay, (0, 0))
        
        title_font = pygame.font.SysFont("Arial", 48, bold=True)
        title_text = title_font.render(title, True, self.FONT_COLOR)
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 2 - 30))
        self.screen.blit(title_text, title_rect)
        
        subtitle_font = pygame.font.SysFont("Arial", 24)
        subtitle_text = subtitle_font.render(subtitle, True, self.FONT_COLOR)
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, self.height // 2 + 20))
        self.screen.blit(subtitle_text, subtitle_rect)
    
    def restart(self) -> None:
        """Restart the game"""
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.add_random_tile()
        self.add_random_tile()
    
    def run(self) -> None:
        """Main game loop"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart()
                    elif not self.game_over:
                        if event.key == pygame.K_LEFT:
                            self.move("left")
                        elif event.key == pygame.K_RIGHT:
                            self.move("right")
                        elif event.key == pygame.K_UP:
                            self.move("up")
                        elif event.key == pygame.K_DOWN:
                            self.move("down")
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

def main():
    board_size = 4
    game = Game2048(board_size)
    game.run()

if __name__ == "__main__":
    main()