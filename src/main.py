import re
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import pandas as pd
import io
from pathlib import Path
from loguru import logger
import utils as file_utils

from data import process_uploaded_file
from analysis import (
    balance_sheet,
    income_statement,
    is_month_comparative,
    labor,
    revenue,
    utils,
)

from analysis.prompt import Prompt

# Set page config
st.set_page_config(
    page_title="Financial Report Generator", page_icon="📊", layout="wide"
)


def qualitative(data_dir):
    prompt = Prompt.master
    data_dir = Path(data_dir) / "processed"

    # Collecting analyses in a list for better readability
    analyses = [
        "Balance sheet analysis: " + balance_sheet.analyse(data_dir),
        "Income Statement analysis: " + income_statement.analyse(data_dir),
        "Variance analysis: " + is_month_comparative.analyse(data_dir),
        "Labor Data analysis: " + labor.analyse(data_dir),
        "Revenue Data analysis: " + revenue.analyse(data_dir),
    ]

    # Joining the analyses into a single prompt
    prompt = "\n".join(analyses) + prompt

    response = utils.send_prompt(prompt)

    return response


def quantitative(data_dir):
    return is_month_comparative.get_data(data_dir)


def markdown2text(text, styles):
    text_f = []
    bold_pattern = r"\*\*(.*?)\*\*"  # Regular expression to match **text**

    def bold_replacer(match):
        return f"<b>{match.group(1)}</b>"  # Replace with bold tag

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        # Replace bold syntax (**text**) with <b>text</b>
        line = re.sub(bold_pattern, bold_replacer, line)
        if line.startswith("### "):  # Heading 2
            text_f.append(Paragraph(line[4:], styles["Heading2"]))
        elif line.startswith("#### "):  # Heading 3
            text_f.append(Paragraph(line[5:], styles["Heading3"]))
        elif line.startswith("- "):  # Bullet points
            text_f.append(Paragraph(line, styles["BodyText"]))
        # TODO: Better implementation
        elif line.startswith("1.") or line.startswith("2."):  # Numbered list
            text_f.append(Paragraph(line, styles["BodyText"]))
        else:  # Regular text
            text_f.append(Paragraph(line, styles["BodyText"]))
        text_f.append(Spacer(1, 12))  # Add spacing
    return text_f


def df2table(df, col_widths=None):
    data = [df.columns.to_list()] + df.values.tolist()
    table = Table(data, colWidths=col_widths)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkslategray),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    return table


# TODO: To be more robust
def generate_pdf(text, dollar_var_top, percent_var_top):

    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # for style in styles:
    #     styles[style].fontName = "Helvetica"

    if "Heading1" in styles:
        styles["Heading1"].alignment = 1
    if "Heading2" in styles:
        styles["Heading2"].alignment = 1
    if "Heading3" in styles:
        styles["Heading3"].alignment = 1

    # Parse the text
    elements = markdown2text(text, styles)

    # Create a small italic style
    small_italic_style = styles["Normal"].clone("SmallItalic")
    small_italic_style.fontSize = 8
    small_italic_style.fontName = "Helvetica"
    small_italic_style.italic = True

    elements.append(df2table(dollar_var_top, col_widths=[200, 150]))
    elements.append(
        Paragraph(
            "Top 10 Categories with Highest Dollar Variance",
            small_italic_style,
        )
    )
    elements.append(Spacer(1, 24))

    elements.append(df2table(percent_var_top, col_widths=[200, 150]))
    elements.append(
        Paragraph(
            "Top 10 Categories with Highest Percent Variance",
            small_italic_style,
        )
    )
    elements.append(Spacer(1, 24))

    # Build the document
    doc.build(elements)
    buffer.seek(0)
    return buffer


def main():
    st.title("Financial Report Generator")
    st.write(
        "Generate comprehensive financial reports with qualitative and quantitative analysis."
    )

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Financial Data (Excel)",
        type=["xlsx", "xls"],
        help="Upload the financial data Excel file",
    )

    if uploaded_file is not None:
        # Create unique folder for this upload
        ROOT = Path(__file__).resolve().parent.parent
        upload_dir = file_utils.save_file(uploaded_file, ROOT)

        # Process the uploaded file
        with st.spinner("Processing uploaded file..."):
            try:
                processed_dir = process_uploaded_file(uploaded_file, upload_dir)
                st.success(f"File processed successfully! Stored in: {processed_dir}")

                # Store the processed directory path in session state
                st.session_state["processed_dir"] = processed_dir

                # Enable the generate report button
                generate_report = st.button("Generate Report")
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                return
    else:
        st.info("Please upload a financial statement file to continue")
        return

    if "processed_dir" in st.session_state and generate_report:
        with st.spinner("Generating report..."):
            try:
                # Generate qualitative analysis
                qual_analysis = qualitative(processed_dir)
                st.subheader("Qualitative Analysis")
                st.markdown(qual_analysis)

                # Generate quantitative analysis
                dollar_var_top, percent_var_top = quantitative(
                    processed_dir / "processed"
                )

                st.subheader("Top 10 Categories with Highest Dollar Variance")
                st.dataframe(dollar_var_top)

                st.subheader("Top 10 Categories with Highest Percent Variance")
                st.dataframe(percent_var_top)

                # Sample for testing formating
                # qual_analysis = "lorem ipsum dolor sit amet, consectetur adipiscing"

                # dollar_var_top = pd.DataFrame(
                #     {
                #         "Category": ["Category 1", "Category 2"],
                #         "Dollar Variance": [100, 50],
                #     }
                # )

                # percent_var_top = pd.DataFrame(
                #     {
                #         "Category": ["Category 3", "Category 4"],
                #         "Percent Variance": [50, 25],
                #     }
                # )

                # Generate PDF
                pdf_buffer = generate_pdf(
                    qual_analysis, dollar_var_top, percent_var_top
                )
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_buffer,
                    file_name="financial_report.pdf",
                    mime="application/pdf",
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
