from matplotlib.pyplot import autoscale
import pandas as pd

from pathlib import Path
import os

import plotly.figure_factory as ff
import pandas as pd
import plotly.offline as pyo

from dataclasses import dataclass, field

@dataclass
class Castor:
    dir: Path = Path("../vhalid_data/Info/")
    new_table: pd.DataFrame = pd.DataFrame
    table: str = field(init=False)


    def __post_init__(self):
        file = sorted(Path("../vhalid_data/Info/").glob("**/VHALID_study_export*.csv"))[0]
        self.table = pd.read_csv(file, sep=';', on_bad_lines='skip')


    def _print_dataframe(df):

        fig =  ff.create_table(df, index=True)
        fig.update_layout(
            autosize=True
            # width=500,
            # height=200,
        )
        # fig.write_image("table_plotly.png", scale=2)
        pyo.plot(fig)


if __name__ == "__main__":
    information = Castor()
    x = 3
    