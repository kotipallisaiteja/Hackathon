import pygame
import numpy as np
import random
import heapq

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Difficulty Settings
DIFFICULTY_LEVELS = {
    "Easy": (10, 10, 5),
    "Medium": (15, 25, 10),
    "Hard": (20, 40, 15),
    "Extreme": (25, 60, 20)
}

# Directions (UP, DOWN, LEFT, RIGHT)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver AI")
clock = pygame.time.Clock()

# Font setup
font = pygame.font.Font(None, 40)

# Draw text on screen
def draw_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Generate Maze
def generate_maze(difficulty):
    global GRID_SIZE, CELL_SIZE
    GRID_SIZE, num_obstacles, num_traps = DIFFICULTY_LEVELS[difficulty]
    CELL_SIZE = WIDTH // GRID_SIZE
    
    maze = np.zeros((GRID_SIZE, GRID_SIZE))
    maze[1, 1] = 2  # Start position
    maze[GRID_SIZE - 2, GRID_SIZE - 2] = 3  # Goal

    for _ in range(num_obstacles):
        x, y = random.randint(1, GRID_SIZE - 2), random.randint(1, GRID_SIZE - 2)
        maze[x, y] = 1  # Wall

    for _ in range(num_traps):
        x, y = random.randint(1, GRID_SIZE - 2), random.randint(1, GRID_SIZE - 2)
        if maze[x, y] == 0:
            maze[x, y] = 4  # Trap

    return maze

# Draw Maze
def draw_maze(maze, player_pos):
    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = WHITE
            if maze[row, col] == 1:
                color = BLACK  # Wall
            elif maze[row, col] == 2:
                color = GREEN  # Start
            elif maze[row, col] == 3:
                color = RED  # Goal
            elif maze[row, col] == 4:
                color = YELLOW  # Trap
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, BLUE, (player_pos[1] * CELL_SIZE, player_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

# A* Pathfinding Algorithm
def a_star_search(maze, start, goal):
    """Uses A* algorithm to find the shortest path to the goal."""
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan Distance

    queue = []
    heapq.heappush(queue, (0, start))
    
    came_from = {start: None}
    cost_so_far = {start: 0}
    
    while queue:
        _, current = heapq.heappop(queue)
        
        if current == goal:
            break  # Goal reached
        
        for dx, dy in DIRECTIONS:
            next_pos = (current[0] + dx, current[1] + dy)

            if (0 <= next_pos[0] < GRID_SIZE and 0 <= next_pos[1] < GRID_SIZE 
                and maze[next_pos[0], next_pos[1]] != 1):
                
                move_cost = 1 if maze[next_pos[0], next_pos[1]] != 4 else 5  # Avoid traps
                
                new_cost = cost_so_far[current] + move_cost
                
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + heuristic(goal, next_pos)
                    heapq.heappush(queue, (priority, next_pos))
                    came_from[next_pos] = current

    # Reconstruct the path
    path = []
    step = goal
    while step in came_from:
        path.append(step)
        step = came_from[step]
    path.reverse()
    return path

# Display "You Won the Game!" message
def display_win_message():
    screen.fill(WHITE)  # Set background to white
    draw_text("You won the game!", WIDTH // 4, HEIGHT // 2, RED)
    pygame.display.flip()
    pygame.time.delay(2000)  # Display message for 2 seconds

# Run AI (Faster Pathfinding)
def run_ai(maze):
    player_pos = (1, 1)
    goal_pos = (GRID_SIZE - 2, GRID_SIZE - 2)
    path = a_star_search(maze, player_pos, goal_pos)
    
    running = True
    for step in path:
        if not running:
            break
        player_pos = step
        draw_maze(maze, player_pos)
        pygame.time.delay(150)  # Speed of movement

        if player_pos == goal_pos:
            display_win_message()  # Display the win message when goal is reached
            break  # Exit loop after winning

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

# Draw Difficulty Selection Menu
def draw_menu():
    screen.fill(WHITE)
    pygame.display.set_caption("Select Difficulty")
    
    menu_options = [("Easy", GREEN, 180), ("Medium", YELLOW, 250), ("Hard", RED, 320), ("Extreme", BLACK, 390)]
    buttons = []

    for text, color, y in menu_options:
        pygame.draw.rect(screen, color, (200, y, 200, 50))
        draw_text(text, 250, y + 10, WHITE)
        buttons.append((text, 200, y, 200, 50))

    pygame.display.flip()
    return buttons

# Get user difficulty selection
def get_user_difficulty():
    buttons = draw_menu()
    selected_difficulty = None

    while selected_difficulty is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for text, bx, by, bw, bh in buttons:
                    if bx <= x <= bx + bw and by <= y <= by + bh:
                        return text  # Return selected difficulty

# Main Function
def main():
    difficulty = get_user_difficulty()
    maze = generate_maze(difficulty)
    run_ai(maze)
    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()
