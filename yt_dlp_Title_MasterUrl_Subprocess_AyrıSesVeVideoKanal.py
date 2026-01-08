import subprocess

# ---------- Dosya Yolları ----------
urls_file = "MasterUrl.txt"
titles_file = "Titles.txt"

# ---------- Dosyaları Oku ----------
with open(urls_file, "r", encoding="utf-8") as f_urls:
    urls = [line.strip() for line in f_urls if line.strip()]

with open(titles_file, "r", encoding="utf-8") as f_titles:
    titles = [line.strip() for line in f_titles if line.strip()]

# ---------- Kontrol ----------
if len(urls) != len(titles):
    print("Hata: URL ve Title sayısı eşleşmiyor!")
    exit()

# ---------- Her video için yt-dlp çalıştır ----------
for url, title in zip(urls, titles):
    # Başlık kullanımı, illegal karakterler _ ile değiştirilir
    safe_title = title.replace("\\", "").replace("/", "").replace(":", "")\
                      .replace("?", "").replace('"', "").replace("<", "")\
                      .replace(">", "").replace("|", "")

    cmd = [
        "yt-dlp",
        "-f", "bestvideo+bestaudio/best",
        #"-f", "bestvideo[height=1080]+bestaudio/best",
        "--merge-output-format", "mp4",
        url,
        "-o", f"{safe_title}.mp4"
    ]
    print(f"İndiriliyor: {safe_title}.mp4")
    subprocess.run(cmd)
#bu yt-dlp e göre biraz yavaş  ancak, lenght , Frame height, Frame widht değerlerini basıyor. 
#WARNING: Live HLS streams are not supported by the native downloader. If this is a livestream, please add "--downloader ffmpeg --hls-use-mpegts" to your command - ama bu sıkıntı olmuyor.