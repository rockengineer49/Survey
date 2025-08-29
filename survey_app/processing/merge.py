from survey_app.io.downhole_loader import load_downhole_csv_for_merge
from survey_app.io.csv_reader import read_survey_csv
from survey_app.processing.merge import merge_downhole_to_baseline
from survey_app.io.csv_writer import write_survey_csv

# Step 1: Load baseline/project file (csv)
baseline_df = read_survey_csv('path/to/your_project_survey.csv')

# Step 2: Load downhole csv (with the new loader)
downhole_df = load_downhole_csv_for_merge('path/to/Downhole.csv')

# Step 3: Merge!
merged_df, changelog = merge_downhole_to_baseline(baseline_df, downhole_df)

# Step 4: Save updated survey file (use version increment/your output logic)
write_survey_csv(merged_df, 'PROJECTNAME', 'output_folder', status='Surveyed', version=2)
