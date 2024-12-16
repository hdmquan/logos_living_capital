from analysis import (
    balance_sheet,
    income_statement,
    is_month_comparative,
    labor,
    revenue,
    utils,
)

prompt = """
Given these analysis of these financial data of a real estate company, compile a complete analysis of what is going on, what should decision maker be aware of and what is the potential course of action. Your analysis should be as concise as possible without compromising any information and do not make up numbers and things.
"""


prompt = (
    "Balance sheet analysis: "
    + balance_sheet.analyse()
    + "Income Statement analysis: "
    + income_statement.analyse()
    + "IS Month Comparative analysis: "
    + is_month_comparative.analyse()
    + "Labor Data analysis: "
    + labor.analyse()
    + "Revenue Data analysis: "
    + revenue.analyse()
    + prompt
)

response = utils.send_prompt(prompt)

print(response)
