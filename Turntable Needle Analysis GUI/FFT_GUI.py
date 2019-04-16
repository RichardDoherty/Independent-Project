# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:09:26 2019

@author: Richard
"""

# implement the default mpl key bindings
from math import log10
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import tkinter
import tkinter.messagebox

import numpy as np

from scipy.io import wavfile
from scipy.fftpack import fft
from scipy.stats import mannwhitneyu

main = tkinter.Tk()

def run_FFT():
   path_1 = entry_1.get()
   path_2 = entry_2.get()
   
   valid_files = True
   try:
       #fs_1, audio_data_1 = wavfile.read("C:/Users/Richard/Desktop/IE_497_498/FFT/Conical/PinkNoise_Conical.wav")
       fs_1, audio_data_1 = wavfile.read(path_1)
   except:
       tkinter.messagebox.showerror("File Error", "File Path for Sample 1 is Invalid")
       valid_files = False

   try:
       #fs_2, audio_data_2 = wavfile.read("C:/Users/Richard/Desktop/IE_497_498/FFT/Conical/PinkNoise_SAS.wav")
       fs_2, audio_data_2 = wavfile.read(path_2)
   except:
       tkinter.messagebox.showerror("File Error", "File Path for Sample 2 is Invalid")
       valid_files = False
       
                            ########### CALCULATIONS BELOW ############
                            #Check to ensure that the audio samples are the 
   if (valid_files == True) and (fs_1 == fs_2):
        print("Files successfully loaded")
        if len(audio_data_1) <= len(audio_data_2):    
            N = len(audio_data_1)
        else: 
            N = len(audio_data_2)
            
        print(N)
        
        data = []
        for col in range(0, 2):
            temp_Row = []
            for row in range(0, N):
            #audio data arrays have N rows and 2 cols
            #our array must be structured to have N cols and 2 rows so that
            #the fft can be calculated for each row.
                if col == 0:
                    temp_Row.append((audio_data_1[row][0] + audio_data_1[row][1])/2)
                else: 
                    temp_Row.append((audio_data_2[row][0] + audio_data_2[row][1])/2)
            data.append(fft(temp_Row))
        print("Merged left and right speakers")
    
        #dt = 1.0/ fs_1 
        #t = np.linspace(0.0, 1.0/(2.0*dt),int(N/2))
    
        FFT_data = []
        cols = np.int(N/2)
        for row in range(0,2):
            temp_Row = []
            temp_Row = (2/N * np.abs(data[row][0:cols]))
            FFT_data.append(temp_Row)        
        print("Fourier Power Data Calculated")
        dt = 1.0/ fs_1 
        t = np.linspace(0.0, 1.0/(2.0*dt),int(N/2))
        sum_of_squares_diff = 0
        for col in range(0, cols):
            FFT_data[0][col] = 20*log10(FFT_data[0][col])
            FFT_data[1][col] = 20*log10(FFT_data[1][col])
            sum_of_squares_diff += abs(FFT_data[0][col] - FFT_data[1][col])
    
        stat, p_val = mannwhitneyu(FFT_data[0], FFT_data[1], use_continuity = True, alternative = "two-sided")
        
        sum_squares_output.configure(state = "normal")
        sum_squares_output.delete(0, tkinter.END)
        sum_squares_output.insert(0, sum_of_squares_diff)
        sum_squares_output.configure(state = "readonly")
        
        p_val_output.configure(state = "normal")
        p_val_output.delete(0, tkinter.END)
        p_val_output.insert(0, p_val)
        p_val_output.configure(state = "readonly")
        print("Adding subplot")
        
        print("Subplot added")
        
        plt.clear()
        plt.plot(t, FFT_data[0][:])
        plt.plot(t, FFT_data[1][:])
        plt.set_xlabel("Frequency")
        plt.set_ylabel("dB")
        plt.set_xlim(100, 14000)
        plt.set_ylim(-100, -40)
        # a tk.DrawingArea
        canvas = FigureCanvasTkAgg(f, master=main)
        canvas.draw()
        canvas.get_tk_widget().grid(row=6, column=1, rowspan=3, columnspan=5)

        

        
   else:
        if (valid_files == True):
            tkinter.messagebox.showerror("Sample Frequency Error", "Incompatible Sampling Frequencies from Files")


main.title("Fast Fourier Transform")
main.geometry("750x600")
label = tkinter.Label( main, text = "FFT Analysis", font=("bold", 24))
label.grid(row=0,column=1,columnspan=2)

entry_label_1 = tkinter.Label(main, text = "Audio Sample 1 File Path: ")
entry_label_1.grid(row=1,column=0)
entry_1 = tkinter.Entry(main, bd = 5, width=75)
entry_1.grid(row=1,column=1, columnspan=2)

entry_label_2 = tkinter.Label(main, text = "Audio Sample 2 File Path: ")
entry_label_2.grid(row=2, column=0)
entry_2 = tkinter.Entry(main, bd = 5, width=75)
entry_2.grid(row=2, column=1, columnspan=2)

sum_squares_label = tkinter.Label(main, text = "Sum of Squares Difference: ")
sum_squares_label.grid(row=3,column=0, sticky="E")
sum_squares_output = tkinter.Entry(main, bd = 5, state = "readonly")
sum_squares_output.grid(row=3,column=1, sticky="W")

p_val_label = tkinter.Label(main, text = "P Value: ")
p_val_label.grid(row=4, column=0, sticky="E")
p_val_output = tkinter.Entry(main, bd = 5, state = "readonly")
p_val_output.grid(row=4, column=1, sticky="W")

compare_bttn = tkinter.Button(main, text = "   Compare Samples   ", command = run_FFT)
compare_bttn.grid(row=4, column=1, sticky="E")

f = Figure(figsize=(5, 4), dpi=100)
plt = f.add_subplot(111)

main.grid_rowconfigure(5, minsize=25)  # Here
main.mainloop()