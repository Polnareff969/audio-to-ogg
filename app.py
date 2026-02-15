import os, subprocess, uuid
from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        if f:
            file_id = str(uuid.uuid4())
            in_p, out_p = f"in_{file_id}", f"{file_id}.ogg"
            f.save(in_p)

            # SETTINGS: 
            # -c:a libopus (Codec)
            # -vbr on (Auto Rate Control / Variable Bitrate)
            # -ar 48000 (Sample Rate)
            # No '-ac' flag used (Preserves original audio channels)
            subprocess.run([
                'ffmpeg', '-y', '-i', in_p,
                '-c:a', 'libopus', 
                '-vbr', 'on',
                '-ar', '48000', 
                '-b:a', '32k',
                '-map_metadata', '-1',
                out_p
            ])
            return send_file(out_p, as_attachment=True, download_name="voice.ogg")
            
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: sans-serif; background: #1c2733; color: white; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
            .card { background: #242f3d; padding: 30px; border-radius: 20px; width: 85%; max-width: 400px; text-align: center; border: 1px solid #3390ec; }
            h2 { color: #64b5f6; margin-bottom: 5px; }
            p { color: #aeb7be; font-size: 13px; margin-bottom: 25px; line-height: 1.5; }
            input[type="file"] { margin: 20px 0; color: #aeb7be; width: 100%; }
            .btn { background: #3390ec; color: white; border: none; padding: 15px; border-radius: 12px; font-weight: bold; width: 100%; font-size: 16px; cursor: pointer; }
            #status { margin-top: 15px; color: #64b5f6; display: none; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Voice Converter</h2>
            <p>libopus | 48kHz | Auto VBR<br>Preserving Original Channels</p>
            <form method="post" enctype="multipart/form-data" id="convForm">
                <input type="file" name="file" accept="audio/*" required>
                <button type="submit" class="btn" id="subBtn">Convert & Download</button>
            </form>
            <div id="status">Converting... Please wait</div>
        </div>
        <script>
            document.getElementById('convForm').onsubmit = function() {
                document.getElementById('subBtn').disabled = true;
                document.getElementById('subBtn').innerText = "Processing...";
                document.getElementById('status').style.display = "block";
            };
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
          
