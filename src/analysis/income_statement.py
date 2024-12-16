import os
import pandas as pd
from utils import PATH, send_prompt, df_to_csv_text
from loguru import logger

file_path = PATH.data_processed / "Income Statement T-12.csv"


def analyse():
    prompt = """
        {income_statement}

        Analyze the income statement of this real estate company to assess its financial health and performance. Identify key financial ratios and trends to provide a comprehensive overview of its financial position. Your analysis should be as concise as possible without compromising any information and do not make up numbers and things.
    """

    if not os.path.exists(file_path):
        logger.error(f"File {file_path.name} does not exist")
        return

    # Read the income statement into a DataFrame
    data = pd.read_csv(file_path, index_col=0)

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
    income_statement = df_to_csv_text(agg_data)

    prompt = prompt.format(income_statement=income_statement)
    return send_prompt(prompt)


if __name__ == "__main__":
    logger.info(response := analyse())
