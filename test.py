import soundfile as sf
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

connection = sqlite3.connect("test.db")

cursor = connection.cursor()

def split_signal(signal):
    b = False
    sensitivity = max(signal) / 1000

    for i in range(1,len(signal) - 1):  
        
        if signal[i] > sensitivity:
            b = True

        if (abs(signal[i+1] - signal[i-1]) < 0.001) and (abs(signal[i]) < sensitivity) and b:
            y_dir = signal[0:i]
            y_refl = signal[i:]
            break

    return y_dir, y_refl

def resize_signal(list_signals):

    if len(list_signals) < 2:
        return list_signals

    len_signal = [0]*len(list_signals)

    for i in range(len(list_signals)):
        len_signal[i] = len(list_signals[i])

    longer_index = np.argmax(len_signal)

    for i in range(len(list_signals)):

        if i == longer_index:
            continue

        list_signals[i] = np.append(list_signals[i],np.zeros(len_signal[longer_index] - len_signal[i]))

    return list_signals

def get_file_name(i, folder):

    cursor.execute("SELECT * FROM " + folder)
    rows = cursor.fetchall()
    file_name = rows[i]

    return "".join(file_name)

def convo(Iexi, Ihead, Iface, Iir):

    HRTF, sampling_rate = sf.read("TF_Head/" + get_file_name(Iface, "TF_Head"))
    OBTF, sampling_rate = sf.read("TF_Head/" + get_file_name(Ihead, "TF_Head"))
    y_rir, sampling_rate = sf.read("Impulse_Reponse/" + get_file_name(Iir, "Impulse_Reponse"))
    y_exi, sampling_rate = sf.read("Excitation_Files/" + get_file_name(Iexi, "Excitation_Files"))

    y_dir, y_refl = split_signal(y_rir)

    Left_HRTF = HRTF[:,0]
    Right_HRTF = HRTF[:,1]
    Left_OBTF = OBTF[:,0]
    Right_OBTF = OBTF[:,1]

    signals = [y_dir, y_refl, y_exi, Left_HRTF, Right_HRTF, Left_OBTF, Right_OBTF]

    signals = resize_signal(signals)

    HL = np.convolve(signals[0], signals[5])
    HR = np.convolve(signals[0], signals[6])
    OL = np.convolve(signals[1], signals[3])
    OR = np.convolve(signals[1], signals[4])

    R = HR + OR
    L = HL + OL

    signals2 = resize_signal([R,y_exi])


    Rf = np.convolve(signals2[0],signals2[1])

    Rf = Rf*(1/max(Rf))

    sd.play(Rf, samplerate=sampling_rate)
    sd.wait()

    plt.plot(Rf)
    plt.show()


convo(1,0,1,1)
