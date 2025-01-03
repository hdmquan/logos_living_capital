import hashlib
import re
import shutil
from datetime import datetime
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def save_file(uploaded_file, root_dir: Path) -> Path:
    """Create a unique folder based on file hash and timestamp"""
    # Create hash of file content
    file_hash = hashlib.md5(uploaded_file.getvalue()).hexdigest()[:8]

    # Create timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create unique folder name
    folder_name = f"{timestamp}_{file_hash}"
    unique_folder = root_dir / "uploads" / folder_name

    # Create folders if they don't exist
    unique_folder.mkdir(parents=True, exist_ok=True)
    (unique_folder / "raw").mkdir(exist_ok=True)
    (unique_folder / "processed").mkdir(exist_ok=True)

    # Save the uploaded file to the "raw" directory
    with open(unique_folder / "raw" / uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return unique_folder


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
