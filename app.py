from flask import Flask, request, render_template
import PyPDF2

# Dummy detection functions
def predict_fake_or_real_email_content(text):
    if "scam" in text.lower() or "fraud" in text.lower():
        return "Scam detected."
    return "Looks legitimate."

def url_detection(url):
    if "malicious" in url:
        return "Malicious URL detected."
    return "Safe URL."

app = Flask(__name__)

# Home Route
@app.route('/')
def home():
    return render_template("index.html")

# File Scam Detection Route
@app.route('/scam', methods=['POST'])   # ✅ fixed (no trailing slash mismatch)
def detect_scam():
    if 'file' not in request.files:
        return render_template("index.html", message="No file uploaded.")

    file = request.files['file']
    extracted_text = ""
    message = ""

    if file.filename == '':
        message = "No file selected."
    elif file.filename.endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            extracted_text = " ".join(
                [page.extract_text() for page in pdf_reader.pages if page.extract_text()]
            )
            if not extracted_text.strip():
                message = "File is empty or unreadable."
        except PyPDF2.errors.PdfReadError:
            message = "Invalid PDF file."
    elif file.filename.endswith('.txt'):
        try:
            extracted_text = file.read().decode("utf-8")
            if not extracted_text.strip():
                message = "File is empty or unreadable."
        except UnicodeDecodeError:
            message = "Could not read the text file."
    else:
        message = "Invalid file type. Upload PDF or TXT only."

    if message:
        return render_template("index.html", message=message)

    result = predict_fake_or_real_email_content(extracted_text)
    return render_template("index.html", message=f"File Scan Result: {result}")

# URL Scam Detection Route
@app.route('/predict', methods=['POST'])
def predict_url():
    url = request.form.get('url', '').strip()

    if not url:
        return render_template("index.html", message="Please enter a URL.")

    if not url.startswith(('http://', 'https://')):
        return render_template("index.html", message="Enter a valid URL starting with http:// or https://")

    classification = url_detection(url)
    return render_template("index.html", input_url=url, predicted_class=f"URL Scan Result: {classification}")

if __name__ == '__main__':
    app.run(debug=True)
