import whisper
import subprocess
import os
import numpy as np
import soundfile as sf
import torch
import re

# ---- AYARLAR ----
input_dir   = r"./"
ffmpeg_exe  = r"C:\ffmpeg\bin\ffmpeg.exe"
language    = "en"
model_size  = "base"
normalize_names = False   # True yaparsan dosya adlarını güvenli hale getirir (boşluk -> "_")

# 🔹 GPU kontrolü
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🔹 Çalışma cihazı: {device}")

# Whisper modeli bir kez yükleniyor
print(f"🔹 Whisper '{model_size}' modeli yükleniyor...")
model = whisper.load_model(model_size, device=device)

def format_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def safe_filename(name):
    """Dosya isimlerini normalize et (boşluk->_, özel karakterleri sil)."""
    name = re.sub(r"[^\w\-\.]", "_", name)  # sadece harf, rakam, _, -, .
    return name

# Klasördeki tüm .ts dosyalarını sırayla işle
for file in os.listdir(input_dir):
    if file.lower().endswith(".ts"):
        base_name = os.path.splitext(file)[0]
        if normalize_names:
            base_name = safe_filename(base_name)

        video_path = os.path.join(input_dir, file)
        audio_path = os.path.join(input_dir, f"{base_name}_temp.wav")
        srt_path   = os.path.join(input_dir, f"{base_name}.srt")

        print(f"\n▶ İşleniyor: {file}")

        # 1️⃣ Videodan WAV çıkar
        subprocess.run([
            ffmpeg_exe,
            "-y",
            "-i", video_path,
            "-ar", "16000",
            "-ac", "1",
            audio_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 2️⃣ WAV dosyasını yükle
        audio, sr = sf.read(audio_path)
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)  # stereo → mono
        audio = audio.astype(np.float32)

        # 3️⃣ Transkripsiyon
        result = model.transcribe(audio, language=language, fp16=(device=="cuda"))

        # 4️⃣ SRT kaydet
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, seg in enumerate(result["segments"], 1):
                start = format_timestamp(seg["start"])
                end = format_timestamp(seg["end"])
                text = seg["text"].strip()
                f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

        print(f"✅ Altyazı oluşturuldu: {srt_path}")

        # 5️⃣ Geçici wav dosyasını sil
        os.remove(audio_path)
        print("🗑️ Geçici ses dosyası silindi.")

print("\n--- Tüm işler tamamlandı! ---")
