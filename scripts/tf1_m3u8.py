import requests
import re
import os

# URL du fichier .m3u8 source
url = "https://raw.githubusercontent.com/Paradise-91/ParaTV/main/streams/tf1plus/tf1.m3u8"

# Chemin du fichier de sortie
FHD_OUTPUT_DIR = "./Streams"
FHD_OUTPUT_FILE = "tf1.m3u8"

# Récupérer le contenu distant
response = requests.get(url)

# Vérifier le succès de la requête
if response.status_code == 200:
    contenu = response.text
    # Regex pour capturer les URLs contenant '1.m3u8'
    urls_m3u8 = re.findall(r'(https?://[^\s]+1\.m3u8)', contenu)
    
    # Supprimer le suffixe '1.m3u8' des URLs
    urls_sans_suffixe = [re.sub(r'1\.m3u8$', '', url) for url in urls_m3u8]

    if urls_sans_suffixe:
        m3u8_url = urls_sans_suffixe[0]  # On prend le premier
        print(f"URL sans le suffixe '1.m3u8' : {m3u8_url}")

        def generate_m3u_content(m3u8_url, resolution, bandwidth, video_url, audio_url):
            content = "#EXTM3U\n"
            content += f"""#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio-AACL-128",LANGUAGE="fr",NAME="Français",DEFAULT=YES,AUTOSELECT=YES,CHANNELS="2",URI="{m3u8_url}{audio_url}"\n"""
            content += f"""#EXT-X-STREAM-INF:BANDWIDTH={bandwidth},AVERAGE-BANDWIDTH={bandwidth-200000},CODECS="avc1.64002A,mp4a.40.2",RESOLUTION={resolution},FRAME-RATE=25.000,AUDIO="audio-AACL-128"\n{m3u8_url}{video_url}\n"""
            return content

        fhd_content = generate_m3u_content(m3u8_url, "1280x720", 4277000, "1.m3u8", "12_0.m3u8")

        os.makedirs(FHD_OUTPUT_DIR, exist_ok=True)

        with open(os.path.join(FHD_OUTPUT_DIR, FHD_OUTPUT_FILE), "w") as f:
            f.write(fhd_content)
        print(f"✅ TF1 généré : {FHD_OUTPUT_FILE}")
    else:
        print("Aucune URL contenant '1.m3u8' trouvée.")
else:
    print(f"Erreur lors de la récupération du fichier: {response.status_code}")