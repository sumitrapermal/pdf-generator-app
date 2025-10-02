import streamlit as st
import io
from reportlab.lib.pagesizes import letter , landscape , A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle



# ---------- Service Agreement ----------
def create_service_agreement(date, ref_no, client_name, package_type, company_type,
                             business_activity, docs_list, costs, duration, scope, terms):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("<b>SERVICE AGREEMENT</b>", styles['Title']))
    elements.append(Spacer(1, 12))

    # Basic Info
    elements.append(Paragraph(f"<b>Date:</b> {date}", styles['Normal']))
    elements.append(Paragraph(f"<b>Ref No:</b> {ref_no}", styles['Normal']))
    elements.append(Paragraph(f"<b>Client Name:</b> {client_name}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Company Info Table
    data = [
        ["Package type", package_type],
        ["Type of the Company", company_type],
        ["Minimum Authorized Person", "One"],
        ["Minimum Director", "One"],
        ["Business Activity", business_activity]
    ]
    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Documents Required
    elements.append(Paragraph("<b>Documents Required:</b>", styles['Heading2']))
    for d in docs_list:
        elements.append(Paragraph(f"• {d}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Cost Table
    elements.append(Paragraph("<b>Estimated Costs:</b>", styles['Heading2']))
    cost_data = [["Sr No", "Service Type", "Cost in BHD"]] + costs
    cost_table = Table(cost_data, colWidths=[50, 300, 100])
    cost_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ]))
    elements.append(cost_table)
    elements.append(Spacer(1, 12))

    # Estimation Duration
    elements.append(Paragraph("<b>Estimation Duration:</b>", styles['Heading2']))
    elements.append(Paragraph(duration, styles['Normal']))
    elements.append(Spacer(1, 12))

    # Scope of Work
    elements.append(Paragraph("<b>Scope of Work:</b>", styles['Heading2']))
    for s in scope:
        elements.append(Paragraph(f"- {s}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Terms & Conditions
    elements.append(Paragraph("<b>Terms & Conditions:</b>", styles['Heading2']))
    for t in terms:
        elements.append(Paragraph(f"{t}", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return buffer



# ---------- Certificate ----------
def create_certificate(name, course, date, cert_id, issued_by):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter),
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)
    elements = []

    # Styles
    title_style = ParagraphStyle(
        'TitleStyle',
        fontSize=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        spaceAfter=20,
        leading=36
    )

    name_style = ParagraphStyle(
        'NameStyle',
        fontSize=28,
        alignment=TA_CENTER,
        textColor=colors.red,
        leading=34
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        fontSize=16,
        alignment=TA_CENTER,
        textColor=colors.blue,
        leading=22,
        spaceAfter=20
    )

    signature_style = ParagraphStyle(
        'SignatureStyle',
        fontSize=12,
        alignment=TA_RIGHT,
        textColor=colors.black,
        spaceBefore=40
    )

    # Title
    elements.append(Paragraph("<b>CERTIFICATE OF COMPLETION</b>", title_style))
    elements.append(Spacer(1, 20))

    # Body text with more details
    text = f"""
    This is proudly presented to <b>{name}</b> for successfully completing the course <b>{course}</b>.<br/><br/>
    {name} has shown exceptional dedication, enthusiasm, and skill throughout the training, 
    completing all assignments and demonstrating outstanding performance.<br/><br/>
    We hereby recognize and congratulate <b>{name}</b> for this achievement.<br/><br/>
    Date Issued: {date} | Certificate ID: {cert_id}<br/>
    Issued By: {issued_by}
    """
    elements.append(Paragraph(text, body_style))
    elements.append(Spacer(1, 50))

    # Signature
    elements.append(Paragraph("______________________________", signature_style))
    elements.append(Paragraph("Authorized Signatory", signature_style))
    elements.append(Paragraph("Director", signature_style))

    # Decorative border & background
    def add_design(canvas, doc):
        canvas.saveState()
        width, height = landscape(letter)
        # Light background color
        canvas.setFillColorRGB(0.95, 0.95, 1)  # very light blue
        canvas.rect(0, 0, width, height, fill=1)

        # Decorative border
        canvas.setStrokeColor(colors.darkblue)
        canvas.setLineWidth(4)
        canvas.rect(20, 20, width - 40, height - 40, fill=0)

        canvas.restoreState()

    doc.build(elements, onFirstPage=add_design, onLaterPages=add_design)
    buffer.seek(0)
    return buffer


# ---------- Invoice ----------
def create_invoice(client, client_address, service, amount, invoice_no, date, due_date, notes):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("<b>Invoice</b>", styles['Title']))
    elements.append(Spacer(1, 20))

    # Client Info
    elements.append(Paragraph(f"Invoice No: {invoice_no}", styles['Normal']))
    elements.append(Paragraph(f"Client: {client}", styles['Normal']))
    elements.append(Paragraph(f"Address: {client_address}", styles['Normal']))
    elements.append(Paragraph(f"Invoice Date: {date}", styles['Normal']))
    elements.append(Paragraph(f"Due Date: {due_date}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Service table
    data = [["Description", "Amount (INR)"], [service, str(amount)], ["Total", str(amount)]]
    table = Table(data, colWidths=[300, 150])
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))

    # Additional Notes
    if notes:
        elements.append(Paragraph(f"<b>Notes:</b> {notes}", styles['Normal']))
        elements.append(Spacer(1, 20))

    # General Terms & Conditions
    terms_text = """
    <b>General Terms and Conditions:</b><br/>
    • Charges are subject to change without notice or changes in Ministry fee and for unforeseen reasons.<br/>
    • Please be noted all charges are mentioned with discount (SME discount).<br/>
    • Payments are nonrefundable in any circumstance, payment should be done within due dates.<br/>
    • Any additional service/admin charges will be charged extra on next invoice.<br/>
    • Any discrepancy in this bill should be brought to our notice immediately within 3 days of invoice.<br/>
    • Should you have any questions or need further assistance, please do not hesitate to reach out to us.<br/>
    • Your feedback is invaluable to us as we strive to improve our services and cater to our client's needs.<br/>
    • Thank you for your Business.<br/>
    """
    elements.append(Paragraph(terms_text, styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return buffer



# ---------- Streamlit App ----------
st.title("📄  PDF Generator")

# First dropdown for template choice
template_choice = st.selectbox("Choose a Template", ["Select...", "Service Agreement", "Certificate", "Invoice"])

# Show inputs based on template selection
if template_choice == "Service Agreement":
    st.subheader("Fill Service Agreement Details")
    date = st.date_input("Date")
    ref_no = st.text_input("Reference Number", "BKR09-2025-CR701")
    client_name = st.text_input("Client Name")
    package_type = st.text_input("Package Type", "Start-up")
    company_type = st.text_input("Company Type", "With Limited Liability (W.L.L)")
    business_activity = st.text_area("Business Activity", "Company Incorporation")

    # Documents
    docs_input = st.text_area("Documents Required (comma separated)", 
                              "Proposed company names, Lease Agreement, Passport copy, POA")
    docs_list = [d.strip() for d in docs_input.split(",")]

    # Costs Table
    st.write("### Enter Cost Items")
    costs = []
    for i in range(1, 4):
        service = st.text_input(f"Service {i} Name", f"Service {i}")
        cost = st.text_input(f"Service {i} Cost", "0.00")
        costs.append([str(i), service, cost])

    # Estimation Duration
    duration = st.text_area("Estimation Duration", "Completion within 3–4 working weeks...")

    # Scope of Work
    scope_input = st.text_area("Scope of Work (comma separated)", 
                               "Consultancy, Documentation, Business Activity approval")
    scope = [s.strip() for s in scope_input.split(",")]

    # Terms & Conditions
    terms_input = st.text_area("Terms & Conditions (comma separated)", 
                               "Confidentiality, Ownership of Work Product, Legislative Compliance")
    terms = [t.strip() for t in terms_input.split(",")]

    if st.button("Generate Service Agreement PDF"):
        pdf_buffer = create_service_agreement(date, ref_no, client_name, package_type, company_type,
                                              business_activity, docs_list, costs, duration, scope, terms)
        st.download_button("⬇️ Download PDF", pdf_buffer, "service_agreement.pdf", "application/pdf")


elif template_choice == "Certificate":
    st.subheader("Fill Certificate Details")
    name = st.text_input("Recipient Name")
    course = st.text_input("Course/Training/Role")
    date = st.date_input("Issued Date")
    cert_id = st.text_input("Certificate ID / Reference No", "CERT-2025-001")
    issued_by = st.text_input("Issued By (Organization)", "ABC Institute of Technology")

    if st.button("Generate Certificate PDF"):
        pdf_buffer = create_certificate(name, course, date, cert_id, issued_by)
        st.download_button("⬇️ Download Certificate", pdf_buffer, "certificate.pdf", "application/pdf")



elif template_choice == "Invoice":
    st.subheader("Fill Invoice Details")
    client = st.text_input("Client Name")
    client_address = st.text_area("Client Address")
    service = st.text_input("Service Provided")
    amount = st.number_input("Amount (INR)", min_value=0, step=500)
    invoice_no = st.text_input("Invoice Number", "INV-2025-001")
    date = st.date_input("Invoice Date")
    due_date = st.date_input("Due Date")
    notes = st.text_area("Additional Notes / Remarks")

    if st.button("Generate Invoice PDF"):
        pdf_buffer = create_invoice(client, client_address, service, amount, invoice_no, date, due_date, notes)
        st.download_button("⬇️ Download PDF", pdf_buffer, "invoice.pdf", "application/pdf")
