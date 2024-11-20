import json
import os
import tkinter as tk
from tkinter.messagebox import showinfo
from utils.experiment import TSP_experiment, create_test_exp
from utils.experiment import load_experiments
from sys import platform

CANVAS_WIDTH = 332
CANVAS_HEIGHT = 332
RADIUS = 20
class InteractivePointsApp:
    def __init__(self, experiments=None, experiment_num=0, args = None):
        # Window init
        self.master = tk.Tk()
        self.master.title("TSP Human benchmark")
        self.canvas = None

        # if platform == "linux" or platform == "linux2":
        #     self.master.overrideredirect(True)
        #     self.master.wait_visibility(self.master)
        #     self.master.wm_attributes("-alpha", 0.5)

        # self.master.wm_attributes("-transparentcolor", "white")

        # TODO: check for number of experiments in so exp_num is not bigger
        self.experiment_num = experiment_num
        self.experiments = experiments

        assert experiment_num >= 0
        self.load_next_experiment()

        # Text input field
        # self.text_input = tk.Entry(self.master)
        # self.text_input.pack(pady=10)
        # Submit button
        submit_button = tk.Button(
            self.master,
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

        # Data logs
        self.current_path_len = 0
        self.optimal_path_len = 0


        self.master.mainloop()

    def load_next_experiment(self):
        print("LOAD NEXT")
        if isinstance(self.experiments,TSP_experiment):
            self.current_experiment = self.experiments
        else:
            assert self.experiment_num < len(self.experiments)
            self.current_experiment = self.experiments[self.experiment_num]
        # print(self.current_experiment.image_path)
        self.experiment_num += 1

        self.image = tk.PhotoImage(file=self.current_experiment.image_path_exp)
        width = self.image.width()
        height = self.image.height()
        if self.canvas is None:
            # Canvas for drawing
            self.canvas = tk.Canvas(self.master, width=width, height=height, bg="white")
            self.canvas.pack(anchor=tk.CENTER, expand=True)
        else:
            self.canvas.delete("all")
            # Canvas for drawing
            self.canvas.width = width

                           # (self.root, width=width, height=height, bg="white"))
            self.canvas.pack(anchor=tk.CENTER, expand=True)
            # self.canvas.pack()

        self.canvas.create_image(
            (width / 2, height / 2),
            image=self.image
        )
        # Draw points on canvas
        self.draw_points()

    def button_clicked(self):
        self.read_text_input()

        if self.experiment_end():
            showinfo(
                title="Congratulations, the test is now over.",
                message="In Fact, "
                        "You Did So Well I’m Going To Note This On Your File In the Commendations Section. "
                        "Oh, There’s Lots Of Room Here." )
            self.root.destroy()
        else:
            showinfo(
                title="NEXT",
                message="GOOD JOB!!!")
            self.load_next_experiment()


    def experiment_end(self):
        return len(self.experiments) == self.experiment_num

    def draw_points(self):
        """Draw points on the canvas and bind click events."""

        points = self.current_experiment.locations
        # print(self.current_experiment.locations)
        for point in points:
            x, y = point["x"], point["y"]
            # Draw a small circle to represent the point
            point_id = self.canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS,
                                               outline="black",fill="white",stipple="gray50")
            # Store point data as tags
            self.canvas.itemconfig(point_id, tags=("point"+point["name"],))
            # self.canvas.itemconfig(point_id,"-alpha",0.5)
            # print(point_id)
            # Bind click event
            self.canvas.tag_bind(point_id, "<Button-1>", lambda event, p=point: self.on_point_click(event, p))

    def on_point_click(self, event, point):
        """Handle point click event."""
        print(f"Clicked on point: {point['name']} at ({point['x']}, {point['y']})")
        self.selected_points.append(point)
        self.highlight_point(point)
        # ADD DESELECT HANDLE

        # If two points are selected, either draw or delete a line
        if len(self.selected_points) == 2:
            p1, p2 = self.selected_points
            self.toggle_line_between_points(p1, p2)
            self.selected_points.clear()
            self.reset_point_colors(p1, p2)


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

    def highlight_point(self, point):
        """Change the color of the selected point to indicate selection."""
        print(point["name"])
        point = self.canvas.find_withtag(point["name"])
        self.canvas.itemconfig(point, fill="green")  # Change color to green

    def reset_point_colors(self,point1,point2):
        point = self.canvas.find_withtag(point1["name"])
        self.canvas.itemconfig(point, fill="blue")

        point = self.canvas.find_withtag(point2["name"])
        self.canvas.itemconfig(point, fill="blue")

    def read_text_input(self):
        """Reads the text from the input field and prints it."""
        text = self.text_input.get()
        print(f"Text input: {text}")

def count_directories(path):
    return len(next(os.walk(path))[1])

def run_gui(experiments):
    root = tk.Tk()
    app = InteractivePointsApp(root, experiments=experiments)
    root.mainloop()

if __name__ == "__main__":
    path = os.path.split(os.getcwd())[0]
    example_exp = create_test_exp("14")

    app = InteractivePointsApp(experiments=example_exp)
    # app.root.mainloop()

    # TODO: SAY CURRENT VS OPTIMAL DISTANCE
    # GIVE AI CHANCE TO FIX
    # TODO: DISTANCE, PORADI BODY, CAS, NUMBER OF ACTIONS
    # Create strat screen for final experiment

    # OTAZKY DAN
    # JAK KOLIK PIXELU JE BORDER JE vzdy stejna