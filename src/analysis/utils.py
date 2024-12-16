from pathlib import Path
from openai import OpenAI
from io import StringIO


class PATH:
    root = Path(__file__).resolve().parent.parent.parent
    src = Path(__file__).resolve().parent.parent
    here = Path(__file__).resolve().parent

    data_processed = root / "data" / "processed"


# TODO: Add multi model interface support
def openAIClient():
    api_key = open(PATH.src / "openai-api-key.txt").read().strip()
    return OpenAI(api_key=api_key)


def dataframe_to_csv_text(df):
    """
    Save the dataframe to CSV format to a variable instead of file
    """
    output = StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()
