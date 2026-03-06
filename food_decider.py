import numpy as np
import tkinter as tk
from tkinter import ttk
from breakfast_tab import Breakfast
from lunch__tab import Lunch
from dinner_tab import Dinner
from dessert_tab import Dessert

class Display:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Decider")

        style = ttk.Style(self.root)
        style.theme_use("winnative")

        self.setup_controls()

    def setup_controls(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.breakfast_frame = ttk.Frame(notebook)
        self.lunch_frame = ttk.Frame(notebook)
        self.dinner_frame = ttk.Frame(notebook)
        self.dessert_frame = ttk.Frame(notebook)

        notebook.add(self.breakfast_frame, text='Breakfast')
        notebook.add(self.lunch_frame, text='Lunch')
        notebook.add(self.dinner_frame, text='Dinner')
        notebook.add(self.dessert_frame, text='Dessert')

        Breakfast(self.breakfast_frame)
        Lunch(self.lunch_frame)
        Dinner(self.dinner_frame)
        Dessert(self.dessert_frame)



if __name__ == "__main__":
    root = tk.Tk()
    app = Display(root)
    root.mainloop() 

    