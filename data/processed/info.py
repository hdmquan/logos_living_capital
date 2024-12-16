import pandas as pd
import glob
from pathlib import Path

here = Path(__file__).resolve().parent

for file in glob.glob(str(here / "*.csv")):
    df = pd.read_csv(file, index_col=0)
    df = df.dropna(thresh=2)
    print("Columns:", df.columns.tolist())
    print("Rows: ", end="")
    for index, row in df.iterrows():
        print(index, end=", ")
    print("\n")
