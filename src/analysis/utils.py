import os
from pathlib import Path
from openai import OpenAI
from io import StringIO
from loguru import logger


class PATH:
    root = Path(__file__).resolve().parent.parent.parent
    src = Path(__file__).resolve().parent.parent
    here = Path(__file__).resolve().parent

    data_processed = root / "data" / "processed"


# TODO: Add multi model interface support
def send_prompt(prompt, model: str = "gpt-4o", temperature=0.3):
    if model in ["gpt-4o", "gpt-4o-mini"]:
        api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content
    else:
        logger.error(f"Model {model} not found or supported")


def df_to_csv_text(df):
    """
    Save the dataframe to CSV format to a variable instead of file
    """
    output = StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()


if __name__ == "__main__":
    response = send_prompt(
        prompt="This is just a test, please respond 'Copy that'",
        model="gpt-4o-mini",
        temperature=0,
    )

    print(response)
