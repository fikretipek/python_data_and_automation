import whisper
import ffmpeg
import os
import numpy as np
import soundfile as sf

# ---- AYARLAR ----
video_path = r"C:\Test\output.mp4"
audio_path = r"C:\Test\temp_audio.wav"
srt_path = r"C:\Test\output.srt"
language = "en"
model_size = "base"
ffmpeg_exe = r"C:\ffmpeg\bin\ffmpeg.exe"  # kendi sisteminize göre

# 1️⃣ Videodan WAV çıkar
print("🔹 Videodan ses çıkarılıyor...")
(
    ffmpeg
    .input(video_path)
    .output(audio_path, ar=16000, ac=1)
    .run(cmd=ffmpeg_exe, overwrite_output=True, quiet=True)
)

# 2️⃣ Whisper modelini yükle
print(f"🔹 Whisper '{model_size}' modeli yükleniyor...")
model = whisper.load_model(model_size)

# 3️⃣ WAV dosyasını yükle
print("🔹 WAV dosyası numpy array olarak yükleniyor...")
audio, sr = sf.read(audio_path)
if len(audio.shape) > 1:
    audio = np.mean(audio, axis=1)  # stereo ise mono yap
audio = audio.astype(np.float32)    # ⚡ float32 yap

# 4️⃣ Transkription
print("🔹 Altyazı oluşturuluyor...")
result = model.transcribe(audio, language=language, fp16=False)

# 5️⃣ SRT formatına çevir ve kaydet
print("🔹 SRT dosyası oluşturuluyor...")
def format_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

with open(srt_path, "w", encoding="utf-8") as f:
    for i, seg in enumerate(result["segments"], 1):
        start = format_timestamp(seg["start"])
        end = format_timestamp(seg["end"])
        text = seg["text"].strip()
        f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

print(f"✅ Altyazı oluşturuldu: {srt_path}")

# 6️⃣ Geçici audio dosyasını sil
os.remove(audio_path)
print("🗑️ Geçici dosya silindi.")
