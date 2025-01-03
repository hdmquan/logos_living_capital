import io
import re
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
from loguru import logger
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from PIL import Image
from reportlab.pdfgen import canvas

from analysis import (
    balance_sheet,
    income_statement,
    is_month_comparative,
    labor,
    revenue,
    utils,
)
from analysis.prompt import Prompt
from data import process_uploaded_file
import utils as file_utils
from utils import markdown2text, df2table
from chart import sankey_diagram, total_revenue_stack_line, total_expense_stack_line

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
    dollar_var_top, percent_var_top = is_month_comparative.get_data(data_dir)

    # Add Sankey diagram generation
    df = pd.read_csv(data_dir / "Income Statement T-12.csv", index_col=0)

    # Create Sankey diagram
    fig_display = sankey_diagram(df, font_size=16)
    fig_pdf = sankey_diagram(df, font_size=10)
    fig_stack_line = total_revenue_stack_line(df)
    fig_expense_stack_line = total_expense_stack_line(df)
    return dollar_var_top, percent_var_top, fig_display, fig_pdf, fig_stack_line, fig_expense_stack_line


# TODO: To be more robust
def generate_pdf(text, dollar_var_top, percent_var_top, sankey_fig, fig_stack_line, fig_expense_stack_line):
    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    if "Heading1" in styles:
        styles["Heading1"].alignment = 1
    if "Heading2" in styles:
        styles["Heading2"].alignment = 1
    if "Heading3" in styles:
        styles["Heading3"].alignment = 1
    elements = []

    # Add H1 for Qualitative Analysis
    elements.append(Paragraph("Qualitative Analysis", styles["Heading1"]))
    elements.append(Spacer(1, 12))

    # Parse the text
    elements.extend(markdown2text(text, styles))

    # Create a small italic style
    small_italic_style = styles["Normal"].clone("SmallItalic")
    small_italic_style.fontSize = 8
    small_italic_style.fontName = "Helvetica"
    small_italic_style.italic = True

    # Add H1 for Quantitative Analysis
    elements.append(Paragraph("Quantitative Analysis", styles["Heading1"]))
    elements.append(Spacer(1, 12))

    elements.append(df2table(dollar_var_top, col_widths=[200, 150]))
    elements.append(
        Paragraph(
            "Ranked Expense Category Dollar Variance",
            small_italic_style,
        )
    )
    elements.append(Spacer(1, 24))

    elements.append(df2table(percent_var_top, col_widths=[200, 150]))
    elements.append(
        Paragraph(
            "Ranked Expense Category Percent Variance",
            small_italic_style,
        )
    )
    elements.append(Spacer(1, 24))

    def add_image_to_elements(fig, elements, title, small_italic_style, max_width=500, img_format='png', width=700, height=500):
        # Convert Plotly figure to PIL Image
        img_bytes = pio.to_image(fig, format=img_format, width=width, height=height)
        img = Image.open(io.BytesIO(img_bytes))
        
        # Save the image to a temporary buffer
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)

        # Calculate image dimensions while maintaining aspect ratio
        img_width, img_height = img.size
        aspect = img_height / float(img_width)
        new_width = min(max_width, img_width)
        new_height = new_width * aspect

        # Create a flowable image
        from reportlab.platypus import Image as RLImage
        img_flowable = RLImage(img_buffer, width=new_width, height=new_height)
        elements.append(img_flowable)
        
        elements.append(
            Paragraph(
                title,
                small_italic_style,
            )
        )
        elements.append(Spacer(1, 24))

    add_image_to_elements(sankey_fig, elements, "Revenue and Expense Flow", small_italic_style)
    add_image_to_elements(fig_stack_line, elements, "Revenue Breakdown Over Time", small_italic_style)
    add_image_to_elements(fig_expense_stack_line, elements, "Expense Breakdown Over Time", small_italic_style)
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
                (dollar_var_top, percent_var_top, sankey_fig_display, sankey_fig_pdf, fig_stack_line, fig_expense_stack_line) = quantitative(
                    processed_dir / "processed"
                )

                st.subheader("Revenue and Expense Flow")
                st.plotly_chart(sankey_fig_display, use_container_width=True)

                st.subheader("Revenue Breakdown Over Time")
                st.plotly_chart(fig_stack_line, use_container_width=True)

                st.subheader("Expense Breakdown Over Time")
                st.plotly_chart(fig_expense_stack_line, use_container_width=True)

                st.subheader("Top 10 Categories with Highest Dollar Variance")
                st.dataframe(dollar_var_top)

                st.subheader("Top 10 Categories with Highest Percent Variance")
                st.dataframe(percent_var_top)

                # Generate PDF
                pdf_buffer = generate_pdf(
                    qual_analysis, dollar_var_top, percent_var_top, sankey_fig_pdf, fig_stack_line, fig_expense_stack_line
                )
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_buffer,
                    file_name="financial_report.pdf",
                    mime="application/pdf",
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                logger.exception(
                    "An error occurred during report generation"
                )  # Print the trace as well


if __name__ == "__main__":
    main()
