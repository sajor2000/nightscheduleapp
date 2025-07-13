from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import calendar
from io import BytesIO

def generate_ics(doctor, schedules, month):
    """Generate ICS calendar file for a doctor's schedule."""
    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//MICU Scheduler//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:MICU Night Shifts - {doctor.name}",
        "X-WR-TIMEZONE:America/Chicago",
    ]
    
    for schedule in schedules:
        date = schedule.date
        # Create all-day event
        ics_lines.extend([
            "BEGIN:VEVENT",
            f"UID:{schedule.id}@micu-scheduler",
            f"DTSTART;VALUE=DATE:{date.strftime('%Y%m%d')}",
            f"DTEND;VALUE=DATE:{(date + timedelta(days=1)).strftime('%Y%m%d')}",
            f"SUMMARY:MICU Night Shift",
            f"DESCRIPTION:Night shift at Rush University Medical Center MICU",
            f"LOCATION:Rush University Medical Center - MICU",
            "STATUS:CONFIRMED",
            "END:VEVENT"
        ])
    
    ics_lines.append("END:VCALENDAR")
    return "\n".join(ics_lines)

def generate_pdf(month, schedules, preferences):
    """Generate PDF calendar for the month's schedule."""
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
        leftMargin=0.5*inch,
        rightMargin=0.5*inch
    )
    
    # Container for the 'Flowable' objects
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    year, month_num = map(int, month.split('-'))
    month_name = calendar.month_name[int(month_num)]
    title = Paragraph(f"<b>MICU Night Shift Schedule - {month_name} {year}</b>", 
                     styles['Title'])
    elements.append(title)
    
    # Create calendar data
    cal = calendar.monthcalendar(year, month_num)
    
    # Create schedule lookup
    schedule_dict = {}
    for s in schedules:
        schedule_dict[s.date.day] = s.doctor_initials
    
    # Create preference lookups
    unavailable_dates = {}
    preferred_dates = {}
    for pref in preferences:
        for date_str in pref.unavailable:
            day = int(date_str.split('-')[2])
            if day not in unavailable_dates:
                unavailable_dates[day] = []
            unavailable_dates[day].append(pref.doctor_initials)
        
        for date_str in pref.preferred:
            day = int(date_str.split('-')[2])
            if day not in preferred_dates:
                preferred_dates[day] = []
            preferred_dates[day].append(pref.doctor_initials)
    
    # Days of week header
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Build calendar table data
    table_data = [days]
    
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append('')
            else:
                cell_text = f"<b>{day}</b><br/>"
                
                # Add assigned doctor
                if day in schedule_dict:
                    cell_text += f"<font size='14'>{schedule_dict[day]}</font>"
                else:
                    cell_text += "<font color='red'>Unassigned</font>"
                
                # Add preference indicators
                if day in preferred_dates:
                    cell_text += f"<br/><font size='8' color='green'>Pref: {', '.join(preferred_dates[day])}</font>"
                if day in unavailable_dates:
                    cell_text += f"<br/><font size='8' color='red'>Unavail: {', '.join(unavailable_dates[day])}</font>"
                
                week_data.append(Paragraph(cell_text, styles['Normal']))
        
        table_data.append(week_data)
    
    # Create table
    table = Table(table_data, colWidths=[1.4*inch]*7, rowHeights=[0.4*inch] + [1.2*inch]*len(cal))
    
    # Style the table
    table_style = TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Calendar cells
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('LEFTPADDING', (0, 1), (-1, -1), 6),
        ('RIGHTPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ])
    
    # Highlight weekends
    for row in range(1, len(table_data)):
        table_style.add('BACKGROUND', (5, row), (6, row), colors.lightgrey)
    
    table.setStyle(table_style)
    elements.append(table)
    
    # Legend
    legend_data = [
        ["Legend:", ""],
        ["Doctor Initials", "Assigned doctor for that night"],
        ["Pref:", "Doctors who preferred to work this day"],
        ["Unavail:", "Doctors unavailable this day"],
        ["Unassigned", "No doctor assigned yet"]
    ]
    
    legend_table = Table(legend_data, colWidths=[1.5*inch, 4*inch])
    legend_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 4), (0, 4), colors.red),
    ]))
    
    elements.append(Paragraph("<br/><br/>", styles['Normal']))
    elements.append(legend_table)
    
    # Build PDF
    doc.build(elements)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes