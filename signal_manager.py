import numpy as np
import sqlite3
from librosa import load
from scipy import signal
import init_db as db
from scipy.io.wavfile import write

connection = sqlite3.connect("signal.db")

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

def orientation(signal):
    if len(np.shape(signal)) == 2 and np.argmax(np.shape(signal)) == 1:
        signal = signal.T

    return signal

def normalize_signal(signal):
    return signal*(0.99/np.amax(np.absolute(signal)))

def convolv_signal(list_two_signals):

    """plt.subplot(2,1,1)
    plt.plot(list_two_signals[0])

    plt.subplot(2,1,2)
    plt.plot(list_two_signals[1])
    plt.show()"""

    mono = True

    for i in range(len(list_two_signals)):
        list_two_signals[i] = reduce_signal_size(list_two_signals[i])

        if len(np.shape(list_two_signals[i])) > 1:
            mono = False
   
    list_two_signals = resize_signal(list_two_signals)  
    
    if mono:    

        return signal.fftconvolve(list_two_signals[0], list_two_signals[1], mode = 'full')

    else:
        for i in range(len(list_two_signals)):
            if len(np.shape(list_two_signals[i])) > 1:
                stereo_signal = list_two_signals[i]
                mono_signal = list_two_signals[i-1]

        right_signal = signal.fftconvolve(stereo_signal[:,0], mono_signal, mode = 'full')
        left_signal = signal.fftconvolve(stereo_signal[:,1], mono_signal, mode = 'full')

        stereo_list = resize_signal([right_signal,left_signal])

        signal_final = np.zeros((len(stereo_list[0]),2))

        signal_final[:,0] = stereo_list[0]
        signal_final[:,1] = stereo_list[1]

        return signal_final

def generate_signal(Iexi, Ihead, Iface, Iir, Combi_id, desired_sampling_rate = 48000):
   
    HRTF, sampling_rate = load("HRTF/" + db.get_file_name(Iface, "HRTF"), sr=desired_sampling_rate, mono = False)
    OBTF, sampling_rate = load("OBTF/" + db.get_file_name(Ihead, "OBTF"), sr=desired_sampling_rate, mono = False)
    y_rir, sampling_rate = load("Impulse_Response/" + db.get_file_name(Iir, "Impulse_Response"), sr=desired_sampling_rate)
    y_exi, sampling_rate = load("Excitation_Files/" + db.get_file_name(Iexi, "Excitation_Files"), sr=desired_sampling_rate)
    
    y_rir_reduce = reduce_signal_size(y_rir)
    y_dir, y_refl, split_index = split_signal(y_rir_reduce)

    y_obrir_1 = convolv_signal([y_dir,orientation(HRTF)])
    y_obrir_2 = convolv_signal([y_refl,orientation(OBTF)])

    y_obrir = np.append(y_obrir_1[:split_index],y_obrir_2, axis = 0)

    y_out = convolv_signal([y_exi,y_obrir])

    y_out_reduce = reduce_signal_size(y_out)

    y_out_final = normalize_signal(y_out_reduce)

    if len(y_out_final) < 8000:
        y_out_final = np.append(y_out_final,np.zeros((8000 - len(y_out_final),2)), axis = 0)

    audio_data_int16 = (y_out_final * 32767).astype(np.int16)

    file_name = "y_out_" + str(Combi_id) + ".wav"

    write("Signal_Response/" + file_name, desired_sampling_rate, audio_data_int16)
   
    return file_name





   