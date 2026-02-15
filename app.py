import os, uuid
from flask import Flask, request, send_file
from voicegram import mp3_to_opus

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        if f:
            file_id = str(uuid.uuid4())
            input_path = f"{file_id}.mp3"
            f.save(input_path)
            try:
                mp3_to_opus(input_path) 
                output_path = f"{file_id}.ogg"
                return send_file(output_path, as_attachment=True, download_name="voice.ogg")
            finally:
                if os.path.exists(input_path): os.remove(input_path)
            
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            :root {
                --bg: #0f1721;
                --card: #1c2733;
                --accent: #3390ec;
                --text: #ffffff;
                --dim: #708499;
            }
            body { 
                background: var(--bg); 
                color: var(--text); 
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                display: flex; align-items: center; justify-content: center; 
                height: 100vh; margin: 0; 
            }
            .container { 
                background: var(--card); 
                padding: 40px 30px; 
                border-radius: 28px; 
                width: 90%; max-width: 360px; 
                text-align: center;
                box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            }
            h1 { font-size: 24px; font-weight: 600; margin: 0 0 8px 0; letter-spacing: -0.5px; }
            p { color: var(--dim); font-size: 14px; margin: 0 0 30px 0; }
            
            .file-input-wrapper {
                position: relative;
                margin-bottom: 20px;
            }
            input[type="file"] {
                opacity: 0; position: absolute; left: 0; top: 0; width: 100%; height: 100%; cursor: pointer;
            }
            .custom-file-btn {
                background: rgba(255,255,255,0.05);
                border: 1px dashed var(--dim);
                padding: 15px; border-radius: 12px;
                display: block; color: var(--dim); font-size: 14px;
            }
            
            .submit-btn { 
                background: var(--accent); color: white; border: none; 
                padding: 16px; border-radius: 14px; font-weight: 600; 
                width: 100%; font-size: 16px; cursor: pointer;
                transition: transform 0.1s, background 0.2s;
            }
            .submit-btn:active { transform: scale(0.97); background: #2b78c2; }
            .submit-btn:disabled { background: #3d4b59; cursor: not-allowed; }
            
            #filename { 
                display: block; margin-top: 10px; font-size: 12px; color: var(--accent); 
                white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Converter</h1>
            <p>Audio to Telegram Voice</p>
            
            <form method="post" enctype="multipart/form-data" id="uploadForm">
                <div class="file-input-wrapper">
                    <div class="custom-file-btn" id="dropzone">Select audio file</div>
                    <input type="file" name="file" id="fileField" accept="audio/*" required>
                    <span id="filename"></span>
                </div>
                
                <button type="submit" class="submit-btn" id="btn">Process</button>
            </form>
        </div>

        <script>
            const fileField = document.getElementById('fileField');
            const btn = document.getElementById('btn');
            const filenameLabel = document.getElementById('filename');

            fileField.onchange = e => {
                if(e.target.files.length > 0) {
                    filenameLabel.innerText = e.target.files[0].name;
                    document.getElementById('dropzone').style.borderColor = "#3390ec";
                }
            };

            document.getElementById('uploadForm').onsubmit = () => {
                btn.disabled = true;
                btn.innerText = "Encoding...";
            };
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
