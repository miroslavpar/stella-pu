import tkinter as tk
from tkinter import ttk, Toplevel, Label, Entry, Text, Button, messagebox
from controllers.simulation import run_simulation
from controllers.plotter import plot_results
from PIL import Image, ImageTk
import os
import matplotlib.pyplot as plt

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("ЕкоСистема Симулация")

        self.create_toolbar()

    def create_toolbar(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        start_button = ttk.Button(toolbar, text="Start Simulation", command=self.open_simulation_settings)
        start_button.pack(side=tk.LEFT)

        about_button = ttk.Button(toolbar, text="About", command=self.show_about)
        about_button.pack(side=tk.LEFT)

        show_table_button = ttk.Button(toolbar, text="Show Results Table", command=self.show_results_table)
        show_table_button.pack(side=tk.LEFT)

    def open_simulation_settings(self):
        self.settings_window = Toplevel(self.root)
        self.settings_window.title("Simulation Settings")

        Label(self.settings_window, text="Simulation Period (years):").grid(row=0, column=0, padx=10, pady=5)
        self.simulation_period_entry = Entry(self.settings_window)
        self.simulation_period_entry.insert(tk.END, "12")
        self.simulation_period_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(self.settings_window, text="Participants:").grid(row=1, column=0, padx=10, pady=5)
        self.participants_text = Text(self.settings_window, height=5, width=40)
        self.participants_text.insert(tk.END, "Zayci=1000\nLisici=50")
        self.participants_text.grid(row=1, column=1, padx=10, pady=5)

        Label(self.settings_window, text="Equations (one per line):").grid(row=2, column=0, padx=10, pady=5)
        self.equations_text = Text(self.settings_window, height=5, width=40)
        self.equations_text.insert(tk.END, "Zayci'=Zayci*100/100 - (Zayci*10/100 + Lisici*12)\nLisici'=Lisici*30/100 - Lisici*5/100")
        self.equations_text.grid(row=2, column=1, padx=10, pady=5)

        start_button = Button(self.settings_window, text="Run Simulation", command=self.run_simulation)
        start_button.grid(row=3, column=0, columnspan=2, pady=10)

        help_button = Button(self.settings_window, text="Help", command=self.show_help_in_settings)
        help_button.grid(row=4, column=0, columnspan=2, pady=10)

    def run_simulation(self):
        try:
            simulation_period = int(self.simulation_period_entry.get())
            if simulation_period <= 0:
                messagebox.showerror("Error", "Simulation Period must be greater than 0.")
                return
        except ValueError:
            messagebox.showerror("Error", "Simulation Period must be a valid integer.")
            return

        participants_data = self.participants_text.get("1.0", tk.END).strip().split("\n")
        equations = self.equations_text.get("1.0", tk.END).strip().split("\n")

        participants = {}
        for line in participants_data:
            try:
                name, initial_value = line.split("=")
                participants[name.strip()] = int(initial_value.strip())
            except ValueError:
                messagebox.showerror("Error", f"Participant '{line}' is missing a value. Use format 'Name=Value'.")
                return

        try:
            self.results = run_simulation(participants, equations, simulation_period)
            self.show_results_table()
            self.show_graph()
        except ZeroDivisionError:
            messagebox.showerror("Error", "Division by zero encountered in equations.")
        except KeyError as e:
            missing_var = str(e).strip("'")
            messagebox.showerror("Error", f"Undefined participant '{missing_var}' in equations.")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

    def show_results_table(self):
        if not hasattr(self, 'results') or not self.results:
            messagebox.showerror("Error", "No results to show. Please run the simulation first.")
            return

        table_window = Toplevel(self.root)
        table_window.title("Simulation Results")

        tree = ttk.Treeview(table_window)
        tree["columns"] = ("Year",) + tuple(self.results.keys())

        tree.column("#0", width=100, minwidth=100, anchor="w")
        for participant in self.results.keys():
            tree.column(participant, width=100, minwidth=100, anchor="w")

        tree.heading("#0", text="Year", anchor="w")
        for participant in self.results.keys():
            tree.heading(participant, text=participant, anchor="w")

        first_key = list(self.results.keys())[0]
        for year, data in enumerate(self.results[first_key]):
            tree.insert("", "end", text=str(year+1), values=(data,) + tuple(self.results[participant][year] for participant in self.results.keys()))

        tree.pack(padx=10, pady=10)

    def show_graph(self):
        if not hasattr(self, 'results') or not self.results:
            messagebox.showerror("Error", "No results to plot. Please run the simulation first.")
            return

        plt.figure(figsize=(10, 6))

        for participant, values in self.results.items():
            plt.plot(range(1, len(values)+1), values, label=participant)

        plt.title("Simulation Results")
        plt.xlabel("Years")
        plt.ylabel("Population")
        plt.legend()
        plt.grid(True)

        plt.show()

    def show_about(self):
        about_window = Toplevel(self.root)
        about_window.title("About")

        name_label = Label(about_window, text="Име: Мирослав Николаев Парапанов", font=("Arial", 14))
        name_label.pack(pady=5)

        faculty_number_label = Label(about_window, text="Факултетен номер: 2401262049", font=("Arial", 14))
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
            error_label = Label(about_window, text="Снимката не може да бъде заредена.", font=("Arial", 12), fg="red")
            error_label.pack(pady=10)

    def show_help_in_settings(self):
        help_text = (
            "Simulation Period (years):\n"
            "This defines the number of years for the simulation to run. Must be a positive integer.\n\n"
            "Participants:\n"
            "Defines the entities in the model, with their initial values. Use the format 'Name=Value', one participant per line.\n"
            "Example:\nZayci=1000\nLisici=50\n\n"
            "Equations:\n"
            "Defines how each participant changes over time. Each equation should be on a separate line and use existing participants.\n"
            "Example:\nZayci'=Zayci*100/100 - (Zayci*10/100 + Lisici*12)"
        )

        help_window = Toplevel(self.settings_window)
        help_window.title("Help")

        help_label = Label(help_window, text=help_text, justify="left", padx=10, pady=10, wraplength=400)
        help_label.pack()
