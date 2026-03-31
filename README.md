# txt2md

A minimalist Flask application to convert raw text into high-quality Markdown documents.

## Features

- **Smart Processing:** Automatically structures your raw input with headings, lists, and formatting.
- **Modern UI:** Clean, responsive interface for effortless writing.
- **Portable:** Easy to run locally or as a Docker container.

## Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/joreichhardt/txt2md.git
   cd txt2md
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration:**
   Set the following environment variables:
   - `AI_API_KEY`: Your API key for processing.
   - `FLASK_SECRET_KEY`: A random string for session security.

4. **Run:**
   ```bash
   python app.py
   ```

## Docker Deployment

### Build
```bash
docker build -t txt2md:latest .
```

### Run
```bash
docker run -p 5000:5000 \
  -e AI_API_KEY="your-key" \
  -e FLASK_SECRET_KEY="your-secret" \
  txt2md:latest
```
