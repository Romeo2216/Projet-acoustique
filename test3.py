import wave

def get_wav_duration(file_path):
    with wave.open(file_path, "r") as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
    return duration

# Exemple d'utilisation
file_path = "Signal_Response/y_out_1.wav"
duration = get_wav_duration(file_path)
print(f"La durée du fichier WAV est de {duration:.2f} secondes.")