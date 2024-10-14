import tkinter as tk
import random
import time
import math


class Actor:
    def __init__(self, color):
        self.color = color
        self.is_satisfied = False


class NeighboursApp:
    def __init__(self, root):
        # Canvas dimensions and margin
        self.width = 500
        self.height = 500
        self.margin = 50
        self.dot_size = 0
        self.interval = 0.45  # in seconds

        # Initialize tkinter canvas
        self.root = root
        self.canvas = tk.Canvas(root, width=self.width, height=self.height)
        self.canvas.pack()

        # Initialize world
        self.init_world()
        self.last_update_time = time.time()

        # Start animation
        self.update_world()
        self.root.after(int(self.interval * 1000), self.animate)

    def init_world(self):
        # Distribution percentages for RED, BLUE, and NONE
        dist = [0.25, 0.25, 0.50]
        n_locations = 900 # Number of locations (should be a square and also work for 25000)

        # Calculate world size
        size = int(math.sqrt(n_locations))
        self.world = [[None for _ in range(size)] for _ in range(size)]

        # Initialize world with random actors
        for row in range(size):
            for col in range(size):
                rand = random.random()
                if rand < dist[0]:
                    self.world[row][col] = Actor("red")
                elif rand < dist[0] + dist[1]:
                    self.world[row][col] = Actor("blue")
                else:
                    self.world[row][col] = None

        # Adjust screen size based on the number of locations
        self.fix_screen_size(n_locations)

    def fix_screen_size(self, n_locations):
        self.dot_size = 9000 / n_locations
        if self.dot_size < 1:
            self.dot_size = 2
        self.width = math.sqrt(n_locations) * self.dot_size + 2 * self.margin
        self.height = self.width

    def update_world(self):
        threshold = 0.7
        size = len(self.world)

        # Iterate over the grid to check for unsatisfied actors
        for row in range(size):
            for col in range(size):
                actor = self.world[row][col]
                if actor is None:
                    continue  # Skip empty cells

                # Calculate the similarity ratio around the actor
                like_me = 0
                total_neighbours = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue  # Skip itself
                        new_row, new_col = row + i, col + j
                        if self.is_valid_location(size, new_row, new_col):
                            neighbour = self.world[new_row][new_col]
                            if neighbour is not None:
                                total_neighbours += 1
                                if neighbour.color == actor.color:
                                    like_me += 1

                similarity = (like_me / total_neighbours) if total_neighbours > 0 else 0
                actor.is_satisfied = similarity >= threshold

                # If not satisfied, move the actor to a random empty location
                if not actor.is_satisfied:
                    new_row, new_col = None, None
                    while True:
                        new_row = random.randint(0, size - 1)
                        new_col = random.randint(0, size - 1)
                        if self.world[new_row][new_col] is None:
                            break

                    # Move actor to the new position
                    self.world[new_row][new_col] = actor
                    self.world[row][col] = None

    def is_valid_location(self, size, row, col):
        return 0 <= row < size and 0 <= col < size

    def render_world(self):
        self.canvas.delete("all")  # Clear the canvas
        size = len(self.world)
        for row in range(size):
            for col in range(size):
                x = int(self.dot_size * col + self.margin)
                y = int(self.dot_size * row + self.margin)
                if self.world[row][col] is not None:
                    color = self.world[row][col].color
                    self.canvas.create_oval(x, y, x + self.dot_size, y + self.dot_size, fill=color)

    def animate(self):
        current_time = time.time()
        if current_time - self.last_update_time >= self.interval:
            self.update_world()
            self.render_world()
            self.last_update_time = current_time
        self.root.after(int(self.interval * 1000), self.animate)


def main():
    root = tk.Tk()
    app = NeighboursApp(root)
    root.title("Segregation Simulation")
    root.mainloop()


if __name__ == "__main__":
    main()