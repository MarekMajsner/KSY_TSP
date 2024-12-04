import json
import math
import os
import tkinter as tk
from tkinter.messagebox import showinfo, RETRY
import time
from collections import Counter

from PIL import ImageTk, Image

from scipy.stats import false_discovery_control

from utils.experiment import TSP_experiment, create_test_exp
from datetime import datetime


def introduction_screen(self):
    """Display the introduction screen."""
    # Create a frame for the introduction
    self.intro_frame = tk.Frame(self.master)
    self.intro_frame.pack(fill=tk.BOTH, expand=True)

    # Add an introduction label
    intro_label = tk.Label(
        self.intro_frame,
        text="Welcome to the TSP Human Benchmark!",
        font=("Arial", 20),
        fg="blue",
        wraplength=600
    )
    intro_label.pack(pady=20)

    # Add a description or instructions
    description_label = tk.Label(
        self.intro_frame,
        text=(
            "In this experiment, you'll solve a series of Traveling Salesman Problems (TSP) by "
            "connecting points on the canvas. \n\n"
            "Instructions:\n"
            "- Click on points to select them.\n"
            "- Connect all points to form a valid closed loop.\n"
            "- Submit your solution when you're done.\n"
            "- Press 'Esc' to deselect all points or click on the background to clear your selection."
        ),
        font=("Arial", 14),
        wraplength=600,
        justify=tk.LEFT
    )
    description_label.pack(pady=10)

    # Add a "Start Experiment" button
    start_button = tk.Button(
        self.intro_frame,
        text="Start Experiment",
        font=("Arial", 16),
        bg="green",
        fg="white",
        command=self.start_experiment
    )
    start_button.pack(pady=20)
    show_valid_solution(self)

def show_valid_solution(self):
    image = Image.open("utils/6_1.png")
    photo = ImageTk.PhotoImage(image)

    label = tk.Label(image=photo, bg='green')
    label.image = photo
    label.pack()

def show_invalid_solution(self):
    print(FAKEEEE)