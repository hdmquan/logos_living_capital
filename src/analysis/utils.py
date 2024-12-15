from pathlib import Path
from openai import OpenAI


class PATH:
    root = Path(__file__).resolve().parent.parent.parent
    src = Path(__file__).resolve().parent.parent
    here = Path(__file__).resolve().parent

    data_processed = root / "data" / "processed"


def openAIClient():
    api_key = open(PATH.src / "openai-api-key.txt").read().strip()
    return OpenAI(api_key=api_key)
