import sounddevice as sd
import soundfile as sf

signal, sampling_rate = sf.read("Signal_Response\y_out_1.wav")
sd.play(signal, samplerate=sampling_rate)
sd.wait()