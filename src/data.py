import os
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path
from loguru import logger

ROOT = Path(__file__).resolve().parent.parent

data_dir = ROOT / "data"
xlsx_path = data_dir / "raw" / "2024 09 Harrisburg Opco Financial Statements.xlsx"


sheets = {
    "Census & Revenue Trend": [[7, 12], ["A", "N"]],
    "Balance Sheet": [[6, 74], ["A", "F"]],
    "Income Statement T-12": [
        [7, 160],
        ["A", "N"],
    ],  # Note: This is huge, consider slicing in analysis
    "IS Month Comparative": [[7, 52], ["A", "M"]],
    # TODO: Deal with missing PPD values
    "IS Month Comparative Detailed": [[7, 319], ["A", "M"]],
    "Revenue Detailed": [[7, 54], ["A", "M"]],
    "Labor": [[7, 145], ["A", "I"]],
}


def xlsx2df(rows: str, columns: str, sheet_name: str, xlsx_path=xlsx_path):
    df = pd.read_excel(
        xlsx_path,
        sheet_name=sheet_name,
        header=None,
        skiprows=rows[0] - 1,  # From row 7 (0 - 6)
        nrows=rows[1] - rows[0] + 1,  # To row 12 (7-12)
        usecols=f"{columns[0]}:{columns[1]}",
    )

    df = df.astype(str)

    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Remove empty
    df = df[~df.apply(lambda row: row.str.strip().eq("").all(), axis=1)]

    # Remove repeated
    df = df[~df.apply(lambda row: row.nunique() <= 1, axis=1)]

    df = df.replace("nan", np.nan)

    # TODO: Deal with threshold values
    return df.dropna(axis=0, thresh=2)


def convert_date(date):
    try:
        date = datetime.strptime(date, "%m/%d/%Y")
        return date.strftime("%B/%Y")
    except ValueError:
        logger.warning(f"Could not convert {date}")
        return date


def rename_columns(df, num_rows=2):
    # Extract header rows
    header_rows = [df.iloc[i].astype(str) for i in range(num_rows)]

    # Concat name with non NaN
    df.columns = [
        " ".join(
            filter(lambda x: x != "nan", [row[col_idx] for row in header_rows])
        ).strip()
        for col_idx in range(len(df.columns))
    ]

    df = df.iloc[num_rows:]

    return df


def process_uploaded_file(uploaded_file, upload_dir: Path):
    logger.debug(f"Processing {uploaded_file} uploaded file")

    xlsx_path = upload_dir / "raw" / uploaded_file.name
    with open(xlsx_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    # Process each sheet
    for sheet_name, (rows, columns) in sheets.items():
        df = xlsx2df(rows, columns, sheet_name, xlsx_path=xlsx_path)

        if sheet_name in ["Census & Revenue Trend", "Income Statement T-12"]:
            # Remove "Month Ending"
            df = df.iloc[1:]

            # Change from mm/dd/yyyy to mmmm/yyyy
            # logger.debug(sheet_name)
            # logger.debug(df.columns)
            # Also make the first line to column names
            df.columns = df.iloc[0].astype(str)
            # First row is still date
            df.columns = [convert_date(column) for column in df.columns]

            # Annotate last column to YTD
            df.columns = df.columns[:-1].tolist() + [f"{df.columns[-1]} YTD"]
            # logger.debug(df.head())

            # Remove "Actual" row and "Census" row because there only one
            df = df.iloc[4:]

        elif sheet_name == "Balance Sheet":
            df = rename_columns(df, num_rows=2)
            logger.debug(df.head())

        elif sheet_name in [
            "IS Month Comparative",
            "IS Month Comparative Detailed",
            "Revenue Detailed",
            "Labor",
        ]:
            df = rename_columns(df, num_rows=3)

            logger.debug(df.head())

        else:
            logger.warning(f"Sheet {sheet_name} not processed")

        # Save to processed directory
        df.to_csv(upload_dir / "processed" / f"{sheet_name}.csv", index=False)

    return upload_dir


if __name__ == "__main__":
    for sheet_name, (rows, columns) in sheets.items():
        df = xlsx2df(rows, columns, sheet_name)

        if sheet_name in ["Census & Revenue Trend", "Income Statement T-12"]:
            # Remove "Month Ending"
            df = df.iloc[1:]

            # Change from mm/dd/yyyy to mmmm/yyyy
            # logger.debug(sheet_name)
            # logger.debug(df.columns)
            # Also make the first line to column names
            df.columns = df.iloc[0].astype(str)
            # First row is still date
            df.columns = [convert_date(column) for column in df.columns]

            # Annotate last column to YTD
            df.columns = df.columns[:-1].tolist() + [f"{df.columns[-1]} YTD"]
            # logger.debug(df.head())

            # Remove "Actual" row and "Census" row because there only one
            df = df.iloc[4:]

        elif sheet_name == "Balance Sheet":
            df = rename_columns(df, num_rows=2)
            logger.debug(df.head())

        elif sheet_name in [
            "IS Month Comparative",
            "IS Month Comparative Detailed",
            "Revenue Detailed",
            "Labor",
        ]:
            df = rename_columns(df, num_rows=3)

            logger.debug(df.head())

        else:
            logger.warning(f"Sheet {sheet_name} not processed")

        df.to_csv(data_dir / "processed" / f"{sheet_name}.csv", index=False)
