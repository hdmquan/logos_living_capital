import os
import pandas as pd
from loguru import logger

try:
    from utils import PATH, send_prompt, df_to_csv_text
    from prompt import Prompt
except (ModuleNotFoundError, ImportError):
    from .utils import PATH, send_prompt, df_to_csv_text
    from .prompt import Prompt

file_name = "Labor.csv"


def analyse(file_dir=PATH.data_processed):
    file_path = file_dir / file_name
    prompt = Prompt.labor

    if not os.path.exists(file_path):
        logger.error(f"File {file_path.name} does not exist")
        return

    # Read the income statement into a DataFrame
    data = pd.read_csv(file_path, index_col=0)

    # Keep only row with the word "Total"
    data = data[data.index.str.contains("total", case=False)]

    # print(data.index)

    # TODO: Need more discussion
    important_roles = [
        "Total Resident Care Director",
        "Total Resident Care Associate",
        "Total Regional Director of Clinical Operations",
        "Total LPN",
        "Total RN",
        "Total Nursing Salaries",
        "Total Aides",
        "Total Executive Director",
        "Total Housekeeping Staff",
        "Total Dietary Salaries",
        "Total Administrative Salaries",
    ]

    data = data[data.index.isin(important_roles)]

    # print(agg_data)
    labor = df_to_csv_text(data)

    prompt = prompt.format(labor=labor)
    return send_prompt(prompt)


if __name__ == "__main__":
    logger.info(response := analyse())
