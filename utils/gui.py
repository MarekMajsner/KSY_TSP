import json
import os
import tkinter as tk
from tkinter.messagebox import showinfo
from utils.experiment import TSP_experiment
from utils.experiment import load_experiments

CANVAS_WIDTH = 332
CANVAS_HEIGHT = 332

class InteractivePointsApp:
    def __init__(self, root, experiments=None, experiment_num=0):
        self.root = root
        self.root.title("TSP Human benchmark")

        # TODO: check for number of experiments in so exp_num is not bigger
        self.experiment_num = experiment_num
        self.experiments = experiments

        assert experiment_num >= 0
        self.load_next_experiment()

        # Text input field
        self.text_input = tk.Entry(root)
        self.text_input.pack(pady=10)
        # Submit button
        submit_button = tk.Button(
            root,
            text='Submit',
            compound=tk.LEFT,
            command=self.button_clicked
        )
        submit_button.pack(
            ipadx=5,
            ipady=5,
            expand=True
        )

        # Store selected points for drawing lines
        self.selected_points = []
        self.lines = {}


        root.mainloop()

    def load_next_experiment(self):

        if isinstance(self.experiments,TSP_experiment):
            self.current_experiment = self.experiments
        else:
            assert self.experiment_num < len(self.current_experiment)
            self.current_experiment = self.experiments[self.experiment_num]

        self.experiment_num += 1

        self.image = tk.PhotoImage(file=self.experiments.image_path)
        width = self.image.width()
        height = self.image.height()
        # Canvas for drawing
        self.canvas = tk.Canvas(root, width=width, height=height, bg="white")
        # self.canvas.pack(anchor=tk.CENTER, expand=True)
        self.canvas.pack()

        self.canvas.create_image(
            (width / 2, height / 2),
            image=self.image
        )
        # Draw points on canvas
        self.draw_points()



    def button_clicked(self):
        # showinfo(
        #     title='Information',
        #     message='Download button clicked!'
        # )
        self.read_text_input()
        if self.experiment_end:
            showinfo(
                title="Congratulations, the test is now over.",
                message="In Fact, "
                        "You Did So Well I’m Going To Note This On Your File In the Commendations Section. "
                        "Oh, There’s Lots Of Room Here." )


    def experiment_end(self):
        return len(self.experiments) == self.experiment_num

    def draw_points(self):
        """Draw points on the canvas and bind click events."""

        points = self.current_experiment.locations
        # print(self.current_experiment.locations)
        for point in points:
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

        # If two points are selected, either draw or delete a line
        if len(self.selected_points) == 2:
            p1, p2 = self.selected_points
            self.toggle_line_between_points(p1, p2)
            self.selected_points.clear()


    def toggle_line_between_points(self, p1, p2):
        """Toggle line between two selected points: draw if not present, delete if present."""
        point_pair = tuple(sorted((p1["name"], p2["name"])))  # Sort to avoid order issues
        if point_pair in self.lines:
            # Line exists; delete it
            self.canvas.delete(self.lines[point_pair])
            del self.lines[point_pair]
            print(f"Deleted line between {p1['name']} and {p2['name']}")
        else:
            # Line does not exist; create it
            x1, y1 = p1["x"], p1["y"]
            x2, y2 = p2["x"], p2["y"]
            line_id = self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2)
            self.lines[point_pair] = line_id
            print(f"Drew line between {p1['name']} and {p2['name']}")

    def read_text_input(self):
        """Reads the text from the input field and prints it."""
        text = self.text_input.get()
        print(f"Text input: {text}")

def count_directories(path):
    return len(next(os.walk(path))[1])

if __name__ == "__main__":
    path = os.path.split(os.getcwd())[0]
    example_exp = TSP_experiment(current_working_dir=path)
    example_exp.create_test_exp()

    root = tk.Tk()
    app = InteractivePointsApp(root,experiments=example_exp)
    root.mainloop()