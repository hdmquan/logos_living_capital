import pandas as pd
from utils import PATH
from loguru import logger

data = pd.read_csv(PATH.data_processed / "Income Statement T-12.csv", index_col=0)

# Keep only row with the word "Total"
data = data[data.index.str.contains("total", case=False)]

# print(data.index)


# TODO: Need more discussion
key_groups = {
    "Total Revenue": ["Total Revenue"],
    "Total Census": ["Total Census"],
    "Total Salaries": [
        "Total Nursing Salaries",
        "Total Dietary Salaries",
        "Total Housekeeping Salaries",
        "Total Recreation Salaries",
        "Total Marketing Salaries",
        "Total R&M Salaries",
        "Total Administrative Salaries",
    ],
    "Total Expenses": [
        "Total Nursing Expenses",
        "Total Dietary Expenses",
        "Total Housekeeping and Laundry Expenses",
        "Total Recreation Expenses",
        "Total Marketing Expenses",
        "Total R&M Expenses",
        "Total G&A Expenses",
    ],
    "Fixed Costs": [
        "Total Rent and Depreciation",
        "Total Insurance",
    ],
}


agg_data = pd.DataFrame(columns=data.columns)

for group, rows in key_groups.items():
    matching_rows = data[data.index.isin(rows)]
    if not matching_rows.empty:
        agg_data.loc[group] = matching_rows.sum()

# print(agg_data)
