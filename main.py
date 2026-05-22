from flask import Flask, request, render_template_string
import yt_dlp

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YT Video Link Extractor</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f9; }
        .container { max-width: 500px; margin: auto; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        input[type="text"] { width: 90%; padding: 10px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .output { margin-top: 20px; word-break: break-all; }
        .success { color: #28a745; font-weight: bold; text-decoration: none; display: block; margin-top: 10px; }
        .error { color: red; }
    </style>
</head>
<body>
<div class="container">
    <h2>YouTube Link Extractor</h2>
    <form method="POST">
        <input type="text" name="url" placeholder="Paste YouTube Link Here" value="{{ url }}">
        <br>
        <button type="submit">Get Download Link</button>
    </form>

    <div class="output">
        {% if download_url %}
            <p style="color:green;">Success! Click below to open/download:</p>
            <a class="success" href="{{ download_url }}" target="_blank">👉 Download / Play Video 👈</a>
        {% elif error %}
            <p class="error">Error: {{ error }}</p>
        {% endif %}
    </div>
</div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    url = ""
    download_url = None
    error = None

    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            ydl_opts = {
                'format': 'best',
                'quiet': True,
                # Force yt-dlp to bypass bot detection using iOS/Android clients
                'extractor_args': {'youtube': {'player_client': ['ios', 'android']}}
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    download_url = info.get('url')
            except Exception as e:
                error = str(e)
        else:
            error = "Please enter a URL."

    return render_template_string(HTML_TEMPLATE, url=url, download_url=download_url, error=error)

if __name__ == '__main__':
    app.run()
    
