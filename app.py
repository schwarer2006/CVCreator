from flask import Flask, render_template, request
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO

app = Flask(__name__)

# Beispiel-Lebenslaufdaten
cv_data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "job_title": "Software Engineer",
    "experience": "5+ years in Python development and cloud technologies.",
    "skills": ["Python", "AWS", "Docker", "Kubernetes"]
}

# Mehrsprachige Anschreiben-Generierung
def generate_cover_letter(cv_data, language):
    if language == "english":
        return f"""
Dear Hiring Manager,

I am writing to express my interest in the {cv_data['job_title']} position at your company. 
With over {cv_data['experience']}, I have developed a strong expertise in technologies such as {', '.join(cv_data['skills'])}.
Based on the job description, I believe my skills align well with your team's needs.

Sincerely,
{cv_data['name']}
{cv_data['email']}
        """
    elif language == "german":
        return f"""
Sehr geehrter Herr/Frau,

ich möchte mein Interesse an der Position {cv_data['job_title']} in Ihrem 
Unternehmen bekunden. 
Mit über {cv_data['experience']} Erfahrung habe ich umfassende Kenntnisse
 in Technologien wie {', '.join(cv_data['skills'])} erworben.
Aufgrund der Stellenbeschreibung bin ich überzeugt, dass meine Fähigkeiten 
gut zu den Anforderungen Ihres Teams passen.

Mit freundlichen Grüßen,
{cv_data['name']}
{cv_data['email']}
        """
    elif language == "french":
        return f"""
Monsieur/Madame,

Je souhaite exprimer mon intérêt pour le poste de {cv_data['job_title']} dans votre entreprise. 
Avec plus de {cv_data['experience']}, j'ai développé une solide expertise dans des technologies telles que {', '.join(cv_data['skills'])}.
Je pense que mes compétences correspondent bien aux besoins de votre équipe.

Cordialement,
{cv_data['name']}
{cv_data['email']}
        """
    elif language == "italian":
        return f"""
Egregio Signore/Signora,

Desidero esprimere il mio interesse per la posizione di {cv_data['job_title']} presso la vostra azienda. 
Con oltre {cv_data['experience']}, ho sviluppato una forte competenza in tecnologie come {', '.join(cv_data['skills'])}.
Credo che le mie competenze siano in linea con le esigenze del vostro team.

Cordiali saluti,
{cv_data['name']}
{cv_data['email']}
        """
    else:
        return "Language not supported"

# Funktion zur Generierung des PDFs mit optimierten Rändern und Zeilenhöhe
def generate_pdf(cover_letter, cv_data):
    pdf_buffer = BytesIO()
    
    # Setze das Format auf DIN A4
    c = canvas.Canvas(pdf_buffer, pagesize=A4)

    # Einstellungen für Schriftarten und Abstände
    c.setFont("Helvetica", 11)
    line_height = 15  # Zeilenhöhe, leicht vergrößert
    margin_left = 1 * inch  # Linker Rand auf 1 Zoll gesetzt
    margin_top = 11 * inch  # Oberer Rand, um Platz für eine zusätzliche Zeile zu schaffen
    
    # Titel des Anschreibens
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_left, margin_top, "Cover Letter")
    
    # Text des Anschreibens
    c.setFont("Helvetica", 11)
    text_object = c.beginText(margin_left, margin_top - line_height*2)
    text_object.setLeading(line_height)
    text_object.textLines(cover_letter)
    c.drawText(text_object)

    # Abschnitt für den Lebenslauf
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_left, margin_top - 230, "Curriculum Vitae")

    c.setFont("Helvetica", 11)
    c.drawString(margin_left, margin_top - 250, f"Name: {cv_data['name']}")
    c.drawString(margin_left, margin_top - 270, f"Experience: {cv_data['experience']}")
    c.drawString(margin_left, margin_top - 290, f"Skills: {', '.join(cv_data['skills'])}")

    c.save()
    
    pdf_buffer.seek(0)
    return pdf_buffer

# Route für das Hauptformular
@app.route('/')
def index():
    return render_template('index.html')

# Route zur Verarbeitung und Generierung des Anschreibens und des PDFs
@app.route('/submit', methods=['POST'])
def submit():
    # Daten aus dem Formular abrufen
    job_description = request.form['job_description']
    language = request.form['language']

    # Anschreiben auf Basis der ausgewählten Sprache generieren
    cover_letter = generate_cover_letter(cv_data, language)

    # PDF generieren
    pdf_buffer = generate_pdf(cover_letter, cv_data)

    # Rückgabe des PDFs als Antwort
    return (pdf_buffer, 200, {
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'inline; filename="output.pdf"'
    })

if __name__ == '__main__':
    app.run(debug=True)
