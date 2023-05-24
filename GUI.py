import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import random
from Visual_grid import visuel_grid
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class GUI(tk.Tk):
    def __init__(self):
        #main set up
        super().__init__()
        self.title('KITT GUI')
        self.minsize(400,400)

        # widgets

        # Create a FigureCanvasTkAgg object to display the plot
        canvas = FigureCanvasTkAgg(visuel_grid(), master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

        #run
        self.mainloop()


GUI()
