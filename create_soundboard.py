#!/usr/bin/env python3
import os
import glob
from pathlib import Path
import base64

buttons_per_row = 2
audio_folder = "../audio_files/"
html_out_filename = "index.html"

html = """
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no" />
        <title>Cobra Commander Soundboard</title>
        <style>
        :root {
            --switch-color: white;
        }
        
        body {
            color: #eaeaea;
            background: black;
            text-align: center;
            font-family: verdana, sans-serif;
        }
        #flex_container {
            display: flex;
            flex-wrap: wrap;
        }
        .grid-container {
            display: grid;
            grid-template-columns: repeat(1/*$buttons_per_row$*/, auto);
            grid-column-gap: 5px;
            grid-row-gap: 5px;
            max-width: 100vw;
            margin: 5px auto;
            padding: 5px;
            border-style: solid;
        }
        button,
        input[type="button"] {
            border: 0;
            border-radius: 0.3rem;
            background: #1fa3ec;
            color: #faffff;
            line-height: 2.4rem;
            font-size: 1.2rem;
            width: 100%;
            -webkit-transition-duration: 0.4s;
            transition-duration: 0.4s;
            cursor: pointer;
        }
        button:hover,
        input[type="button"]:hover {
            background: #0e70a4;
        }
        </style>
    </head>
    <body>
        <script>
            function play(id) {
                var audio = document.getElementById(id);
                audio.play();
            }
        </script>
        <div id="flex_container">
            <div class="grid-container">
                <!--$audio_section$-->
            </div>
        </div>
    </body>
</html>
"""

audio_section = ""
filelist = glob.glob(f"{audio_folder}*")
for fname in sorted(filelist):
    path = Path(fname)
    ext = path.suffix
    if ext in [".mp3", ".wav"]:
        basename = path.stem
        parts = basename.split('_')
        capitalized_parts = [part.title() for part in parts]
        button_text = ' '.join(capitalized_parts)
        file = open(fname, "rb")
        file_content = file.read()
        file.close()

        b64data = (base64.b64encode(file_content)).decode("ascii")
        if ext == ".mp3":
            media_type = "audio/mpeg"
        elif ext == ".wav":
            media_type = "audio/wav"
        audio_html = f"""<input type="button" value="{button_text}" data-audio-id="{fname}" onclick="play(this.getAttribute('data-audio-id'))">\n<audio id="{fname}" src="data:{media_type};base64,{b64data}"></audio>"""
        audio_section += audio_html + "\n"

html = html.replace("1/*$buttons_per_row$*/", str(buttons_per_row))
html = html.replace("<!--$audio_section$-->", audio_section)
file = open(html_out_filename, "w")
file.write(html)
file.close()

