from flask import Flask, render_template, request, redirect, url_for
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if url:
        try:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            filename = yt.title + '.mp4'
            stream.download(output_path='downloads', filename=filename)
            return redirect(url_for('downloaded', filename=filename))
        except Exception as e:
            return str(e)
    return 'URL inválida.'

@app.route('/downloaded/<filename>')
def downloaded(filename):
    return render_template('downloaded.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
