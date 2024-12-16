from analysis import (
    balance_sheet,
    income_statement,
    is_month_comparative,
    labor,
    revenue,
    utils,
)

from analysis.prompt import Prompt


def analyse():
    prompt = Prompt.master

    # Collecting analyses in a list for better readability
    analyses = [
        "Balance sheet analysis: " + balance_sheet.analyse(),
        "Income Statement analysis: " + income_statement.analyse(),
        "IS Month Comparative analysis: " + is_month_comparative.analyse(),
        "Labor Data analysis: " + labor.analyse(),
        "Revenue Data analysis: " + revenue.analyse(),
    ]

    # Joining the analyses into a single prompt
    prompt = "\n".join(analyses) + prompt

    response = utils.send_prompt(prompt)

    return response


if __name__ == "__main__":
    print(response := analyse())
