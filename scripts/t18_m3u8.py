import requests
import re
import os
import sys
import datetime

# Logging simple pour GitHub Actions
def log(msg):
    print(f"[{datetime.datetime.now()}] {msg}")

# URL source
url = "https://raw.githubusercontent.com/Paradise-91/ParaTV/main/streams/t18/t18-dm.m3u8"

# Dossier et fichier de sortie
FHD_OUTPUT_DIR = "./Streams"
FHD_OUTPUT_FILE = "t18.m3u8"

try:
    log(f"Téléchargement de : {url}")
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        contenu = response.text

        # Extraction des URLs contenant '1080@60.m3u8'
        urls_m3u8 = re.findall(r'(https?://[^\s]+1080@60\.m3u8)', contenu)
        urls_sans_suffixe = [re.sub(r'1080@60\.m3u8$', '', url) for url in urls_m3u8]

        if urls_sans_suffixe:
            m3u8_url = urls_sans_suffixe[0]
            log(f"URL extraite : {m3u8_url}")

            def generate_m3u_content(m3u8_url, resolution, bandwidth, video_url):
                content = "#EXTM3U\n"
                content += f'#EXT-X-STREAM-INF:BANDWIDTH={bandwidth},AVERAGE-BANDWIDTH={bandwidth-200000},CODECS="avc1.64002A,mp4a.40.2",RESOLUTION={resolution},FRAME-RATE=25.000,AUDIO="audio-AACL-128"\n{m3u8_url}{video_url}\n'
                return content

            fhd_content = generate_m3u_content(m3u8_url, "1920x1080", 4277000, "1080@60.m3u8")

            os.makedirs(FHD_OUTPUT_DIR, exist_ok=True)
            output_path = os.path.join(FHD_OUTPUT_DIR, FHD_OUTPUT_FILE)
            with open(output_path, "w") as f:
                f.write(fhd_content)

            log(f"✅ Fichier généré : {output_path}")
        else:
            log("❌ Aucune URL contenant '1080@60.m3u8' trouvée.")
            sys.exit(1)
    else:
        log(f"❌ Erreur HTTP {response.status_code} lors du téléchargement.")
        sys.exit(1)

except Exception as e:
    log(f"❌ Exception levée : {str(e)}")
    sys.exit(1)
