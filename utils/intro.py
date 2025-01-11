import json
import math
import os
import tkinter as tk
from tkinter.messagebox import showinfo, RETRY
import time
from collections import Counter

from PIL import ImageTk, Image

#from scipy.stats import false_discovery_control

from utils.experiment import TSP_experiment, create_test_exp
from datetime import datetime


def introduction_screen(self):
    """Display the introduction screen."""
    # Create a frame for the introduction
    self.intro_frame = tk.Frame(self.master)
    self.intro_frame.pack(expand=True)

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
            "- Click on points to connect them.\n"
            "- Connect all points to form a valid closed loop.\n"
            "- Press 'Esc' to deselect point or click on the background to clear your selection.\n"
            "- To delete a line click on the line or select the two points it connects.\n"
            "- Submit your solution when you're done."
        ),
        font=("Arial", 14),
        wraplength=600,
        justify=tk.LEFT
    )
    description_label.pack(pady=10)

    # Create a frame for the images
    image_frame = tk.Frame(self.intro_frame)
    image_frame.pack(pady=10)

    # Add the first image
    image1 = Image.open("figs/Valid.png")
    photo1 = ImageTk.PhotoImage(image1)
    label1 = tk.Label(image_frame, image=photo1)
    label1.image = photo1
    label1.pack(side=tk.LEFT)

    # Add the second image
    image2 = Image.open("figs/Invalid.png")
    photo2 = ImageTk.PhotoImage(image2)
    label2 = tk.Label(image_frame, image=photo2)
    label2.image = photo2
    label2.pack(side=tk.LEFT, padx=10)

    # Add a "Start Experiment" button
    start_button = tk.Button(
        self.intro_frame,
        text="Start Experiment",
        font=("Arial", 25),
        bg="green",
        fg="white",
        command=self.start_experiment
    )
    start_button.pack(pady=20)

