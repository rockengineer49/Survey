import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import pandas as pd
from survey_app.io.csv_reader import read_survey_csv
from survey_app.io.csv_writer import write_survey_csv
from survey_app.io.downhole_loader import load_downhole_csv_for_merge
from survey_app.processing.merge import merge_downhole_to_baseline


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
            from survey_app.io.csv_writer import write_survey_csv
            try:
                output_path = write_survey_csv(df, project_name, outdir, status="Baseline")
                messagebox.showinfo(
                    "Project Initialized",
                    f"Baseline written to:\n{output_path}\n\nRecords: {len(df)}"
         )
            except Exception as e:
                messagebox.showerror("Write error", f"Could not save survey file:\n\n{e}")

        except Exception as e:
            messagebox.showerror("Error", f"Could not initialize project:\n\n{e}")

    def update_survey_dialog():
        root = tk.Tk()
        root.withdraw()  # Hide the main window

    # Prompt the user with three choices
        survey_type = simpledialog.askstring(
            "Update Survey",
            "Choose data to update:\n- survey\n- downhole\n- both"
        )

        if survey_type is None:
            return  # User canceled dialog

        survey_type = survey_type.lower().strip()
        if survey_type not in ['survey', 'downhole', 'both']:
            messagebox.showerror("Error", "Please type: survey, downhole, or both")
            return

    # Now, survey_type is one of 'survey', 'downhole', 'both'
    # Use this to drive your file selection & merge logic
    # if survey_type == 'survey': ... (ask for top of pipe file)
    # if survey_type == 'downhole': ... (ask for downhole file)
    # if survey_type == 'both': ... (ask for both files)


    # 2. Pick downhole data
        downhole_file = filedialog.askopenfilename(
            title="Select Downhole CSV",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not downhole_file:
            return
        try:
            downhole_df = load_downhole_csv_for_merge(downhole_file)
        except Exception as e:
            messagebox.showerror("Downhole Error", f"Could not read downhole file:\n{e}")
            return
        if downhole_df.empty:
            messagebox.showwarning("No Downhole Data", "No valid downhole records found in this file.")
            return

    # 3. Merge
        try:
            merged_df, changelog = merge_downhole_to_baseline(baseline_df, downhole_df)
        except Exception as e:
            messagebox.showerror("Merge Error", f"Could not merge files:\n{e}")
            return

    # 4. Save merged survey
        save_file = filedialog.asksaveasfilename(
            title="Save Updated Survey CSV",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not save_file:
            return
        try:
            merged_df.to_csv(save_file, index=False)
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not write output file:\n{e}")
            return

    # 5. Report summary (you can customize to reflect actual fields from changelog)
        messagebox.showinfo(
            "Survey Updated",
            f"Survey updated and saved:\n{save_file}\n\n"
            f"Updated Holes: {changelog.get('updated_holes', 'N/A')}\n"
            f"Added Downhole: {changelog.get('added_holes', 'N/A')}\n"
            f"Conflicts: {changelog.get('conflicts', 'N/A')}\n"
            f"Detail: {changelog.get('msg', 'No conflicts')}"
        )
    def update_survey(self):
        import tkinter as tk

        win = tk.Toplevel(self)
        win.title("Select Update Type")
        val = tk.StringVar(value="survey")

        options = [("Survey (Top of Pipe Only)", "survey"),
                   ("Downhole Only", "downhole"),
                   ("Both", "both")]
        for text, mode in options:
            tk.Radiobutton(win, text=text, variable=val, value=mode).pack(anchor='w')
        tk.Button(win, text="OK", command=win.destroy).pack()
        win.wait_window()
        choice = val.get()
        tk.Message(self, text=f"You selected: {choice}").pack()
    # proceed with file dialogs/merge logic based on 'choice'



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
