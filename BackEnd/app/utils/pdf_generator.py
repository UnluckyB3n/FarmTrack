from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from io import BytesIO


def generate_animal_traceability_report(animal_data: dict, events: list, movements: list) -> BytesIO:
    """
    Generate a comprehensive PDF traceability report for an animal.
    
    Args:
        animal_data: Dictionary with animal information
        events: List of event records
        movements: List of movement records
    
    Returns:
        BytesIO object containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    title = Paragraph("Animal Traceability Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Report metadata
    report_date = Paragraph(f"<b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                           styles["Normal"])
    elements.append(report_date)
    elements.append(Spacer(1, 24))
    
    # Animal Information Section
    elements.append(Paragraph("Animal Information", heading_style))
    
    animal_info_data = [
        ['Attribute', 'Value'],
        ['Animal ID', str(animal_data.get('id', 'N/A'))],
        ['Name', animal_data.get('name', 'N/A')],
        ['Tag ID', animal_data.get('tag_id', 'N/A')],
        ['Species', animal_data.get('species', 'N/A')],
        ['Breed', animal_data.get('breed', {}).get('name', 'N/A')],
        ['Current Facility', animal_data.get('facility', {}).get('name', 'N/A')],
        ['Owner', animal_data.get('owner', {}).get('username', 'N/A')],
        ['Date Added', animal_data.get('date_added', 'N/A')[:10] if animal_data.get('date_added') else 'N/A']
    ]
    
    animal_table = Table(animal_info_data, colWidths=[2*inch, 4*inch])
    animal_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(animal_table)
    elements.append(Spacer(1, 24))
    
    # Movement History Section
    if movements:
        elements.append(Paragraph("Movement History", heading_style))
        
        movement_data = [['Step', 'Facility', 'Type', 'Location', 'Date']]
        for idx, movement in enumerate(movements):
            movement_data.append([
                str(len(movements) - idx),
                movement.get('facility_name', 'Unknown'),
                movement.get('facility_type', 'N/A'),
                movement.get('facility_location', 'N/A'),
                movement.get('timestamp', 'N/A')[:10] if movement.get('timestamp') else 'N/A'
            ])
        
        movement_table = Table(movement_data, colWidths=[0.5*inch, 2*inch, 1.2*inch, 1.5*inch, 1.3*inch])
        movement_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9)
        ]))
        
        elements.append(movement_table)
        elements.append(Spacer(1, 24))
    
    # Event Timeline Section
    if events:
        elements.append(Paragraph("Event Timeline", heading_style))
        
        event_data = [['Date', 'Type', 'Valid', 'Details']]
        for event in events[:20]:  # Limit to 20 most recent events
            event_data.append([
                event.get('timestamp', 'N/A')[:10] if event.get('timestamp') else 'N/A',
                event.get('event_type', 'N/A'),
                '✓' if event.get('is_valid') else '✗',
                event.get('event_metadata', 'No details')[:50] + '...' if event.get('event_metadata', '') and len(event.get('event_metadata', '')) > 50 else event.get('event_metadata', 'No details')
            ])
        
        event_table = Table(event_data, colWidths=[1*inch, 1.2*inch, 0.6*inch, 3.7*inch])
        event_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8)
        ]))
        
        elements.append(event_table)
        
        if len(events) > 20:
            elements.append(Spacer(1, 12))
            note = Paragraph(f"<i>Note: Showing 20 most recent events out of {len(events)} total events.</i>", 
                           styles["Normal"])
            elements.append(note)
    
    # Footer
    elements.append(Spacer(1, 24))
    footer = Paragraph("<i>This report was automatically generated by FarmTrack - Livestock Traceability System</i>", 
                      styles["Normal"])
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF content
    buffer.seek(0)
    return buffer


def generate_compliance_report(stats: dict, anomalies: list, facilities: list) -> BytesIO:
    """
    Generate a compliance report for regulators.
    
    Args:
        stats: Dictionary with system statistics
        anomalies: List of anomaly records
        facilities: List of facility records
    
    Returns:
        BytesIO object containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    title = Paragraph("Compliance Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Report metadata
    report_date = Paragraph(f"<b>Report Period:</b> {datetime.now().strftime('%B %Y')}<br/>"
                           f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                           styles["Normal"])
    elements.append(report_date)
    elements.append(Spacer(1, 24))
    
    # System Statistics
    elements.append(Paragraph("System Overview", heading_style))
    
    stats_data = [
        ['Metric', 'Value'],
        ['Total Animals', str(stats.get('totalAnimals', 0))],
        ['Total Events', str(stats.get('totalEvents', 0))],
        ['Anomalies Detected', str(stats.get('anomalies', 0))],
        ['Registered Facilities', str(stats.get('totalFacilities', 0))],
        ['Compliance Rate', f"{((stats.get('totalEvents', 0) - stats.get('anomalies', 0)) / stats.get('totalEvents', 1) * 100):.1f}%" if stats.get('totalEvents', 0) > 0 else 'N/A']
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(stats_table)
    elements.append(Spacer(1, 24))
    
    # Anomalies Section
    if anomalies:
        elements.append(Paragraph("Recent Anomalies", heading_style))
        
        anomaly_data = [['Date', 'Animal ID', 'Event Type', 'Reason']]
        for anomaly in anomalies[:15]:
            anomaly_data.append([
                anomaly.get('timestamp', 'N/A')[:10] if anomaly.get('timestamp') else 'N/A',
                str(anomaly.get('animal_id', 'N/A')),
                anomaly.get('event_type', 'N/A'),
                anomaly.get('anomaly_reason', 'No reason provided')[:40]
            ])
        
        anomaly_table = Table(anomaly_data, colWidths=[1*inch, 1*inch, 1.5*inch, 3*inch])
        anomaly_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.red),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightpink),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8)
        ]))
        
        elements.append(anomaly_table)
        elements.append(Spacer(1, 24))
    
    # Facilities Section
    if facilities:
        elements.append(Paragraph("Registered Facilities", heading_style))
        
        facility_data = [['Name', 'Type', 'Location']]
        for facility in facilities[:20]:
            facility_data.append([
                facility.get('name', 'N/A'),
                facility.get('facility_type', 'N/A'),
                facility.get('location', 'N/A')
            ])
        
        facility_table = Table(facility_data, colWidths=[2.5*inch, 1.5*inch, 2.5*inch])
        facility_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9)
        ]))
        
        elements.append(facility_table)
    
    # Footer
    elements.append(Spacer(1, 24))
    footer = Paragraph("<i>This compliance report was automatically generated by FarmTrack - Livestock Traceability System</i>", 
                      styles["Normal"])
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    buffer.seek(0)
    return buffer
