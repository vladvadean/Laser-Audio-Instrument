# LASER AUDIO INSTRUMENT
## Table of Contents :
1. [Introduction](#introduction) 
2. [Installation and Configuration](#installation-and-configuration) 
3. [Concept](#concept) 
4. [Python code analysis](#python-code-analysis) 
5. [Structure](#structure) 
6. [How to use](#how-to-use) 
7. [Improvement](#improvement)

## Introduction
&nbsp;&nbsp;&nbsp;&nbsp;This project aims to convert the light intensity of a red optic laser into audio, using:

 - Arduino Microcontroller
 - A standard USB connection
 - Python data processing and sound design

&nbsp;&nbsp;&nbsp;&nbsp;By measuring the vibrations of a reflexive surface with a red laser which is reflected and its light is captured by a photoresistor, we can process the data of the light's intensity and create a wave. The wave's segments can be mapped to certain musical notes replacing any kind of music instrument.

## Installation and Configuration
Project's requirements:

 -Software:
 - Arduino IDE(or any kind of Arduino software development app)
 - Python(version used: 3.12):
		 -Matplotlib
		 -Pandas
		 -Serial
		 -Scipy.io
		 -NumPy
		 
 -Hardware:
 - Arduino Microcontroller(version used: Arduino ATMEGA 2560)
 - USB 3.0 type A - USB 2.0 type B - **the cable must support data transfer**
 - PC with a USB port
 - Breadboard with:
			-5k ohm resistor
			 -ldr
			 -wire jumpers
			 -red laser module
 
 Files that can be configured:
 - ``arduino.py``
		 - change the variable **com_port** to the port that the arduino usb cable uses
		 - change the variable **baud_rate** to the data transfer speed needed
 - ``create.py``
		 - change the variable **carrier_frequency** and **frequency_deviation** related to the wave created
		 - change the **default_sampling_rate** or call the script by the sampling rates defined

## Concept
&nbsp;&nbsp;&nbsp;&nbsp;The project is based on the physical properties of light relfection and refraction. Having the light reflect of a surface that can easily reflect light, any physical vibration of the surface will result in the quantity of light reflected and refracted. By constantly measuring the quantity of a red laser's light that falls on a photoresistor. If the vibrations are stronger, the quantity of light lost due to the refraction phenomenon is greater and as such we can corelate stronger and lighter taps with different musical notes.  
 &nbsp;&nbsp;&nbsp;&nbsp;With the data collected we obtain data points that we can plot and interpolate them to obtain a function. By modelling a carrier wave with the resulted function we obtain a custom wave that is AM and FM modulated. The musical notes are than mapped to the final wave resulted in the modulation process.  
&nbsp;&nbsp;&nbsp;&nbsp;The sound design component can be easily modified. Things such as the set of musical notes, their frequency, the carrier wave characteristic, the modulation processes which take place only by changing the numerical values of the variables.  
&nbsp;&nbsp;&nbsp;&nbsp;All of the intermediate steps are shown on plots and schematics so the data process can be easily checked.  
&nbsp;&nbsp;&nbsp;&nbsp;Why red? It is the color with one of the highest wavelengths, meaning it is a reliable source of detecting vibration even in a difficult environment: residual light, dust particles in the air, residual electro-magnetic waves etc.

## Python code analysis
&nbsp;&nbsp;&nbsp;&nbsp;For the development of the Python scripts, we will mainly store data in NumPy Arrays, Pandas DataFrame and NumPy cos and sin functions. The Python code is split between 3 scripts for a more easier debugging and for an easier future scaling. The first two scripts are pretty straight forward: the first ones only gets data from the connection and validates it, the second one reads values from a file and assigns each one a value on the time axis so we can plot and create a function on the XOY axis. The third function is the most complex one: by using the SciPy.Interpolate.CubicSpline method we create a function able to connect all the data points. Then by using the NumPy cos method we define the function of a carrier wave that is then modulated with other NumPy cos wave defined function. By using the wavfile import of the SciPy.IO package we can edit the final audio file. For this we need to parse the **combined_signal** and map it's values to certain audio notes, contained in the list **violin_notes**.

## Structure
&nbsp;&nbsp;&nbsp;&nbsp;The project is split between 3 scripts of Python, one Arduino script(the .txt file), and a folder containing all the musical notes a.k.a. `audio`:

   - ``arduino.py``
	   This establishes the connection between the Arduino setup and collects the data transmitted by the microcontroller. Every set of values is written in the terminal and then flushed until the connection is lost or the user cancels it (Ctrl + C). The values are saved in the `received_values.txt`.
   - ``plot.py``
	   Each number from the `received_values.txt` is assigned a time value, based on the **time_interval** variable, and checked if it is valid. Then it is saved in the `data_points.txt`. 
   - ``create.py``
	  Using cubic spline interpolation we obtain a function which passes through of all our data points collected. By modelling a carrier wave with our function and modulating it we obtain a wave that we use for the audio mapping
   - ``sensor.txt`` 
	  A basic script of establishing a connection with the sensor on a certain pin and the serial communication protocol by controlling the baud rate.
   - `audio`
	  A folder containing all the musical notes in a .wav format.
	  
**All the files should be added in the same path**
	  
## How to use
&nbsp;&nbsp;&nbsp;&nbsp;After downloading the repo and configuring the breadboard with all the required components, upload the Arduino code on the microcontroller. Then run the `arduino.py` script and let it run as long as you want to record the laser. After that run the `plot.py` and the `create.py` scripts. You will obtain the audio file `combined_file.wav` depending on the notes selected in the `audio` folder.
## Improvement 

 1. Develop the wave in such manner that it does not need mapping and is the final audio result.
 2. Make the audio be played in real-time.
 3. Create a GUI for the project.
