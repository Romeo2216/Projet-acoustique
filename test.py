import soundfile as sf
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import librosa

connection = sqlite3.connect("test.db")

cursor = connection.cursor()

def split_signal(signal, Db_cap = 60, interval_size = 1):
    
    sensitivity = max(np.absolute(signal)) * 10**(-Db_cap/20)

    interval = len(signal)//(100 * interval_size)

    for i in range(1,len(signal) - interval,interval):  

        if np.mean(abs(signal[i:i+interval])) < sensitivity:
            if i % 2 == 1:
                j = i+1

            y_dir = signal[0:j]
            y_refl = signal[j:]
            break

    return y_dir, y_refl, j

def resize_signal(list_signals):

    if len(list_signals) < 2:
        return list_signals

    len_signal = [0]*len(list_signals)

    for i in range(len(list_signals)):
        len_signal[i] = max(np.shape(list_signals[i]))

    longer_index = np.argmax(len_signal)

    for i in range(len(list_signals)):

        if i == longer_index:
            continue
        
        if len(np.shape(list_signals[i])) == 2:
            list_signals[i] = np.append(list_signals[i],np.zeros((len_signal[longer_index] - len_signal[i],2)), axis = 0)
        else:
            list_signals[i] = np.append(list_signals[i],np.zeros(len_signal[longer_index] - len_signal[i]))

    return list_signals

def get_file_name(i, folder):

    cursor.execute("SELECT * FROM " + folder)
    rows = cursor.fetchall()
    file_name = rows[i]

    return "".join(file_name)

def reduce_signal_size(signal, Db_cap = 60):

    if len(np.shape(signal)) == 2 and np.argmax(np.shape(signal)) == 1:
        signal = signal.T

    sensitivity = np.amax(np.absolute(signal)) * 10**(-Db_cap/20)

    is_start_found = True
    is_end_found = True

    start = 0
    end = len(signal) - 1

    for i in range(1,max(np.shape(signal))):

        if np.amax(np.absolute(signal[i])) > sensitivity and is_start_found:
            start = i
            is_start_found = False

        if np.amax(np.absolute(signal[-i])) > sensitivity and is_end_found:
            end = -i
            is_end_found = False

    if (end-start) % 2 == 1:
        end += -1

    return signal[start:end]

def normalize_signal(signal):
    return signal*(0.99/np.amax(np.absolute(signal)))

def convolv_signal(list_two_signals):

    mono = True

    for i in range(len(list_two_signals)):
        list_two_signals[i] = reduce_signal_size(list_two_signals[i])

        if len(np.shape(list_two_signals[i])) > 1:
            mono = False
   
    list_two_signals = resize_signal(list_two_signals)  
    
    if mono:    

        return np.convolve(list_two_signals[0], list_two_signals[1])

    else:
        for i in range(len(list_two_signals)):
            if len(np.shape(list_two_signals[i])) > 1:
                stereo_signal = list_two_signals[i]
                mono_signal = list_two_signals[i-1]

        right_signal = np.convolve(stereo_signal[:,0], mono_signal)
        left_signal = np.convolve(stereo_signal[:,1], mono_signal)

        return right_signal

def convo(Iexi, Ihead, Iface, Iir, desired_sampling_rate = 48000):
   
    HRTF, sampling_rate = librosa.load("TF_Head/" + get_file_name(Iface, "TF_Head"), sr=desired_sampling_rate, mono = False)
    OBTF, sampling_rate = librosa.load("TF_Head/" + get_file_name(Ihead, "TF_Head"), sr=desired_sampling_rate, mono = False)
    y_rir, sampling_rate = librosa.load("Impulse_Reponse/" + get_file_name(Iir, "Impulse_Reponse"), sr=desired_sampling_rate)
    y_exi, sampling_rate = librosa.load("Excitation_Files/" + get_file_name(Iexi, "Excitation_Files"), sr=desired_sampling_rate)
    
    y_rir_reduce = reduce_signal_size(y_rir)
    y_dir, y_refl, split_index = split_signal(y_rir_reduce)

    y_obrir_1 = convolv_signal([y_dir,HRTF])
    y_obrir_2 = convolv_signal([y_refl,OBTF])

    y_obrir = np.append(y_obrir_1[:split_index],y_obrir_2)

    y_out = convolv_signal([y_exi,y_obrir])

    y_out_reduce = reduce_signal_size(y_out)

    y_out_final = normalize_signal(y_out_reduce)
   
    sd.play(y_out_final, samplerate=48000)
    sd.wait()

    plt.plot(y_out_final)
    plt.show()


convo(1,0,1,1)

"""y_exi, sampling_rate = sf.read("Excitation_Files/click.wav")

y_exi2, sampling_rate = sf.read("Impulse_Reponse/CircularWall_D150.wav")

#y_exi = y_exi[:,0]



new_y_exi_1 = reduce_signal_size(y_exi2)



plt.subplot(2,1,1)
plt.plot(y_exi2)

plt.subplot(2,1,2)
plt.plot(new_y_exi_1)
plt.show()"""
