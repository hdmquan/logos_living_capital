import openai
from openai import OpenAI
from fpdf import FPDF

from pathlib import Path
from datetime import datetime

here = Path(__file__).resolve().parent
data = here / "data"


def generate_pdf_from_prompt(prompt):
    # Set your OpenAI API key
    api_key = open(here / "openai-api-key.txt").read().strip()

    client = OpenAI(api_key=api_key)
    # openai.api_key = api_key

    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    output_text = response["choices"][0]["message"]["content"]

    # Create a PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, output_text)

    # Save the PDF to a file
    pdf_file_path = (
        here / "output" / f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    )
    pdf.output(pdf_file_path)

    print(f"PDF generated: {pdf_file_path}")


prompt = """
We are a retirement home. Here is our Value Variance:
{is_month_comparative}

Here is our Census Revenue Trend:
{census_revenue_trend}

Write a concise paragraph summarizing what is going on, what went wrong and its potential cause, and what is the most suitable course of action.
"""

if __name__ == "__main__":
    is_month_comparative_file = data / "is_month_comparative.csv"
    census_revenue_trend_file = data / "census_revenue_trend.csv"

    if not (is_month_comparative_file).exists():
        print("Error: Monthly comparative data not found.")
        exit(1)
    if not (census_revenue_trend_file).exists():
        print("Error: Census revenue trend data not found.")
        exit(1)

    with open(is_month_comparative_file) as f1, open(census_revenue_trend_file) as f2:
        # Read and strip the data from both files
        is_month_comparative = f1.read().strip()
        census_revenue_trend = f2.read().strip()

        # Format the prompt with both pieces of data
        prompt = prompt.format(
            is_month_comparative=is_month_comparative,
            census_revenue_trend=census_revenue_trend,
        )

    generate_pdf_from_prompt(prompt)
