import json
import os
import tkinter as tk
from tkinter.messagebox import showinfo
import time

from scipy.stats import false_discovery_control

from utils.experiment import TSP_experiment, create_test_exp
from datetime import datetime

CANVAS_WIDTH = 332
CANVAS_HEIGHT = 332
RADIUS = 20
class InteractivePointsApp:
    def __init__(self, experiments=None, args = None):
        """

        :param experiments:
        :param args:
        """
        self.data_log = {}
        self.log_data = False
        if not args is None:
            self.log_data = not args.nologs
        self.experiments = experiments

        self.total_num_experiments = len(self.experiments)
        self.experiment_num = 0
        self.current_experiment = self.experiments[self.experiment_num]

        self.radius = RADIUS
        """tkinter window init"""
        self.master = tk.Tk()
        self.master.title("TSP Human benchmark")
        self.canvas = None

        # TODO: ADD INTRO SCREEN WITH DESCRIPTION AND HELP
        self.load_next_experiment()


        """Submit button"""
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
        self.lines = {}
        self.selected_points = []

        # Data logs
        self.current_path_len = 0
        self.optimal_path_len = 0


        # self.optimal_path_len = self.experiments[self.experiment_num].optimal_distance
        # print("AAAAAAAAAAAAAAAAAAAAAAA", self.optimal_path_len)
        self.num_actions = 0

        # Create text widget and specify size.
        # T = tk.Text(self.master, height=5, width=52)
        # T.pack()
        # "DEBUG" LABELS
        self.time_label = tk.Label(self.master, font=("Arial", 16), fg="blue")
        self.time_label.pack(pady=10)
        self.start = time.time()
        self.update_time()
        # Other initializations (e.g., canvas, buttons, etc.)
        self.master.mainloop()


    def update_time(self):
        """Update the time widget with the current time."""
        current_time = datetime.now().strftime("%H:%M:%S")
        end = time.time()
        length = end - self.start

        length = convert_format(length)
        self.time_label.config(text=f"Current Time: {length}")
        # Schedule the next update
        self.master.after(1000, self.update_time)  # Update every 1000ms (1 second)

    def load_next_experiment(self):

        assert self.experiment_num < len(self.experiments)
        self.current_experiment = self.experiments[self.experiment_num]
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


        # Reset data
        self.lines = {}
        self.selected_points = []
        self.start = time.time()


    def log_experiment(self):
        """Save the points from the current path to a JSON file with a time-dependent name."""

        # Extract the points involved in the current path
        path_points = []
        for point_pair in self.lines:
            path_points.append({
                "point1": point_pair[0],
                "point2": point_pair[1]
            })
        end = time.time()
        length = end - self.start
        # Save the path to a JSON file
        exp_data = {
            "path": path_points,
            "time": length
        }
        self.data_log[self.current_experiment.exp_name] = exp_data



    def save_logs(self):
        # Generate a time-dependent filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"Experiment_{timestamp}.json"
        file_name = os.path.join("tests_runs",file_name)
        try:
            with open(file_name, "w") as file:
                json.dump(self.data_log, file, indent=4)
            print(f"Path saved successfully to {file_name}.")
        except Exception as e:
            print(f"Error saving path: {e}")

    def button_clicked(self):
        # TODO: Simple check if all points are used
        self.log_experiment()

        if self.experiment_end():
            showinfo(
                title="Congratulations, the test is now over.",
                message="In Fact, "
                        "You Did So Well I’m Going To Note This On Your File In the Commendations Section. "
                        "Oh, There’s Lots Of Room Here.")
            if self.log_data:
                self.save_logs()
            self.master.destroy()
        else:
            showinfo(
                title="NEXT",
                message="GOOD JOB!!!")
            self.load_next_experiment()


    def experiment_end(self):
        return self.total_num_experiments <= self.experiment_num

    def draw_points(self):
        """Draw points on the canvas and bind click events."""

        points = self.current_experiment.locations

        for point in points:
            x, y = point["x"], point["y"]
            # Draw a small circle to represent the point
            point_id = self.canvas.create_oval(x - self.radius, y - self.radius, x + self.radius, y + self.radius,
                                               outline="black",fill="white",stipple="gray50",
                                               tags=("point"+point["name"]))
            # Store point data as tags
            self.canvas.itemconfig(point_id, tags=("point"+point["name"]))
            # Bind click event
            self.canvas.tag_bind(point_id, "<Button-1>", lambda event, p=point: self.on_point_click(event, p))

    def on_point_click(self, event, point):
        """Handle point click event."""
        if point in self.selected_points:
            self.reset_point_color(point)
            self.selected_points.pop()
            print(f"Deselect on point: {point['name']} at ({point['x']}, {point['y']})")
        else:
            self.selected_points.append(point)
            self.highlight_point(point)
            print(f"Clicked on point: {point['name']} at ({point['x']}, {point['y']})")


        # If two points are selected, either draw or delete a line
        if len(self.selected_points) == 2:
            p1, p2 = self.selected_points
            self.toggle_line_between_points(p1, p2)
            self.selected_points.pop(0)
            self.reset_point_color(p1)
            # self.reset_point_color(p2)

    def on_line_click(self, event, line_id):
        """Handle line click event by deleting the line."""
        self.canvas.delete(line_id)
        # Remove line from `self.lines`
        self.lines = {pair: lid for pair, lid in self.lines.items() if lid != line_id}
        print("Line deleted")

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
            line_id = self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2,dash=(5, 3))
            self.lines[point_pair] = line_id
            print(f"Drew line between {p1['name']} and {p2['name']}")
            self.canvas.tag_bind(line_id, "<Button-1>",
                                 lambda event, l=line_id: self.on_line_click(event, line_id))

    def highlight_point(self, point):
        """Change the color of the selected point to indicate selection."""
        point = self.canvas.find_withtag("point"+point["name"])
        self.canvas.itemconfig(point, fill="blue")  # Change color to green

    def reset_point_color(self,point):
        point = self.canvas.find_withtag("point"+point["name"])
        self.canvas.itemconfig(point, fill="white")

def count_directories(path):
    return len(next(os.walk(path))[1])


def convert_format(sec):
   sec = sec % (24 * 3600)
   hour = sec // 3600
   sec %= 3600
   min = sec // 60
   sec %= 60
   return "%02d:%02d:%02d" % (hour, min, sec)

if __name__ == "__main__":
    path = os.path.split(os.getcwd())[0]
    example_exp = create_test_exp("14",path)

    app = InteractivePointsApp(experiments=[example_exp])

    # TODO: SAY CURRENT VS OPTIMAL DISTANCE
    # TODO: DISTANCE, NUMBER OF ACTIONS
    # TODO: Create intro screen