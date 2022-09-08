import pandas as pd
import numpy as np

from pathlib import Path

import plotly.graph_objects as go

import pandas as pd
import plotly.offline as pyo
import plotly.io as pio

from dataclasses import dataclass, field

@dataclass
class Castor:
    dir: Path = Path("../vhalid/Data/Info/")
    new_table: pd.DataFrame = pd.DataFrame
    table: str = field(init=False)


    def __post_init__(self):
        file = sorted(Path("../vhalid/Data/Info/").glob("**/VHALID_study_export_202208*.csv"))[0]
        self.table = pd.read_csv(file, sep=';', on_bad_lines='skip')


    def _print_dataframe(patient, nr, list_df):
        save_dir = Path(f"../vhalid_data/Tables/Patient{nr}/")
        for df_str in list_df:
            if df_str in list_df:
                df = eval(f"patient.{df_str}")
                fig = go.Figure(data=[go.Table(
                        cells=dict(values=[df.index, list(df["Values"])], align=["left", "center"],
                        font_size=15, font_family=["Arial Black", "Arial"], height=50))
                            ])
                fig.update_layout(
                    autosize=True,
                    width=1000
                )
                try:
                    save_dir.mkdir(parents=True, exist_ok=False)
                except FileExistsError:
                    pass
                finally:
                    # pass
                    if df_str == "vha4":
                        df_str = "vha3_was4"
                    elif df_str == "vha5":
                        df_str = "vha4_was5"
                    elif df_str == "vha6":
                        df_str = "vha5_was6"
                    elif df_str == "vha7":
                        df_str = "vha1_ic7"
                    elif df_str == "vha8":
                        df_str = "vha2_ic8"
                    elif df_str == "vha9":
                        df_str = "vha3_ic9"
                    fig.write_image(save_dir / f"{df_str}.png", scale=2)
                    # pyo.plot(fig)


if __name__ == "__main__":
    information = Castor()
    x = 3
