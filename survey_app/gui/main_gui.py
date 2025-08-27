import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import pandas as pd
from survey_app.io.csv_reader import read_survey_csv
from survey_app.io.csv_writer import write_survey_csv


class SurveyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Survey Project Manager")
        self.geometry("430x260")
        self.resizable(False, False)

        tk.Label(self, text="Survey Project Manager", font=("Arial", 16, "bold")).pack(pady=12)

        # Main buttons
        self.init_btn = tk.Button(self, text="Initialize Project", width=25, command=self.init_project)
        self.init_btn.pack(pady=5)

        self.update_btn = tk.Button(self, text="Update Survey", width=25, command=self.update_survey)
        self.update_btn.pack(pady=5)

        self.elev_btn = tk.Button(self, text="Elevation Data", width=25, command=self.elevation_data)
        self.elev_btn.pack(pady=5)

        self.graph_btn = tk.Button(self, text="Graphs", width=25, command=self.graphs)
        self.graph_btn.pack(pady=5)

    def init_project(self):
        # Ask for baseline survey file
        file = filedialog.askopenfilename(
            title="Select Baseline Survey CSV",
            filetypes=[("CSV Files", "*.csv"), ("All files", "*.*")]
        )
        if not file:
            return
        # Ask for output folder
        outdir = filedialog.askdirectory(title="Select Output Folder")
        if not outdir:
            return
        # Project name input
        project_name = simpledialog.askstring("Project Name", "Enter a project name:")
        if not project_name:
            return
        # Try loading csv with reader
        try:
            df = read_survey_csv(file)
            messagebox.showinfo("Project Initialized", f"Loaded {len(df)} baseline records.\n\n(Not saved yet. Add logic here to save new project files.)")
        except Exception as e:
            messagebox.showerror("Error", f"Could not initialize project:\n\n{e}")

    def update_survey(self):
        messagebox.showinfo("Not implemented", "Update Survey logic to be added.")

    def elevation_data(self):
        messagebox.showinfo("Not implemented", "Elevation Data logic to be added.")

    def graphs(self):
        messagebox.showinfo("Not implemented", "Graphing logic to be added.")

def launch():
    app = SurveyApp()
    app.mainloop()

if __name__ == "__main__":
    launch()
