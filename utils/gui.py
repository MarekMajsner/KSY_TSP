import json
import os
import tkinter as tk
from utils.experiment import TSP_experiment
from utils.experiment import load_experiments

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

class InteractivePointsApp:
    def __init__(self, root, experiments=None):
        self.root = root
        self.root.title("Interactive Points")

        self.experiments = experiments

        width = CANVAS_WIDTH
        height = CANVAS_HEIGHT
        # Canvas for drawing
        self.canvas = tk.Canvas(root, width=width, height=height, bg="white")
        # self.canvas.pack(anchor=tk.CENTER, expand=True)
        self.canvas.pack()

        python_image = tk.PhotoImage(file=self.experiments.image_path)
        self.canvas.create_image(
            (100, 100),
            image=python_image
        )

        root.mainloop()

        self.experiment_num = 0

        # Store selected points for drawing lines
        self.selected_points = []

        # Draw points on canvas
        self.draw_points()


    def draw_points(self):
        """Draw points on the canvas and bind click events."""
        for point in self.points:
            x, y = point["x"], point["y"]
            # Draw a small circle to represent the point
            point_id = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue", outline="black")
            # Store point data as tags
            self.canvas.itemconfig(point_id, tags=(point["name"],))
            # Bind click event
            self.canvas.tag_bind(point_id, "<Button-1>", lambda event, p=point: self.on_point_click(event, p))

    def on_point_click(self, event, point):
        """Handle point click event."""
        print(f"Clicked on point: {point['name']} at ({point['x']}, {point['y']})")
        self.selected_points.append(point)

        # If two points are selected, draw a line
        if len(self.selected_points) == 2:
            self.draw_line_between_points()
            self.selected_points.clear()

    def draw_line_between_points(self):
        """Draw a line between two selected points."""
        p1, p2 = self.selected_points
        x1, y1 = p1["x"], p1["y"]
        x2, y2 = p2["x"], p2["y"]
        self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2)
        print(f"Drew line between {p1['name']} and {p2['name']}")


if __name__ == "__main__":
    path = os.path.split(os.getcwd())[0]
    example_exp = TSP_experiment(current_working_dir=path)
    example_exp.create_test_exp()

    root = tk.Tk()
    app = InteractivePointsApp(root,experiments=example_exp)
    root.mainloop()
