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

    # Set up game state variables
    self.score = 0
    self.level = 1
    self.paused = False

    # Bind arrow keys to the game
    self.window.bind("<Left>", self.turn_left)
    self.window.bind("<Right>", self.turn_right)
    self.window.bind("<Up>", self.turn_up)
    self.window.bind("<Down>", self.turn_down)

    # Start the game loop
    self.window.after(SNAKE_SPEED, self.game_loop)

  def get_random_position(self):
    """Returns a random (x, y) position that is not occupied by the snake."""
    while True:
      x = random.randint(0, GRID_SIZE - 1)
      y = random.randint(0, GRID_SIZE - 1)
      if (x, y) not in self.snake_positions:
        return (x, y)

  def toggle_pause(self):
    """Toggles the paused state of the game."""
    self.paused = not self.paused
    if self.paused:
      self
  def game_loop(self):
    """The main game loop. Updates the game state and redraws the canvas."""
    # Check if the game is paused
    if self.paused:
      self.window.after(SNAKE_SPEED, self.game_loop)
      return

    # Check if the snake has hit the edge of the grid or itself
    x, y = self.snake_positions[0]
    if (
        x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE
        or (self.direction == "Up" and y == 0)
        or (self.direction == "Down" and y == GRID_SIZE - 1)
        or (self.direction == "Left" and x == 0)
        or (self.direction == "Right" and x == GRID_SIZE - 1)
        or (self.direction == "Up" and (x, y - 1) in self.snake_positions)
        or (self.direction == "Down" and (x, y + 1) in self.snake_positions)
        or (self.direction == "Left" and (x - 1, y) in self.snake_positions)
        or (self.direction == "Right" and (x + 1, y) in self.snake_positions)
    ):
      self.end_game()
      return

    # Check if the snake has eaten the food
    if self.snake_positions[0] == self.food_position:
      self.score += 1
      self.score_label.config(text="Score: {}".format(self.score))
      self.food_position = self.get_random_position()
      self.snake_positions.append(self.snake_positions[-1])

      # Increase the level and speed every 5 points
      if self.score % 5 == 0:
        self.level += 1
        self.level_label.config(text="Level: {}".format(self.level))
        SNAKE_SPEED = max(50, SNAKE_SPEED - 50)

    # Update the snake's position
    if self.direction == "Up":
      self.snake_positions.insert(0, (x, y - 1))
    elif self.direction == "Down":
      self.snake_positions.insert(0, (x, y + 1))
    elif self.direction == "Left":
      self.snake_positions.insert(0, (x - 1, y))
    elif self.direction == "Right":
      self.snake_positions.insert(0, (x + 1, y))

    # Remove the snake's tail
    self.snake_positions = self.snake_positions[:SNAKE_LENGTH]

    # Redraw the canvas
    self.canvas.delete("all")
    for x, y in self.snake_positions:
      self.canvas.create_rectangle(
          x * GRID_PIXELS // GRID_SIZE, y * GRID_PIXELS // GRID_SIZE,
          (x + 1))

    def turn_left(self, event):
   
        if self.direction != "Right":
          self.direction = "Left"

  def turn_right(self, event):
    """Turns the snake right if it is not already moving left."""
    if self.direction != "Left":
      self.direction = "Right"

  def turn_up(self, event):
    """Turns the snake up if it is not already moving down."""
    if self.direction != "Down":
      self.direction = "Up"

  def turn_down(self, event):
    """Turns the snake down if it is not already moving up."""
    if self.direction != "Up":
      self.direction = "Down"

  def end_game(self):
    """Ends the game and displays a game over message."""
    self.canvas.create_text(
        GRID_PIXELS // 2, GRID_PIXELS // 2,
        text="Game Over!", fill=SNAKE_COLOR, font=("Helvetica", 32)
    )
    self.window.unbind("<Left>")
    self.window.unbind("<Right>")
    self.window.unbind("<Up>")
    self.window.unbind("<Down>")

if __name__ == "__main__":
  SnakeGame()
  tk.mainloop()

