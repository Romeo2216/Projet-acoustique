import sounddevice as sd
import soundfile as sf
import init_db as db
import shutil
import os
import threading

dossier = "Signal_Response"

if os.path.exists(dossier):
    shutil.rmtree(dossier)

os.mkdir(dossier)

db.clear_db()

db._init_db()

db.save_conbination()

order = db.generate_test()

db.load_signal(order)

"""s, sampling_rate = sf.read("Signal_Response/y_out_1.wav")

sd.play(s,samplerate=sampling_rate)
sd.wait()"""