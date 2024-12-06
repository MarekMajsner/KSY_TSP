import tkinter as tk

HELPTEXT = ""

class Tooltip:
    """Class to create a tooltip for a widget."""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None

        # Bind events to show/hide tooltip
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        """Display the tooltip near the widget."""
        if self.tooltip_window or not self.text:
            return

        # Create a new top-level window for the tooltip
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)  # Remove window borders
        self.tooltip_window.wm_geometry(
            f"+{self.widget.winfo_rootx() + 20}+{self.widget.winfo_rooty() + 20}"
        )  # Position near the widget

        # Add the text label to the tooltip window
        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            background="yellow",
            relief=tk.SOLID,
            borderwidth=1,
            font=("Arial", 10),
        )
        label.pack()

    def hide_tooltip(self, event=None):
        """Hide the tooltip."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


def create_gui():
    """Create a GUI with a button that shows help on hover."""
    root = tk.Tk()
    root.title("Tooltip Example")

    # Create a button
    help_button = tk.Button(root, text="Hover Over Me", font=("Arial", 14))
    help_button.pack(pady=20)

    # Attach a tooltip to the button
    Tooltip(help_button, text="This is a helpful tooltip!")

    root.mainloop()


if __name__ == "__main__":
    create_gui()
