from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_sample_pdf():
    file_path = "data/AetherCorp_Annual_Report_2025.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # Page 1: Introduction
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, height - 100, "AetherCorp Annual Strategy Report 2025")
    
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 150, "Confidential - Internal Use Only")
    
    text = [
        "Executive Summary:",
        "AetherCorp is a global leader in sustainable energy solutions.",
        "In 2024, our total revenue reached $4.2 billion, a 15% increase from 2023.",
        "Our primary goal for 2025 is the 'Project Helios' initiative, which aims to",
        "reduce carbon emissions by 40% across all manufacturing plants.",
        "",
        "Regional Performance:",
        "- North America: $1.8 billion (Growth: 8%)",
        "- Europe: $1.4 billion (Growth: 12%)",
        "- Asia-Pacific: $1.0 billion (Growth: 25%)"
    ]
    
    y = height - 200
    for line in text:
        c.drawString(100, y, line)
        y -= 20
        
    # Page 2: Policies
    c.showPage()
    c.setFont("Helvetica-Bold", 18)
    c.drawString(100, height - 100, "Employee Benefits & Remote Work Policy")
    
    c.setFont("Helvetica", 12)
    policy_text = [
        "Remote Work Guidelines:",
        "1. Employees are eligible for 'Flexible Fridays', allowing work-from-home.",
        "2. A monthly home-office stipend of $150 is provided for high-speed internet.",
        "3. Core collaboration hours are 10:00 AM to 3:00 PM EST.",
        "",
        "Health Benefits:",
        "- Premium Dental coverage is included for all full-time staff.",
        "- Mental health days: Employees are entitled to 5 paid 'Recharge Days' per year.",
        "",
        "Contact Information:",
        "For HR inquiries, contact hr@aethercorp.internal or call ext. 5505."
    ]
    
    y = height - 150
    for line in policy_text:
        c.drawString(100, y, line)
        y -= 20

    c.save()
    print(f"✅ Created sample PDF at: {file_path}")

if __name__ == "__main__":
    # Ensure directory exists
    os.makedirs("data", exist_ok=True)
    create_sample_pdf()
