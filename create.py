import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline
import sounddevice as sd
from pydub import AudioSegment
from pydub.playback import play
from playsound import playsound
from scipy.io import wavfile

sampling_rate_1X = 1
sampling_rate_2X = 2
sampling_rate_10X = 10
sampling_rate_100X = 100
sampling_rate_1000X = 1000

default_sampling_rate = 10

# in Hz
carrier_frequency = 8000
frequency_deviation = 1000

import sys

sampling_rate = default_sampling_rate

# choose the sampling rate from script argv parameter
if len(sys.argv) > 1:
    match sys.argv[1]:
        case "1x":
            sampling_rate = sampling_rate_1X
        case "2x":
            sampling_rate = sampling_rate_2X
        case "10x":
            sampling_rate = sampling_rate_10X
        case "100x":
            sampling_rate = sampling_rate_100X
        case "1000x":
            sampling_rate = sampling_rate_1000X
        case _:
            sampling_rate = default_sampling_rate

file_csv = open("data_points.txt","r")
lines = file_csv.readlines()

# extract the total time the signal was emitted
final_line = lines[-1]
final_line = final_line.strip().split(',')
total_time = final_line[0]

# sample values from the csv file according to sampling_rate
lines = lines[0::sampling_rate]
lines = [line.strip().split(',') for line in lines]
time = [float(line[0]) for line in lines]
values = [int(line[1]) for line in lines]
data = pd.DataFrame({'values': values, 'time': time})
plt.figure(figsize=(10, 10))
plt.plot(data['time'], data['values'], marker='x')
plt.title('Data Chosen')
plt.xlabel('Time')
plt.ylabel('Values')
plt.grid(True)
plt.show()

### spline interpolation on the sets of data received

# perform cubic spline interpolation
cs = CubicSpline(data['time'], data['values'])

# generate a range of time values for plotting the spline
time_spline = np.linspace(min(data['time']), max(data['time']), 500)

# Use the spline function to get interpolated values
values_spline = cs(time_spline)

# plot the original data points and the interpolated spline
plt.figure(figsize=(12, 10))
plt.plot(data['time'], data['values'], 'x', label='Original Data')
plt.plot(time_spline, values_spline, label='Cubic Spline')
plt.xlim(min(data['time']), max(data['time']))
plt.ylim(min(data['values']), max(data['values']))
plt.title('Cubic Spline Interpolation of Data Chosen')
plt.xlabel('Time')
plt.ylabel('Values')
plt.legend()
plt.show()

### amplitude modulation

# generate the carrier wave
carrier_wave = np.cos(2 * np.pi * carrier_frequency * time_spline)

# perform the amplitude modulation
am_modulated_signal = values_spline * carrier_wave

# perform the frequency modulation
fm_modulated_signal = np.cos(2 * np.pi * carrier_frequency * time_spline 
                             + frequency_deviation * np.cumsum(values_spline) / len(time_spline))

# combine the am and fm signals
combined_signal = am_modulated_signal + fm_modulated_signal
    
### show the final result
plt.figure(figsize=(12, 18))
plt.subplot(5, 1, 1)
plt.plot(time_spline, values_spline, label="Original Signal")
plt.title("Original Signal")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.legend()

plt.subplot(5, 1, 2)
plt.plot(time_spline, carrier_wave, label="Carrier Signal")
plt.title("Carrier Signal")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.legend()

plt.subplot(5, 1, 3)
plt.plot(time_spline, am_modulated_signal, label="AM Modulated Signal")
plt.title("AM Modulated Signal")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.legend()

plt.subplot(5, 1, 4)
plt.plot(time_spline, fm_modulated_signal, label="FM Modulated Signal")
plt.title("FM Modulated Signal")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.legend()

plt.subplot(5, 1, 5)  
plt.plot(time_spline, combined_signal, label="Combined AM and FM Signal")
plt.title("Combined AM and FM Modulated Signal")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.legend()

plt.subplots_adjust(hspace=1)

plt.show()

### generate wav files from the instrument notes

# get instrument notes
# 3000 ms the average length of a .wav file
step = int(float(total_time))//3000 
violin_notes = []
violin_notes.append("audio/355893__mtg__violin-a3.wav")
violin_notes.append("audio/355828__mtg__violin-asharp4.wav")
violin_notes.append("audio/355777__mtg__violin-b5.wav")
violin_notes.append("audio/355808__mtg__violin-c4.wav")
violin_notes.append("audio/356138__mtg__violin-csharp6.wav")
violin_notes.append("audio/355796__mtg__violin-d4.wav")
violin_notes.append("audio/355992__mtg__violin-dsharp5.wav")
violin_notes.append("audio/355976__mtg__violin-e4.wav")
violin_notes.append("audio/356145__mtg__violin-f4.wav")
violin_notes.append("audio/356135__mtg__violin-fsharp4.wav")
violin_notes.append("audio/355979__mtg__violin-g3.wav")
violin_notes.append("audio/356176__mtg__violin-gsharp4.wav")

# beginning low pitch
sample_rate, main_data = wavfile.read("audio/356176__mtg__violin-gsharp4.wav")

# append notes to form the output file
for i in  combined_signal[::step]:

    match True:
        case _ if i > 769.0:
            sample_rate, data_aux = wavfile.read(violin_notes[0])
        case _ if 744.0 < i and i <= 769.0:  
            sample_rate, data_aux = wavfile.read(violin_notes[1])
        case _ if 730.0 < i and i <= 744.0:  
            sample_rate, data_aux = wavfile.read(violin_notes[2])
        case _ if 700.0 < i and i <= 730.0:
            sample_rate, data_aux = wavfile.read(violin_notes[3])
        case _ if 670.0 < i and i <= 700.0:
            sample_rate, data_aux = wavfile.read(violin_notes[4])
        case _ if 640.0 < i and i <= 670.0:
            sample_rate, data_aux = wavfile.read(violin_notes[5])
        case _ if 610.0 < i and i <= 640.0:
            sample_rate, data_aux = wavfile.read(violin_notes[6])
        case _ if 580.0 < i and i <= 610.0:
            sample_rate, data_aux = wavfile.read(violin_notes[7])
        case _ if 580.0 >= i:
            sample_rate, data_aux = wavfile.read(violin_notes[8])  

    main_data = np.concatenate((main_data, data_aux)) 

# output the resulted file     
wavfile.write("combined_file.wav", sample_rate, main_data)

# play the audio
playsound("combined_file.wav")

