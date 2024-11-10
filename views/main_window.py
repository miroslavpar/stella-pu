import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel, Label
from controllers.simulation import simulate_population
from controllers.plotter import plot_results
from PIL import Image, ImageTk
import os

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("ЕкоСистема Симулация")

        self.create_toolbar()

    def create_toolbar(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        start_button = ttk.Button(toolbar, text="Start Simulation", command=self.start_simulation)
        start_button.pack(side=tk.LEFT)

        about_me = ttk.Button(toolbar, text="About", command=self.about_me)
        about_me.pack(side=tk.LEFT)

    def start_simulation(self):
            results = simulate_population()
            plot_results(results)

    def about_me(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About")

        name_label = tk.Label(about_window, text="Име: Мирослав Николаев Парапанов", font=("Arial", 14))
        name_label.pack(pady=5)

        faculty_number_label = tk.Label(about_window, text="Факултетен номер: 2401262049", font=("Arial", 14))
        faculty_number_label.pack(pady=5)
        image_path = os.path.join(os.getcwd(), "images", "image.jpg")

        try:
            image = Image.open(image_path)
            image = image.resize((100, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            image_label = Label(about_window, image=photo)
            image_label.image = photo
            image_label.pack(pady=10)
        except Exception as e:
            print(e)
            error_label = Label(about_window, text="Снимката не може да бъде заредена.", font=("Arial", 12), fg="red")
            error_label.pack(pady=10)
