import os
import pandas as pd
from loguru import logger
from utils import PATH, openAIClient

file_path = PATH.data_processed / "Balance Sheet.csv"

# TODO: Revise and improve this prompt
# Current output is very undesirable
prompt = """ 
    {balance_sheet}
    
    Analyze the balance sheet of this real estate company to assess its financial health and performance. Identify key financial ratios and trends to provide a comprehensive overview of its financial position. Your analysis should be as concise as possible without compromising any information and do not make up numbers and things.
    """


def analyse():

    if not os.path.exists(file_path):
        logger.error(f"File {file_path.name} does not exist")
        return

    # Balance sheet is small enough for the LLM to directly analyse
    with open(file_path) as f:
        balance_sheet = f.read().strip()
        client = openAIClient()

        # TODO: Fine-tune parameters
        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt.format(balance_sheet=balance_sheet)}
            ],
        )

        return response.choices[0].message.content


if __name__ == "__main__":
    logger.info(response := analyse())
