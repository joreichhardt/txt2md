import os
from flask import Flask, render_template, request, flash
from prometheus_flask_exporter import PrometheusMetrics
import google.generativeai as genai
from markdown import markdown
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "prod-secret-7721")

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.8')

conversion_counter = metrics.counter(
    'txt2md_conversions_total', 'Total number of text conversions'
)

# API Configuration
api_key = os.environ.get("AI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    system_instruction = (
        "You are a text-to-markdown conversion specialist. You always produce "
        "standard CommonMark/GitHub Flavored Markdown. You strictly use ATX "
        "headings (#) and never use wiki-style syntax like '==' or '==='. "
        "Additionally, you insert relevant and tasteful emojis at the beginning "
        "of section headings to represent the topic."
    )
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction=system_instruction
    )
else:
    model = None

@app.route("/", methods=["GET", "POST"])
def index():
    converted_html = None
    markdown_content = ""
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
                prompt = (
                    f"Convert the following text into high-quality standard Markdown. "
                    f"Use ATX headings (#), standard formatting, and include relevant "
                    f"emojis for each section heading to make the document more engaging. "
                    f"Return ONLY the markdown content:\n\n{original_text}"
                )
                response = model.generate_content(prompt)
                markdown_content = response.text
                converted_html = markdown(markdown_content, extensions=['extra', 'codehilite'])
                conversion_counter.inc()
            except Exception as e:
                flash(f"Error during processing: {str(e)}", "error")
                
    return render_template(
        "index.html", 
        original_text=original_text, 
        converted_html=converted_html,
        markdown_content=markdown_content
    )

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=debug_mode)
