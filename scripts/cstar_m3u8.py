import requests
import re
import os
import sys
import datetime

# Logging simple pour GitHub Actions
def log(msg):
    print(f"[{datetime.datetime.now()}] {msg}")

# URL source
url = "https://raw.githubusercontent.com/Paradise-91/ParaTV/main/streams/canalplus/cstar-dm.m3u8"

# Dossier et fichier de sortie
OUTPUT_DIR = "./Streams"
OUTPUT_FILE = "cstar-1080.m3u8"

try:
    log(f"Téléchargement de : {url}")
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        contenu = response.text

        # Regex pour capturer les deux lignes ensemble
        pattern = re.compile(r'(#EXT-X-STREAM-INF:.*NAME="1080@60".*?)\n(https?://[^\s]+1080@60\.m3u8)', re.DOTALL)
        match = pattern.search(contenu)

        if match:
            stream_info = match.group(1)
            stream_url = match.group(2)
            final_content = f"#EXTM3U\n{stream_info}\n{stream_url}\n"

            os.makedirs(OUTPUT_DIR, exist_ok=True)
            output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
            with open(output_path, "w") as f:
                f.write(final_content)

            log(f"✅ Fichier généré : {output_path}")
        else:
            log("❌ Aucun flux 1080@60 trouvé.")
            sys.exit(1)
    else:
        log(f"❌ Erreur HTTP {response.status_code} lors du téléchargement.")
        sys.exit(1)

except Exception as e:
    log(f"❌ Exception levée : {str(e)}")
    sys.exit(1)
