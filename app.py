import os, uuid
from flask import Flask, request, send_file
# We import the logic you found
from voicegram import mp3_to_opus

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        if f:
            file_id = str(uuid.uuid4())
            # Save the incoming file with an .mp3 extension so voicegram recognizes it
            input_path = f"{file_id}.mp3"
            f.save(input_path)
            
            try:
                # This is the magic line you found
                # It handles the libopus, 48k, and metadata stripping automatically
                mp3_to_opus(input_path) 
                
                # voicegram outputs a file with the same name but .ogg extension
                output_path = f"{file_id}.ogg"
                
                return send_file(output_path, as_attachment=True, download_name="voice.ogg")
            finally:
                # Cleanup to keep your Render storage from filling up
                if os.path.exists(input_path): os.remove(input_path)
            
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background: #1c2733; color: white; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .card { background: #242f3d; padding: 30px; border-radius: 20px; width: 85%; max-width: 400px; text-align: center; border: 1px solid #3390ec; }
        .btn { background: #3390ec; color: white; border: none; padding: 15px; border-radius: 12px; font-weight: bold; width: 100%; cursor: pointer; }
    </style></head>
    <body>
        <div class="card">
            <h2>Voicegram Converter</h2>
            <p style="color:#aeb7be">Forcing Telegram Voice Bubble</p>
            <form method="post" enctype="multipart/form-data" id="f">
                <input type="file" name="file" accept="audio/*" required style="margin-bottom:20px; width:100%;">
                <button type="submit" class="btn" id="b">Convert & Download</button>
            </form>
        </div>
        <script>document.getElementById('f').onsubmit = function(){ document.getElementById('b').innerText="Processing..."; };</script>
    </body></html>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
