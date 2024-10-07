
from flask import Flask, render_template, request
from transformers import pipeline
import pdfkit

app = Flask(__name__)

# Modell für Stellenanalyse laden
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Beispieldaten für den Lebenslauf
cv_data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "job_title": "Software Engineer",
    "experience": "5+ years in Python development and cloud technologies.",
    "skills": ["Python", "AWS", "Docker", "Kubernetes"]
}

def generate_cover_letter(cv_data, matched_skills, language):
    if language == "english":
        return generate_english_cover_letter(cv_data, matched_skills)
    elif language == "german":
        return generate_german_cover_letter(cv_data, matched_skills)
    elif language == "french":
        return generate_french_cover_letter(cv_data, matched_skills)
    elif language == "italian":
        return generate_italian_cover_letter(cv_data, matched_skills)
    else:
        return "Language not supported"

def generate_english_cover_letter(cv_data, matched_skills):
    return f"""
Dear Hiring Manager,

I am writing to express my interest in the {cv_data['job_title']} position at your company. With over {cv_data['experience']}, 
I have developed a strong expertise in technologies such as {', '.join(cv_data['skills'])}.

Based on the job description for the {cv_data['job_title']} role, I believe my skills in {', '.join(matched_skills)} 
align well with the requirements outlined by your team. My experience in building scalable systems with {', '.join(matched_skills)} 
makes me confident in my ability to contribute effectively to your company.

Sincerely,
{cv_data['name']}
{cv_data['email']}
    """

def generate_german_cover_letter(cv_data, matched_skills):
    return f"""
Sehr geehrter Herr/Frau,

hiermit bewerbe ich mich auf die Position {cv_data['job_title']} in Ihrem Unternehmen. Mit über {cv_data['experience']} Erfahrung 
habe ich ein umfassendes Know-how in Technologien wie {', '.join(cv_data['skills'])} erworben.

Basierend auf der Stellenbeschreibung für die Position {cv_data['job_title']} bin ich überzeugt, dass meine Fähigkeiten in {', '.join(matched_skills)} 
gut zu den Anforderungen Ihres Teams passen. Meine Erfahrung in der Entwicklung skalierbarer Systeme mit {', '.join(matched_skills)} 
macht mich sicher, dass ich effektiv zu Ihrem Unternehmen beitragen kann.

Mit freundlichen Grüßen,
{cv_data['name']}
{cv_data['email']}
    """

def generate_french_cover_letter(cv_data, matched_skills):
    return f"""
Monsieur/Madame,

Je souhaite exprimer mon intérêt pour le poste de {cv_data['job_title']} dans votre entreprise. Avec plus de {cv_data['experience']}, 
j'ai développé une expertise solide dans des technologies telles que {', '.join(cv_data['skills'])}.

En me basant sur la description de poste pour le rôle de {cv_data['job_title']}, je crois que mes compétences en {', '.join(matched_skills)} 
correspondent bien aux exigences de votre équipe. Mon expérience dans le développement de systèmes évolutifs avec {', '.join(matched_skills)} 
me rend confiant quant à ma capacité à contribuer efficacement à votre entreprise.

Cordialement,
{cv_data['name']}
{cv_data['email']}
    """

def generate_italian_cover_letter(cv_data, matched_skills):
    return f"""
Egregio Signore/Signora,

Scrivo per esprimere il mio interesse per la posizione di {cv_data['job_title']} presso la vostra azienda. Con oltre {cv_data['experience']}, 
ho sviluppato una solida esperienza in tecnologie come {', '.join(cv_data['skills'])}.

In base alla descrizione del lavoro per il ruolo di {cv_data['job_title']}, credo che le mie competenze in {', '.join(matched_skills)} 
siano in linea con i requisiti del vostro team. La mia esperienza nella costruzione di sistemi scalabili con {', '.join(matched_skills)} 
mi rende fiducioso nella mia capacità di contribuire efficacemente alla vostra azienda.

Cordiali saluti,
{cv_data['name']}
{cv_data['email']}
    """

# Route für das Hauptformular
@app.route('/')
def index():
    return render_template('index.html')

# Route für die Verarbeitung und Anzeige im Browser
@app.route('/submit', methods=['POST'])
def submit():
    # Daten von der Benutzeroberfläche abrufen
    job_description = request.form['job_description']
    language = request.form['language']

    # Analysiere, welche Skills relevant sind
    result = classifier(job_description, candidate_labels=cv_data['skills'])
    matched_skills = [skill for skill in result['labels'] if skill['score'] > 0.5]

    # Anschreiben generieren
    cover_letter = generate_cover_letter(cv_data, matched_skills, language)

    # Erzeuge ein HTML-Dokument zur Vorschau im Browser
    html = f"""
    <html>
    <head></head>
    <body>
        <h1>Cover Letter</h1>
        <p>{cover_letter.replace('\n', '<br>')}</p>

        <h2>CV</h2>
        <p>Name: {cv_data['name']}</p>
        <p>Experience: {cv_data['experience']}</p>
        <p>Skills: {', '.join(cv_data['skills'])}</p>

        <!-- Button zum Erstellen des PDFs -->
        <form action="/generate_pdf" method="POST">
            <input type="hidden" name="html_content" value="{html}">
            <input type="submit" value="Download as PDF">
        </form>
    </body>
    </html>
    """

    return html

# Route zur PDF-Generierung
@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # HTML-Inhalt aus dem Formular abrufen
    html_content = request.form['html_content']

    # PDF erstellen
    pdfkit.from_string(html_content, 'output.pdf')

    return "PDF erfolgreich erstellt! Sie können es unter dem Dateinamen 'output.pdf' finden."

if __name__ == '__main__':
    app.run(debug=True)
