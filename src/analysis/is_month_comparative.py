import os
import pandas as pd
from loguru import logger

try:
    from utils import PATH, send_prompt, df_to_csv_text
    from prompt import Prompt
except (ModuleNotFoundError, ImportError):
    from .utils import PATH, send_prompt, df_to_csv_text
    from .prompt import Prompt

file_name = "Revenue Detailed.csv"


def analyse(file_dir=PATH.data_processed):
    # file_path = file_dir / file_name
    prompt = Prompt.is_month_comparative

    dollar_var_top, percent_var_top = get_data(file_dir)

    prompt = prompt.format(
        percent_var_top=percent_var_top, dollar_var_top=dollar_var_top
    )
    return send_prompt(prompt)


def get_data(file_dir=PATH.data_processed):
    file_path = file_dir / file_name

    logger.debug(file_path)

    if not os.path.exists(file_path):
        logger.error(f"File {file_path.name} does not exist")
        return

    # Read the income statement into a DataFrame
    data = pd.read_csv(file_path, index_col=0)

    # data = data.loc["Total Revenue":"Operating Expenses"]
    # data = data.drop(index=["Total Revenue", "Operating Expenses"])

    data = data.iloc[:, [-4, -2, -1]]

    percent_var_top = data.sort_values(by=data.columns[-1], ascending=False).head(10)
    percent_var_top.columns = ["Percent Variance (%)", "% Value", "$ Value"]

    # percent_var_top.iloc[-1] = (
    #     percent_var_top.iloc[-1].astype(float).round(2).astype(str) + "%"
    # )

    dollar_var_top = data.sort_values(by=data.columns[-2], ascending=False).head(10)
    dollar_var_top.columns = ["Dollar ($) Variance", "% Value", "$ Value"]
    dollar_var_top.insert(0, "Rank", range(1, 1 + len(dollar_var_top)))
    percent_var_top.insert(0, "Rank", range(1, 1 + len(percent_var_top)))

    return dollar_var_top, percent_var_top


if __name__ == "__main__":
    logger.info(response := analyse())
