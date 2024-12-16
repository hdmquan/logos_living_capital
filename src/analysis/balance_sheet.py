import os
import pandas as pd
from loguru import logger

try:
    from utils import PATH, send_prompt, df_to_csv_text
    from prompt import Prompt
except ModuleNotFoundError:
    from .utils import PATH, send_prompt, df_to_csv_text
    from .prompt import Prompt

file_path = PATH.data_processed / "Balance Sheet.csv"

# TODO: Revise and improve this prompt
# Current output is very undesirable


def analyse():
    prompt = Prompt.balance_sheet

    if not os.path.exists(file_path):
        logger.error(f"File {file_path.name} does not exist")
        return

    # Balance sheet is small enough for the LLM to directly analyse
    with open(file_path) as f:
        balance_sheet = f.read().strip()
        prompt = prompt.format(balance_sheet=balance_sheet)
        return send_prompt(prompt)


if __name__ == "__main__":
    logger.info(response := analyse())
