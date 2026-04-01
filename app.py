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
metrics.info('app_info', 'Application info', version='1.1.2')


# API Configuration
api_key = os.environ.get("AI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    system_instruction = (
        "You are a text-to-markdown conversion specialist. You always produce "
        "standard CommonMark/GitHub Flavored Markdown. You strictly use ATX "
        "headings (#) and never use wiki-style syntax like '==' or '==='. "
        "Additionally, you insert relevant and tasteful emojis as Markdown "
        "shortcodes (e.g., :rocket:, :bulb:, :memo:) at the beginning of section "
        "headings to represent the topic. "
        "CRITICAL: Always maintain the original language of the input text. "
        "Do NOT translate the content."
    )
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction=system_instruction
    )
else:
    model = None

@app.route("/", methods=["GET", "POST"])
@metrics.counter('txt2md_conversions_total', 'Total number of text conversions',
                 labels={'result': lambda: request.method})
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
                    f"Maintain the original language of the text. Do NOT translate it. "
                    f"Use ATX headings (#), standard formatting, and include relevant "
                    f"emoji shortcodes (like :smile:) for each section heading to make "
                    f"the document more engaging. Return ONLY the markdown content:\n\n"
                    f"{original_text}"
                )
                response = model.generate_content(prompt)
                markdown_content = response.text
                
                # Render HTML with emoji support
                extensions = [
                    'extra', 
                    'codehilite', 
                    'pymdownx.emoji'
                ]
                converted_html = markdown(markdown_content, extensions=extensions)
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
