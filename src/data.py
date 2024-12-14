import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

data_dir = ROOT / "data"
xlsx_path = data_dir / "raw" / "2024 09 Harrisburg Opco Financial Statements.xlsx"

# TODO: Deal with rows serve as hierachy
sheets = {
    "Census & Revenue Trend": [[7, 12], ["A", "N"]],  # TODO: Clear row of "Actual"
    "Balance Sheet": [[6, 74], ["A", "F"]],  # TODO: Clear blank rows
    "Income Statement T-12": [
        [7, 160],
        ["A", "N"],
    ],  # Note: This is huge, consider slicing in analysis
    # TODO: Deal with Level 1 column names for the following, may need separate function
    # "IS Month Comparative": [[7, 52], ["A", "M"]]
    # Messy ahh spreadsheet, may need a separate script or split to 3 different csv
    # "IS Month Comparative Detailed": []
    # "Revenue Detailed": [[7, 54], ["A", "M"]]
    # "Labor": [[7, 145], ["A", "I"]],
}


def xlsx2csv(rows: str, columns: str, sheet_name: str, xlsx_path=xlsx_path):
    df = pd.read_excel(
        xlsx_path,
        sheet_name=sheet_name,
        header=None,
        skiprows=rows[0] - 1,  # From row 7 (0 - 6)
        nrows=rows[1] - rows[0] + 1,  # To row 12 (7-12)
        usecols=f"{columns[0]}:{columns[1]}",
    )

    # Trim it to drop NA and blank/empty rows
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.dropna()
    print(df.head())

    df.to_csv(data_dir / "processed" / f"{sheet_name}.csv", index=False, header=False)


for sheet_name, (rows, columns) in sheets.items():
    xlsx2csv(rows, columns, sheet_name)
