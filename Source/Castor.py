import pandas as pd

from pathlib import Path
import os

from dataclasses import dataclass, field

@dataclass
class Castor:
    dir: Path = Path("Info/")
    new_table: pd.DataFrame = pd.DataFrame([])
    table: str = field(init=False)


    def __post_init__(self):
        file = sorted(Path("Info/").glob("**/VHALID_study_export*.csv"))[0]
        self.table = pd.read_csv(file, sep=';', on_bad_lines='skip')


if __name__ == "__main__":
    info = Castor()
    x = 3
