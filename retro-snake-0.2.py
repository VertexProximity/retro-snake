import tkinter as tk
import random

# Constants for the game
GRID_SIZE = 20
GRID_PIXELS = 500
SNAKE_LENGTH = 3
SNAKE_SPEED = 250  # Milliseconds

# Colors for the game
BG_COLOR = "#FFFFFF"
SNAKE_COLOR = "#000000"
FOOD_COLOR = "#FF0000"
OBSTACLE_COLOR = "#0000FF"
POWERUP_COLOR = "#00FF00"

class SnakeGame:
  def __init__(self):
    # Set up the main window
    self.window = tk.Tk()
    self.window.title("Python Snake Game")
    self.window.resizable(False, False)

    # Create the canvas for the game
    self.canvas = tk.Canvas(self.window, width=GRID_PIXELS, height=GRID_PIXELS, bg=BG_COLOR)
    self.canvas.pack()

    # Create a frame for the score and level display
    self.score_frame = tk.Frame(self.window)
    self.score_frame.pack()
    self.score_label = tk.Label(self.score_frame, text="Score: 0")
    self.score_label.pack(side="left")
    self.level_label = tk.Label(self.score_frame, text="Level: 1")
    self.level_label.pack(side="right")

    # Create a pause button
    self.pause_button = tk.Button(self.window, text="Pause", command=self.toggle_pause)
    self.pause_button.pack()

    # Set up the snake's starting position and direction
    self.snake_positions = [(GRID_SIZE // 2, GRID_SIZE // 2)]
    self.direction = "Right"

    # Set up the food's starting position
    self.food_position = self.get_random_position()

    # Set up the game state
    self.paused = False
    self.score = 0
    self.level = 1

    # Set up the obstacles and power-ups
    self.obstacles = []
    self.power_ups = []
    self.power_up_active = False
    self.power_up_timer = 0

    # Bind the arrow keys to the snake's movement
    self.window.bind("<Left>", self.turn_left)
    self.window.bind("<Right>", self.turn_right)
    self.window.bind("<up>", self.up)
    self.window.bind("<down>", self.down)

  def run(self):
    """Starts the game loop."""
    self.window.after(SNAKE_SPEED, self.game_loop)
    self.window.mainloop()

  def game_loop(self):
    """Updates the game state and redraws the game elements."""
    if not self.paused:
      self.update_snake()
      self.check_collisions()
      self.check_level_up()
      self.update_obstacles()
      self.update_power_ups()
      self.draw()

    self.window.after(SNAKE_SPEED, self.game_loop)

  def update_snake(self):
    """Updates the position of the snake."""
    # Calculate the new snake head position
    new_head_position = self.get_new_head_position()

    # Check if the snake has run into itself or an obstacle
    if (new_head_position in self.snake_positions
        or new_head_position in self.obstacles):
      self.end_game()
      return

    # Add the new head position to the snake
    self.snake_positions.insert(0, new_head_position)

    # Remove the snake's tail if it has not eaten food
    if new_head_position != self.food_position:
      self.snake_positions.pop()
    else:
      # Generate a new food position
      self.food_position = self.get_random_position()

      # Increase the score
      self.score += 1
      self.score_label.config(text="Score: " + str(self.score))

  def check_collisions(self):
    """Checks if the snake has run into a power-up or food."""
    head_position = self.snake_positions[0]

    # Check for power-up collision
    for power_up in self.power_ups:
      if head_position == power_up:
        self.power_up_active = True
        self.power_up_timer = 250  # Power-up lasts for 250 game loops
        self.power_ups.remove(power_up)

    # Check for food collision
    if head_position == self.food_position:
      # Increase the snake's length
      self.snake_positions.append(self.food_position)

      # Generate a new food position
      self.food_position = self.get_random_position()

      # Increase the score
      self.score += 1
      self.score_label.config(text="Score: " + str(self.score))

  def check_level_up(self):
    """Checks if the player has reached the score needed to advance to the next level."""
    if self.score >= self.level * 10:
      # Increase the level
      self.level += 1
      self.level_label.config(text="Level: " + str(self.level))

      # Add obstacles to the game
      for i in range(self.level):
        self.obstacles.append()
    def update_obstacles(self):
     for i, obstacle in enumerate(self.obstacles):
      # Calculate the new obstacle position
      new_obstacle_position = self.get_new_obstacle_position(obstacle, self.snake_positions[0])

      # Check if the obstacle has collided with the snake
      if new_obstacle_position in self.snake_positions:
        self.end_game()
        return

      # Update the obstacle position
      self.obstacles[i] = new_obstacle_position

  def update_power_ups(self):
    """Updates the positions of the power-ups and the power-up timer."""
    if self.power_up_active:
      self.power_up_timer -= 1
      if self.power_up_timer == 0:
        self.power_up_active = False

    if len(self.power_ups) < 3 and random.randint(1, 100) == 1:
      self.power_ups.append(self.get_random_position())

  def draw(self):
    """Draws the game elements on the canvas."""
    # Clear the canvas
    self.canvas.delete("all")

    # Draw the snake
    for x, y in self.snake_positions:
      self.draw_rectangle(x, y, SNAKE_COLOR)
  def draw_rectangle(self, x, y, color):
    """Draws a rectangle at the given grid position with the given color."""
    x1 = x * GRID_PIXELS // GRID_SIZE
    y1 = y * GRID_PIXELS // GRID_SIZE
    x2 = x1 + GRID_PIXELS // GRID_SIZE
    y2 = y1 + GRID_PIXELS // GRID_SIZE
    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

  def get_random_position(self):
    """Returns a random grid position that is not occupied by the snake or an obstacle."""
    while True:
      x = random.randint(0, GRID_SIZE - 1)
      y = random.randint(0, GRID_SIZE - 1)
      if (x, y) not in self.snake_positions and (x, y) not in self.obstacles:
        return x, y

  def get_new_head_position(self):
    """Calculates the new position of the snake's head based on its current direction."""
    if self.direction == "Up":
      return self.snake_positions[0][0], (self.snake_positions[0][1] - 1) % GRID_SIZE
    elif self.direction == "Down":
      return self.snake_positions[0][0], (self.snake_positions[0][1] + 1) % GRID_SIZE
    elif self.direction == "Left":
      return (self.snake_positions[0][0] - 1) % GRID_SIZE, self.snake_positions[0][1]
    elif self.direction == "Right":
      return (self.snake_positions[0][0] + 1) % GRID_SIZE, self.snake_positions[0][1]

  def get_new_obstacle_position(self, obstacle, snake_head):
    """Calculates the new position of an obstacle based on its current position and the position of the snake's head."""
    # Calculate the distance between the obstacle and the snake's head
    distance = abs(obstacle[0] - snake_head[0]) + abs(obstacle[1] - snake_head[1])

    # Move the obstacle towards the snake if it is more than 2 grid
    def get_new_obstacle_position(self, obstacle, snake_head):
   
    # Calculate the distance between the obstacle and the snake's head
     distance = abs(obstacle[0] - snake_head[0]) + abs(obstacle[1] - snake_head[1])

    # Move the obstacle towards the snake if it is more than 2 grid spaces away
    if distance > 2:
      if obstacle[0] < snake_head[0]:
        x = (obstacle[0] + 1) % GRID_SIZE
      elif obstacle[0] > snake_head[0]:
        x = (obstacle[0] - 1) % GRID_SIZE
      else:
        x = obstacle[0]

      if obstacle[1] < snake_head[1]:
        y = (obstacle[1] + 1) % GRID_SIZE
      elif obstacle[1] > snake_head[1]:
        y = (obstacle[1] - 1) % GRID_SIZE
      else:
        y = obstacle[1]
    else:
      # Otherwise, move the obstacle randomly
      x = (obstacle[0] + random.randint(-1, 1)) % GRID_SIZE
      y = (obstacle[1] + random.randint(-1, 1)) % GRID_SIZE

    return x, y

  def turn_left(self, event):
    """Turns the snake left if it is not already moving right."""
    if self.direction != "Right":
      self.direction = "Left"

  def turn_right(self, event):
    """Turns the snake right if it is not already moving left."""
    if self.direction != "Left":
      self.direction = "Right"

  def toggle_pause(self):
    """Pauses or unpauses the game"""

    self.paused = not self.paused
    if self.paused:
      self.pause_button.config(text="Unpause")
    else:
      self.pause_button.config(text="Pause")

  def end_game(self):
    """Ends the game and displays a game over message."""
    self.window.unbind("<Left>")
    self.window.unbind("<Right>")
    self.canvas.create_text(GRID_PIXELS // 2, GRID_PIXELS // 2, text="Game Over", font=("Arial", 24))
    self.pause_button.pack_forget()

if __name__ == "__main__":
  game = SnakeGame()
  game.run()

