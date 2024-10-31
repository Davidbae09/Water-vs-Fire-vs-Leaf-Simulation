import tkinter as tk
import random
from tkinter import messagebox

# Constants for element types
WATER = "water"
FIRE = "fire"
LEAF = "leaf"

class Element:
    def __init__(self, canvas, element_type, position, speed=4):
        self.canvas = canvas
        self.element_type = element_type
        self.size = 20
        self.dx = random.choice([-speed, speed])
        self.dy = random.choice([-speed, speed])
        self.x, self.y = self.get_initial_position(position)
        self.shape = self.create_shape()

    def get_initial_position(self, position):
        if position == "left_bottom":
            return random.randint(0, self.canvas.winfo_width() // 3 - self.size), random.randint(self.canvas.winfo_height() // 2, self.canvas.winfo_height() - self.size)
        elif position == "right_bottom":
            return random.randint(2 * self.canvas.winfo_width() // 3, self.canvas.winfo_width() - self.size), random.randint(self.canvas.winfo_height() // 2, self.canvas.winfo_height() - self.size)
        elif position == "top_center":
            return random.randint(self.canvas.winfo_width() // 3, 2 * self.canvas.winfo_width() // 3 - self.size), random.randint(0, self.canvas.winfo_height() // 2 - self.size)

    def create_shape(self):
        color = {"water": "blue", "fire": "red", "leaf": "green"}.get(self.element_type, "black")
        return self.canvas.create_oval(self.x, self.y, self.x + self.size, self.y + self.size, fill=color)

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Check for wall collisions
        if self.x <= 0 or self.x >= self.canvas.winfo_width() - self.size:
            self.dx *= -1
        if self.y <= 0 or self.y >= self.canvas.winfo_height() - self.size:
            self.dy *= -1

        # Update the shape position
        self.canvas.coords(self.shape, self.x, self.y, self.x + self.size, self.y + self.size)

    def change_type(self, new_type):
        if self.element_type != new_type:
            self.element_type = new_type
            self.canvas.delete(self.shape)
            self.shape = self.create_shape()

class Simulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Element Simulation")
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()

        # Slider for speed control
        self.speed_slider = tk.Scale(root, from_=1, to=10, orient="horizontal", label="Speed", command=self.update_speed)
        self.speed_slider.set(4)  # Default speed
        self.speed_slider.pack()

        self.elements = []
        self.speed = self.speed_slider.get()
        self.running = True  # Flag to control the simulation status

        # Use after to create elements after the canvas is fully initialized
        self.root.after(100, self.create_elements)  # Delay to ensure the canvas is ready
        self.update()

    def create_elements(self):
        # Create 30 elements (10 for each position group)
        positions = ["left_bottom"] * 8 + ["right_bottom"] * 8 + ["top_center"] * 8
        element_types = [random.choice([WATER, FIRE, LEAF]) for _ in range(24)]
        self.elements = [Element(self.canvas, element_types[i], positions[i], speed=self.speed) for i in range(24)]

    def update(self):
        if self.running:  # Check if the simulation is running
            self.move_elements()
            self.check_collisions()
            self.check_winner()
            self.root.after(50, self.update)

    def update_speed(self, value):
        self.speed = int(value)
        for element in self.elements:
            element.dx = self.speed if element.dx > 0 else -self.speed
            element.dy = self.speed if element.dy > 0 else -self.speed

    def move_elements(self):
        for element in self.elements:
            element.move()

    def check_collisions(self):
        for i in range(len(self.elements)):
            for j in range(i + 1, len(self.elements)):
                if self.check_overlap(self.elements[i], self.elements[j]):
                    self.resolve_collision(self.elements[i], self.elements[j])

    def check_overlap(self, element_a, element_b):
        return (element_a.x < element_b.x + element_b.size and
                element_a.x + element_a.size > element_b.x and
                element_a.y < element_b.y + element_b.size and
                element_a.y + element_a.size > element_b.y)

    def resolve_collision(self, element_a, element_b):
        if element_a.element_type == FIRE and element_b.element_type == WATER:
            element_a.change_type(WATER)
        elif element_a.element_type == WATER and element_b.element_type == LEAF:
            element_a.change_type(LEAF)
        elif element_a.element_type == LEAF and element_b.element_type == FIRE:
            element_a.change_type(FIRE)

        if element_b.element_type == FIRE and element_a.element_type == WATER:
            element_b.change_type(WATER)
        elif element_b.element_type == WATER and element_a.element_type == LEAF:
            element_b.change_type(LEAF)
        elif element_b.element_type == LEAF and element_a.element_type == FIRE:
            element_b.change_type(FIRE)

    def check_winner(self):
        types = {element.element_type for element in self.elements}
        if len(types) == 1:
            self.running = False  # Stop the update loop
            winner_type = types.pop().capitalize()
            messagebox.showinfo("Game Over", f"All elements have transformed to {winner_type}! {winner_type} wins!")
            self.root.destroy()  # Close the application after "OK" is clicked

if __name__ == "__main__":
    root = tk.Tk()
    simulation = Simulation(root)
    root.mainloop()
