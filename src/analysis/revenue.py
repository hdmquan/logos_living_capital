import os
import pandas as pd
from loguru import logger

try:
    from utils import PATH, send_prompt, df_to_csv_text
except ModuleNotFoundError:
    from .utils import PATH, send_prompt, df_to_csv_text

file_path = PATH.data_processed / "Revenue Detailed.csv"


def analyse():
    prompt = """
        {revenue_detailed}

        Analyze the revenue details of this real estate company to assess its financial health and performance. Identify key financial ratios and trends to provide a comprehensive overview of its financial position. Your analysis should be as concise as possible without compromising any information and do not make up numbers and things.
    """

    if not os.path.exists(file_path):
        logger.error(f"File {file_path.name} does not exist")
        return

    # Read the income statement into a DataFrame
    data = pd.read_csv(file_path, index_col=0)

    # Keep only row with the word "Total"
    data = data[data.index.str.contains("total", case=False)]

    # print(data.index)

    # print(agg_data)
    revenue_detailed = df_to_csv_text(data)

    prompt = prompt.format(revenue_detailed=revenue_detailed)
    return send_prompt(prompt)


if __name__ == "__main__":
    logger.info(response := analyse())
