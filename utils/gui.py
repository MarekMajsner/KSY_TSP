import json
import math
import os
import tkinter as tk
from tkinter.messagebox import showinfo, RETRY
import time
from collections import Counter

from scipy.stats import false_discovery_control

from utils.experiment import TSP_experiment, create_test_exp
from datetime import datetime

RADIUS = 20
DECIMALS = 0
LINE_WIDTH = 5
SELECT_COLOR = 'red'
class InteractivePointsApp:
    def __init__(self, experiments=None, args = None):
        """

        :param experiments:
        :param args:
        """
        self.args = args
        self.num_actions = None
        self.optimal_path_len = None
        self.current_path_len = None
        self.selected_points = None
        self.image = None
        self.lines = None
        self.data_log = {}
        self.log_data = False
        if not args is None:
            self.log_data = not args.nologs
        self.experiments = experiments
        self.intro_frame = None
        self.optimize = False

        self.total_num_experiments = len(self.experiments)
        self.experiment_num = 0
        self.current_experiment = self.experiments[self.experiment_num]

        self.radius = RADIUS

        """tkinter window init"""
        self.master = tk.Tk()
        self.master.title("TSP Human benchmark")
        self.canvas = None

        from utils.intro import introduction_screen
        if not args.debug:
            introduction_screen(self)
            print("LOADING INTRO")
            self.master.mainloop()
        else:
            self.start_experiment()


    def update_len(self):
        """Update the widget with the current length."""
        # Floating point -0 work around
        if self.current_path_len<0:
            self.current_path_len = 0

        self.current_len_label.config(text=f"Length: {self.current_path_len:.{DECIMALS}f} Optimal: {self.optimal_path_len:.{DECIMALS}f}"
)
        # Schedule the next update
        self.master.after(100, self.update_len)  # Update every 1000ms (1 second)

    def update_time(self):
        """Update the time widget with the current time."""
        current_time = datetime.now().strftime("%H:%M:%S")
        end = time.time()
        length = end - self.start

        length = convert_format(length)
        self.time_label.config(text=f"Current Time: {length}")
        # Schedule the next update
        self.master.after(1000, self.update_time)  # Update every 1000ms (1 second)

    def clear_all(self):
        """Clear all lines and reset the state."""
        # Reset all points' colors
        for point in self.current_experiment.locations:
            self.reset_point_color(point)

        # Remove all lines from the canvas
        for line_id in self.lines.values():
            self.canvas.delete(line_id)

        # Reset the state variables
        self.selected_points = []
        self.lines = {}
        self.current_path_len = 0
        self.num_actions = 0

        print("Cleared all lines and selections.")
        self.update_len()

    def start_experiment(self):
        """Start the experiment by removing the introduction screen."""

        # Destroy the introduction frame
        if not self.intro_frame is None:
            self.intro_frame.destroy()



        """ESC to deselect bind"""
        self.master.bind("<Escape>", self.clear_selection)

        self.reset_data()

        """PROBLEM NAME LABEL"""
        self.name_label = tk.Label(self.master, font=("Arial", 20), fg="blue",wraplength=600)
        self.name_label.pack(pady=5)

        """DEBUG FRAME"""
        self.debug_frame = tk.Frame(self.master)
        self.debug_frame.pack(expand=True)
        """CURRENT LEN LABEL"""
        self.current_len_label = tk.Label(self.debug_frame, font=("Arial", 16))
        self.current_len_label.pack(pady=5)
        self.update_len()

        """TIME LABEL"""
        self.time_label = tk.Label(self.debug_frame, font=("Arial", 16))
        self.time_label.pack(pady=5)
        self.start = time.time()
        self.update_time()
        self.load_next_experiment()



        # self.name_label.config(text=f"Problem name: {self.current_experiment.exp_name}")

        """Clear All button"""
        self.clear_all_button = tk.Button(
            self.master,
            text="Clear All",
            compound=tk.LEFT,
            bg="red",
            fg="white",
            font=("Arial", 16),
            command=self.clear_all
        )
        self.clear_all_button.pack(padx=5, pady=5, expand=False, side = "top")

        """Submit button"""
        self.submit_button = tk.Button(
            self.master,
            bg="green",
            fg="white",
            text='Submit',
            font=("Arial", 16),
            compound=tk.LEFT,
            command=self.submit_button_clicked
        )
        self.submit_button.pack(
            padx=5,
            pady=5,
            expand=False,
            side = "top"
        )

        # Other initializations (e.g., canvas, buttons, etc.)
        if self.intro_frame is None:
            self.master.mainloop()



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
            self.canvas.pack(expand=False,padx = 100)
            self.canvas.bind("<Button-1>", self.clear_selection_on_background)
            # self.name_label.config(text=f"Problem name: {self.current_experiment.exp_name}")
        else:
            # self.name_label.config(text=f"Problem name: {self.current_experiment.exp_name}, {}")
            self.canvas.delete("all")
            # Canvas for drawing
            self.canvas.config(width=width,height=height)
            # self.canvas.width = width
            # self.canvas.height = height

                           # (self.root, width=width, height=height, bg="white"))
            self.canvas.pack(expand=False,padx = 100)
            # self.canvas.pack()
        self.name_label.config(text=f"Problem name: {self.current_experiment.exp_name}  {self.experiment_num}/{len(self.experiments)}")
        self.canvas.create_image(
            (width / 2, height / 2),
            image=self.image,
            tag="image"
        )
        self.canvas.tag_bind("image", "<Button-1>", self.clear_selection())

        # Draw points on canvas
        self.draw_points()

        self.reset_data()

        showinfo(
            title="Instructions!!!",
            message="First connect the points as fast as possible with the shortest path you can find."
                    "Then you will be granted time to optimize.")
        self.start = time.time()  # reset time for proper start



    def reset_data(self):
        # TODO: FIX RESET ADD CLEAR INSTEAD OF NEW LIST AND DICT INIT
        self.lines = {}
        self.selected_points = []
        self.update_log_values()

    def update_log_values(self):
        self.start = time.time()
        # Data logs
        self.current_path_len = 0
        self.optimal_path_len = self.current_experiment.optimal_distance
        self.num_actions = 0

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
        measured_time = end - self.start
        # Save the path to a JSON file
        exp_data = {
            "path": path_points,
            "time": measured_time,
            "path_len": self.current_path_len,
            "opt_len": self.optimal_path_len,
            "num_action": self.num_actions
        }
        self.data_log[self.current_experiment.exp_name] = exp_data

    def clear_selection_on_background(self, event):
        """Clear selection if the background is clicked."""
        # Check if the click is on a point
        clicked_items = self.canvas.find_withtag("current")
        if not any('point' in self.canvas.gettags(item)[0] for item in clicked_items):
            self.clear_selection()
            print("Cleared selection on background click.")

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

    def check_path_valid(self):
        """
        Checks if all points are used and then if all points are used twice meaning a valid path is formed
        :return:
        """

        path_points = []
        for point_pair in self.lines:
            path_points.append(point_pair[0])
            path_points.append(point_pair[1])
        counts = Counter(path_points)
        if len(counts) != self.current_experiment.num_locations:
            return False
        for point in path_points:
            if counts[point] !=2:
                return False
        return True

    def submit_button_clicked(self):
        path_is_valid = True
        if not self.args.debug:
            path_is_valid = self.check_path_valid()

        if path_is_valid:
            self.debug_frame.pack_forget()
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
                if not self.args.debug:
                    if self.optimize:
                        self.optimize = False
                        self.load_next_experiment()
                        self.debug_frame.pack_forget()
                        # self.clear_all_button.pack(padx=5, pady=5, expand=False, side="bottom")
                        # self.submit_button.pack(padx=5, pady=5, expand=False, side="bottom")
                    else:
                        if self.current_path_len <= self.optimal_path_len:
                            showinfo(
                                title="NEXT",
                                message="GOOD JOB!!! Your path was optimal")
                        else:
                            # Second stage of each experiment using iteration planning
                            showinfo(
                                title="OPTIMIZE??",
                                message=f"GOOD JOB!!! "
                                        f"Length: {self.current_path_len:.{DECIMALS}f} Optimal: {self.optimal_path_len:.{DECIMALS}f}")
                            self.optimize = True
                            self.current_experiment.exp_name = self.current_experiment.exp_name + "OPTIMIZE"
                            # self.load_next_experiment()
                            self.debug_frame.pack()
                            self.clear_all_button.pack(padx=5, pady=5, expand=False, side="bottom")
                            self.submit_button.pack(padx=5, pady=5, expand=False, side="bottom")



        else:
            showinfo(
                title="INVALID PATH",
                message="Please, check your path is closed loop connecting all points")

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
            self.num_actions += 1
            p1, p2 = self.selected_points
            self.toggle_line_between_points(p1, p2)
            self.selected_points.pop(0)
            self.reset_point_color(p1)
            # self.reset_point_color(p2)

    def on_line_click(self, event, line_id):
        """Handle line click event by deleting the line."""
        self.num_actions += 1
        self.canvas.delete(line_id)

        # print(line_id)
        points_pari = list((pair, lid) for pair, lid in self.lines.items() if lid == line_id)
        points_pari = points_pari[0]
        p1 = self.current_experiment.named_locations[points_pari[0][0]]
        p2 = self.current_experiment.named_locations[points_pari[0][1]]
        line_len = math.dist([p1[0], p1[1]], [p2[0], p2[1]])
        # self.canvas.find_withtag("point"+point["name"])
        # Remove line from `self.lines`
        del self.lines[points_pari[0]]
        self.current_path_len -= line_len

    def toggle_line_between_points(self, p1, p2):
        """Toggle line between two selected points: draw if not present, delete if present."""
        point_pair = tuple(sorted((p1["name"], p2["name"])))  # Sort to avoid order issues

        line_len = math.dist([p1["x"], p1["y"]],[p2["x"], p2["y"]])

        if point_pair in self.lines:
            # Line exists; delete it
            self.canvas.delete(self.lines[point_pair])
            del self.lines[point_pair]
            print(f"Deleted line between {p1['name']} and {p2['name']}")
            self.current_path_len -= line_len
        else:
            # Line does not exist; create it
            x1, y1 = p1["x"], p1["y"]
            x2, y2 = p2["x"], p2["y"]
            line_id = self.canvas.create_line(x1, y1, x2, y2, fill="red", width=LINE_WIDTH,dash=(5, 3))
            self.canvas.tag_lower(line_id)
            self.canvas.tag_lower("image")
            self.lines[point_pair] = line_id
            print(f"Drew line between {p1['name']} and {p2['name']}")
            self.canvas.tag_bind(line_id, "<Button-1>",
                                 lambda event, l=line_id: self.on_line_click(event, line_id))
            # ADD Lenght
            self.current_path_len += line_len

    def highlight_point(self, point):
        """Change the color of the selected point to indicate selection."""
        point = self.canvas.find_withtag("point"+point["name"])
        self.canvas.itemconfig(point, fill=SELECT_COLOR)  # Change color to green
        self.canvas.itemconfig(point, stipple="")

    def reset_point_color(self,point):
        point = self.canvas.find_withtag("point"+point["name"])
        self.canvas.itemconfig(point, fill="white",stipple="gray50")

    def clear_selection(self, event=None):
        """Clear all selected points."""
        if self.selected_points:
            for point in self.selected_points:
                self.reset_point_color(point)
            self.selected_points = []
            print("Selection cleared.")


def count_directories(path):
    return len(next(os.walk(path))[1])


def convert_format(sec):
   sec = sec % (24 * 3600)
   hour = sec // 3600
   sec %= 3600
   minutes = sec // 60
   sec %= 60
   return "%02d:%02d:%02d" % (hour, minutes, sec)

if __name__ == "__main__":
    path = os.path.split(os.getcwd())[0]
    example_exp = create_test_exp("14",path)

    app = InteractivePointsApp(experiments=[example_exp])

    # TODO: ADD INFO THAT NUMBERS ON IMAGES HAVE NO MEANING
    # TODO: HIDE DEBUG INFO

    # TODO: FIRST SELECT TO SHOW OPTIMAL PATH
    # TODO: ON SUBMIT GOOD JOB OR ALLOW TO OPTIMIZE
    # TODO: LOG THE DIFFERENT PATHS
