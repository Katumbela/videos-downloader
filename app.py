from flask import Flask, render_template, request, redirect, url_for
import youtube_dl

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if url:
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                ydl.download([url])
                filename = f'downloads/{info["title"]}.{info["ext"]}'
                return redirect(url_for('downloaded', filename=filename))
        except Exception as e:
            return str(e)
    return 'URL inválida.'

@app.route('/downloaded/<filename>')
def downloaded(filename):
    return render_template('downloaded.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
