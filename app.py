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

            # THE STRICT CBR VERSION (Mimics FreeConvert's most stable output)
            # -vbr off: Disables Variable Bitrate (forces Constant Bitrate)
            # -application voip: Forces voice-optimized packet structure
            # -map_metadata -1: Strips all "Music" tags
            subprocess.run([
                'ffmpeg', '-y', '-i', in_p,
                '-c:a', 'libopus', 
                '-b:a', '24k',         # 24k is the "magic" number for TG bubbles
                '-vbr', 'off',         # TURN OFF VBR (Force CBR)
                '-application', 'voip', 
                '-ar', '48000', 
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
            h2 { color: #64b5f6; margin: 0; }
            p { color: #aeb7be; font-size: 12px; margin: 10px 0 20px 0; }
            .btn { background: #3390ec; color: white; border: none; padding: 15px; border-radius: 12px; font-weight: bold; width: 100%; font-size: 16px; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Voice Converter</h2>
            <p>libopus | 48kHz | <b>Strict CBR</b> | Original Channels</p>
            <form method="post" enctype="multipart/form-data" id="f">
                <input type="file" name="file" accept="audio/*" required style="margin-bottom:20px; width:100%;">
                <button type="submit" class="btn" id="b">Convert & Download</button>
            </form>
        </div>
        <script>
            document.getElementById('f').onsubmit = function() {
                document.getElementById('b').innerText = "Converting...";
                document.getElementById('b').disabled = true;
            };
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
