import os
from flask import Flask, render_template, request, flash
import google.generativeai as genai
from markdown import markdown
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "prod-secret-7721")

# API Configuration
api_key = os.environ.get("AI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

@app.route("/", methods=["GET", "POST"])
def index():
    converted_html = None
    original_text = ""
    
    if request.method == "POST":
        original_text = request.form.get("text", "")
        
        if not api_key:
            flash("AI_API_KEY is not set. Please check your environment configuration.", "error")
        elif not original_text.strip():
            flash("Please enter some text to process.", "warning")
        else:
            try:
                # Content processing logic
                prompt = f"Convert the following text to high-quality Markdown. Use appropriate structure, headings, and formatting. Return only the markdown content:\n\n{original_text}"
                response = model.generate_content(prompt)
                markdown_content = response.text
                converted_html = markdown(markdown_content, extensions=['extra', 'codehilite'])
            except Exception as e:
                flash(f"Error during processing: {str(e)}", "error")
                
    return render_template("index.html", original_text=original_text, converted_html=converted_html)

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=debug_mode)
