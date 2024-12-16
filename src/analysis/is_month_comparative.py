import os
import pandas as pd
from loguru import logger

try:
    from utils import PATH, send_prompt, df_to_csv_text
    from prompt import Prompt
except ModuleNotFoundError:
    from .utils import PATH, send_prompt, df_to_csv_text
    from .prompt import Prompt

file_path = PATH.data_processed / "Revenue Detailed.csv"


def analyse():
    prompt = Prompt.is_month_comparative

    if not os.path.exists(file_path):
        logger.error(f"File {file_path.name} does not exist")
        return

    # Read the income statement into a DataFrame
    data = pd.read_csv(file_path, index_col=0)
    data = data.dropna()

    data = data.iloc[:, [-4, -2, -1]]

    percent_var_top = data.sort_values(by=data.columns[-1], ascending=False).head(10)

    # percent_var_top.iloc[-1] = (
    #     percent_var_top.iloc[-1].astype(float).round(2).astype(str) + "%"
    # )

    dollar_var_top = data.sort_values(by=data.columns[-2], ascending=False).head(10)

    prompt = prompt.format(
        percent_var_top=percent_var_top, dollar_var_top=dollar_var_top
    )
    return send_prompt(prompt)


if __name__ == "__main__":
    logger.info(response := analyse())
