import re
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import pandas as pd
import io

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


def qualitative():
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


def quantitative():
    return is_month_comparative.get_data()


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
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    return table


def generate_pdf():
    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    text = qualitative()
    dollar_var_top, percent_var_top = quantitative()

    # Parse the text
    elements = markdown2text(text, styles)

    # Add first DataFrame
    elements.append(
        Paragraph("Top 10 Categories with Highest Dollar Variance", styles["Heading3"])
    )
    elements.append(df2table(dollar_var_top, col_widths=[200, 150]))
    elements.append(Spacer(1, 24))

    # Add second DataFrame
    elements.append(
        Paragraph("Top 10 Categories with Highest Percent Variance", styles["Heading3"])
    )
    elements.append(df2table(percent_var_top, col_widths=[200, 150]))
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

    if st.button("Generate Report"):
        with st.spinner("Generating report..."):
            try:
                # Generate qualitative analysis
                qual_analysis = qualitative()
                st.subheader("Qualitative Analysis")
                st.markdown(qual_analysis)

                # Generate quantitative analysis
                dollar_var_top, percent_var_top = quantitative()

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Top 10 Categories with Highest Dollar Variance")
                    st.dataframe(dollar_var_top)

                with col2:
                    st.subheader("Top 10 Categories with Highest Percent Variance")
                    st.dataframe(percent_var_top)

                # Generate PDF
                pdf_buffer = generate_pdf()
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
