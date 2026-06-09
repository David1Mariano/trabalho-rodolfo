from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet

from mission_statistics import mission_statistics
from graficos import generate_graphs


def generate_report():

    generate_graphs()

    stats = mission_statistics()

    pdf = SimpleDocTemplate(
        "Mission_Report.pdf",
        pagesize=landscape(A4)
    )

    styles = getSampleStyleSheet()

    elements = []

    # =====================
    # TÍTULO
    # =====================

    elements.append(
        Paragraph(
            "NASA Mission Control Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 8))

    elements.append(
        Paragraph(
            "Experimental Space Mission Monitoring System",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            "This report summarizes telemetry, operational statistics and mission performance indicators.",
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 10))

    # =====================
    # GRÁFICOS
    # =====================

    elements.append(
        Paragraph(
            "Mission Telemetry Graphs",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 5))

    graphs = Table(
        [[
            Image(
                "temperature_graph.png",
                width=250,
                height=140
            ),

            Image(
                "energy_graph.png",
                width=250,
                height=140
            )
        ]],
        colWidths=[300, 300]
    )

    graphs.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))

    elements.append(graphs)

    elements.append(Spacer(1, 10))

    # =====================
    # DADOS
    # =====================

    temp = stats["temperature"]
    energy = stats["energy"]

    # =====================
    # TABELA TEMPERATURA
    # =====================

    temp_table = Table([
        ["TEMPERATURE METRIC", "VALUE"],
        ["Mean", temp["mean"]],
        ["Median", temp["median"]],
        ["Mode", temp["mode"]],
        ["Minimum", temp["minimum"]],
        ["Maximum", temp["maximum"]],
        ["Std Dev", temp["std_dev"]],
        ["Variance", temp["variance"]],
        ["CV (%)", temp["cv"]],
        ["Q1", temp["q1"]],
        ["Q2", temp["q2"]],
        ["Q3", temp["q3"]],
    ])

    temp_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER")
    ]))

    # =====================
    # TABELA ENERGIA
    # =====================

    energy_table = Table([
        ["ENERGY METRIC", "VALUE"],
        ["Mean", energy["mean"]],
        ["Median", energy["median"]],
        ["Mode", energy["mode"]],
        ["Minimum", energy["minimum"]],
        ["Maximum", energy["maximum"]],
        ["Std Dev", energy["std_dev"]],
        ["Variance", energy["variance"]],
        ["CV (%)", energy["cv"]],
        ["Q1", energy["q1"]],
        ["Q2", energy["q2"]],
        ["Q3", energy["q3"]],
    ])

    energy_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER")
    ]))

    # =====================
    # TABELAS LADO A LADO
    # =====================

    stats_tables = Table(
        [[temp_table, energy_table]],
        colWidths=[330, 330]
    )

    stats_tables.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER")
    ]))

    elements.append(stats_tables)

    elements.append(Spacer(1, 10))

    # =====================
    # CONCLUSÃO AUTOMÁTICA
    # =====================

    if temp["cv"] < 20:
        conclusion = (
            "The mission demonstrated stable operational "
            "behavior with low temperature variability."
        )
    else:
        conclusion = (
            "The mission exhibited elevated variability "
            "and should be monitored carefully."
        )

    elements.append(
        Paragraph(
            "Automatic Analysis",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            conclusion,
            styles["BodyText"]
        )
    )

    pdf.build(elements)

    print("Mission_Report.pdf generated successfully.")