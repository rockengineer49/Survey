from dataclasses import dataclass
from pathlib import Path

DATE_FMT = "%Y.%m.%d"  # Used in output file names
SURVEY_SUFFIX = "Survey.csv"
CHANGELOG_SUFFIX = "Changelog.txt"

PROJECT_META_FILENAME = "project_meta.json"  # stores project center and settings

@dataclass
class ProjectPaths:
    root: Path
    @property
    def meta_file(self) -> Path:
        return self.root / PROJECT_META_FILENAME

