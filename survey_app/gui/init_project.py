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
    except Exception as e:
        messagebox.showerror("Error", f"Could not load baseline survey:\n\n{e}")
        return
    # Write standardized output CSV with status
    try:
        output_path = write_survey_csv(df, project_name, outdir, status="Baseline")
        messagebox.showinfo(
            "Project Initialized",
            f"Baseline written to:\n{output_path}\n\nRecords: {len(df)}"
        )
    except Exception as e:
        messagebox.showerror("Write error", f"Could not save survey file:\n\n{e}")
