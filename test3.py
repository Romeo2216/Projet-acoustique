import sqlite3
import sounddevice as sd
import soundfile as sf

# Connexion à SQLite
connexion = sqlite3.connect("signal.db")
cursor = connexion.cursor()

cursor.execute("SELECT * FROM Test_order WHERE rowid = ?",(1,))
row = cursor.fetchone()

A_index = row[1]
B_index = row[2]

cursor.execute("SELECT * FROM Combination WHERE rowid = ?",(A_index,))
row = cursor.fetchone()

A_file_name = row[5]

cursor.execute("SELECT * FROM Combination WHERE rowid = ?",(B_index,))
row = cursor.fetchone()

B_file_name = row[5]

s, sampling_rate = sf.read("Signal_Response/" + str(A_file_name))

sd.play(s,samplerate=sampling_rate)
sd.wait()