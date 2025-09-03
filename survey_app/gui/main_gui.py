import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import pandas as pd
import os
import glob
from datetime import datetime
from survey_app.processing.merge import merge_surveys

# --- Helper: type selection dialog ---
def pick_update_type(parent):
    result = {}
    win = tk.Toplevel(parent)
    win.title("Select Update Type")
    var = tk.StringVar(value="survey")
    
    tk.Label(win, text="Which data would you like to update?").pack(anchor='w', padx=10, pady=10)
    opts = [
        ("Survey (Top of Pipe Only)", "survey"),
        ("Downhole Only", "downhole"),
        ("Both", "both")
    ]
    for text, val in opts:
        tk.Radiobutton(win, text=text, variable=var, value=val).pack(anchor='w', padx=20)
    def on_ok():
        result['choice'] = var.get()
        win.grab_release()
        win.destroy()
    win.protocol("WM_DELETE_WINDOW", on_ok)
    tk.Button(win, text="OK", command=on_ok).pack(pady=10)
    win.grab_set()
    parent.wait_window(win)
    return result.get('choice')

class SurveyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Survey Project Manager")
        self.geometry("430x260")
        self.resizable(False, False)
        tk.Label(self, text="Survey Project Manager", font=("Arial", 16, "bold")).pack(pady=12)

        tk.Button(self, text="Initialize Project", width=25, command=self.init_project).pack(pady=5)
        tk.Button(self, text="Update Survey", width=25, command=self.update_survey).pack(pady=5)
        tk.Button(self, text="Elevation Data", width=25, command=self.elevation_data).pack(pady=5)
        tk.Button(self, text="Graphs", width=25, command=self.graphs).pack(pady=5)

    def init_project(self):
        file = filedialog.askopenfilename(
            title="Select Baseline Survey CSV",
            filetypes=[("CSV Files", "*.csv"), ("All files", "*.*")]
        )
        if not file:
            return
        outdir = filedialog.askdirectory(title="Select Output Folder")
        if not outdir:
            return
        project_name = simpledialog.askstring("Project Name", "Enter a project name:")
        if not project_name:
            return
        try:
            df = pd.read_csv(file)
            # Simplified default: just write to standard file
            today_str = datetime.now().strftime("%Y.%m.%d")
            outpath = os.path.join(outdir, f"{today_str}_{project_name}_Survey.csv")
            df['Status'] = 'Baseline'
            df.to_csv(outpath, index=False)
            messagebox.showinfo(
                "Project Initialized",
                f"Baseline written to:\n{outpath}\n\nRecords: {len(df)}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Could not initialize project:\n\n{e}")

    def update_survey(self):
        choice = pick_update_type(self)
        if not choice:
            return  # Dialog cancelled
        # 1. Project directory
        project_dir = filedialog.askdirectory(title="Select Project Folder")
        if not project_dir:
            return

        # 2. Find latest baseline survey csv
        survey_files = glob.glob(os.path.join(project_dir, '*_Survey.csv'))
        if not survey_files:
            messagebox.showerror("Error", "No baseline survey file found. Please initialize project first.")
            return
        baseline_file = sorted(survey_files)[-1]
        try:
            baseline_df = pd.read_csv(baseline_file)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read baseline survey CSV:\n{e}")
            return

        # 3. Get input files based on update type
        top_df, downhole_df = None, None
        if choice in ("survey", "both"):
            top_file = filedialog.askopenfilename(
                title="Select Top of Pipe Survey CSV",
                filetypes=[("CSV", "*.csv")])
            if not top_file:
                return
            try:
                top_df = pd.read_csv(top_file)
            except Exception as e:
                messagebox.showerror("Error", f"Could not read Top of Pipe CSV:\n{e}")
                return
        if choice in ("downhole", "both"):
            downhole_file = filedialog.askopenfilename(
                title="Select Downhole Survey CSV",
                filetypes=[("CSV", "*.csv")])
            if not downhole_file:
                return
            try:
                downhole_df = pd.read_csv(downhole_file)
            except Exception as e:
                messagebox.showerror("Error", f"Could not read Downhole CSV:\n{e}")
                return

        # 4. Merge logic
        try:
            merged_df, changelog = merge_surveys(baseline_df, top_df, downhole_df)
        except Exception as e:
            messagebox.showerror("Error during merge", str(e))
            return

        # 5. Save new survey & changelog
        today_str = datetime.now().strftime("%Y.%m.%d")
        project_name = os.path.basename(project_dir)
        base = os.path.join(project_dir, f"{today_str}_{project_name}_Survey")
        outcsv = base + ".csv"
        version = 1
        while os.path.exists(outcsv):
            version += 1
            outcsv = f"{base}_v{version}.csv"
        merged_df.to_csv(outcsv, index=False)
        log_file = outcsv.replace("_Survey.csv", "_changelog.txt")
        with open(log_file, "w") as f:
            import pprint
            pprint.pprint(changelog, stream=f)
        messagebox.showinfo(
            "Update Complete",
            f"Survey updated.\nSaved as:\n{os.path.basename(outcsv)}\nChangelog:\n{os.path.basename(log_file)}"
        )

    def elevation_data(self):
        messagebox.showinfo("Not implemented", "Elevation Data logic to be added.")

    def graphs(self):
        messagebox.showinfo("Not implemented", "Graphing logic to be added.")

def launch():
    app = SurveyApp()
    app.mainloop()

if __name__ == "__main__":
    launch()
