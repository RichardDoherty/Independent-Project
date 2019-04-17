# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:09:26 2019

@author: Richard
"""
#log10 used for converting FFT power results to Decibles
from math import log10

#matplot lib used to plot results of FFT
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#tkinter used to create GUI
import tkinter
import tkinter.messagebox

#used for various numberical calculations 
import numpy as np

#used for .wav import, FFT calculations, and mannwhitney nonpramatic hypothesis test
from scipy.io import wavfile
from scipy.fftpack import fft
from scipy.stats import mannwhitneyu

main = tkinter.Tk()

#Assigned to compare button
#Description: Loads .wav files, runs a FFT transform on the data, plots the results, and runs a 
#             hypothesis test comparing the results 
#Pre Conditions: All packages are imported properly and file paths have been added to the two entry boxes
#Post Conditions: Outputs a mannwhitney p-value, absolute difference, and a plot of the two samples FFT results
def run_FFT():
    
   #get file paths from entry boxes
   path_1 = entry_1.get()
   path_2 = entry_2.get()
   
   #Try to load each  file and with each exception caught create a message box to know what file failed
   valid_files = True   #boolean to track if an exception was caught or not
   try:
       fs_1, audio_data_1 = wavfile.read(path_1)
   except:
       tkinter.messagebox.showerror("File Error", "File Path for Sample 1 is Invalid")
       valid_files = False

   try:
       fs_2, audio_data_2 = wavfile.read(path_2)
   except:
       tkinter.messagebox.showerror("File Error", "File Path for Sample 2 is Invalid")
       valid_files = False
       
                            ########### CALCULATIONS BELOW ############
                            #Check to ensure that the audio samples are the 
   if (valid_files == True) and (fs_1 == fs_2):
        print("Files successfully loaded")
        #create a variable for the number of point analyzed from each sample
        #in order for the FFT to run properly number of point analyzed for each sample must be equal
        #assign the N variable witht the lesser number of samples present in the two samples
        if len(audio_data_1) <= len(audio_data_2):    
            N = len(audio_data_1)
        else: 
            N = len(audio_data_2)
        
        #Audio data per sample is read in as a 2xN dimensional array of sound output 
        #the two rows corresond to the left and right speaker
        #Calculate the average of the two values and calculate the FFT of the output 
        #Store the values for the two samples in a Nx2 array
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

    
        #the output of the FFT is real and imaginary frequencies
        #calculate the magintude of the real and imaginary frequency for the two samples and store in a Nx2 array
        FFT_data = []
        cols = np.int(N/2)
        for row in range(0,2):
            temp_Row = []
            temp_Row = (2/N * np.abs(data[row][0:cols]))
            FFT_data.append(temp_Row)        
        
        
        #variable to store the abs difference between the samples
        abs_diff = 0
        
        #convert the FFT power magniture to Decibles
        for col in range(0, cols):
            FFT_data[0][col] = 20*log10(FFT_data[0][col])
            FFT_data[1][col] = 20*log10(FFT_data[1][col])
            abs_diff += abs(FFT_data[0][col] - FFT_data[1][col])
            
        #Run a non-paramatic test to test the samilarity of the two samples
        stat, p_val = mannwhitneyu(FFT_data[0], FFT_data[1], use_continuity = True, alternative = "two-sided")
        
        #Unlock the output for the abs difference entry box, clear it, input the abs diff. and relock
        abs_diff_output.configure(state = "normal")
        abs_diff_output.delete(0, tkinter.END)
        abs_diff_output.insert(0, abs_diff)
        abs_diff_output.configure(state = "readonly")
        
        #Unlock the output for the p-val entry box, clear it, input the p-val and relock
        p_val_output.configure(state = "normal")
        p_val_output.delete(0, tkinter.END)
        p_val_output.insert(0, p_val)
        p_val_output.configure(state = "readonly")
        
        #calculate the time array for plotting
        dt = 1.0/ fs_1 
        t = np.linspace(0.0, 1.0/(2.0*dt),int(N/2))
        
        #plot the FFT result from the two samples
        plt.clear()
        plt.plot(t, FFT_data[0][:])
        plt.plot(t, FFT_data[1][:])
        plt.set_xlabel("Frequency")
        plt.set_ylabel("dB")
        plt.set_xlim(100, 14000)
        plt.set_ylim(-100, -40)
        canvas = FigureCanvasTkAgg(f, master=main)
        canvas.draw()
        canvas.get_tk_widget().grid(row=6, column=1, rowspan=3, columnspan=5)
   else:
        #if the samples weren't valid then show that the sampling frequency was not valid
        if (valid_files == True):
            tkinter.messagebox.showerror("Sample Frequency Error", "Incompatible Sampling Frequencies from Files")

#Create window title and display title for GUI 
main.title("Fast Fourier Transform")
main.geometry("750x600")
label = tkinter.Label( main, text = "FFT Analysis", font=("bold", 24))
label.grid(row=0,column=1,columnspan=2)

#create entry boxes for the two sample audio files
entry_label_1 = tkinter.Label(main, text = "Audio Sample 1 File Path: ")
entry_label_1.grid(row=1,column=0)
entry_1 = tkinter.Entry(main, bd = 5, width=75)
entry_1.grid(row=1,column=1, columnspan=2)

entry_label_2 = tkinter.Label(main, text = "Audio Sample 2 File Path: ")
entry_label_2.grid(row=2, column=0)
entry_2 = tkinter.Entry(main, bd = 5, width=75)
entry_2.grid(row=2, column=1, columnspan=2)

#create entry box for the absolute differnce in data
abs_diff_label = tkinter.Label(main, text = "Absolute Difference: ")
abs_diff_label.grid(row=3,column=0, sticky="E")
abs_diff_output = tkinter.Entry(main, bd = 5, state = "readonly")
abs_diff_output.grid(row=3,column=1, sticky="W")

#create entry box for the p-value of the mannwhitney hypothesis test
p_val_label = tkinter.Label(main, text = "P Value: ")
p_val_label.grid(row=4, column=0, sticky="E")
p_val_output = tkinter.Entry(main, bd = 5, state = "readonly")
p_val_output.grid(row=4, column=1, sticky="W")

#compare button that runs the FFT function
compare_bttn = tkinter.Button(main, text = "   Compare Samples   ", command = run_FFT)
compare_bttn.grid(row=4, column=1, sticky="E")

f = Figure(figsize=(5, 4), dpi=100)
plt = f.add_subplot(111)

main.grid_rowconfigure(5, minsize=25)  # Here
main.mainloop()