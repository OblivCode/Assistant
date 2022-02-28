from vosk import Model, KaldiRecognizer, SetLogLevel
from queue import Queue
from threading import Thread
import modules.logger as log
import numpy as np
import pyaudio, wave, os, sys, winsound, json

chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100
filename = './resources/temp/speech.wav'
vosk_model_filename ='./resources/vosk-model'

SetLogLevel(-1)

class engine():
    def __init__(self):
        self.pyaudio = pyaudio.PyAudio()
        self.l_queue = Queue()
        self.model = Model(vosk_model_filename)
        

        self.input_stream = self.pyaudio.open(format=sample_format,
        channels=channels, rate=fs,
        frames_per_buffer=chunk,
        input=True)
        self.input_stream.stop_stream()

        self.listening = False
    
    def start_listen(self):
        print(self.listening)
        if self.listening:
            return
        self.listening = True

        frames = []

        #store data 
        def func():
            self.input_stream.start_stream()
            print('started listening')
            
            for i in range(0, int(fs/chunk * 60)):
                data = self.input_stream.read(chunk)
                frames.append(data)
                
                try:
                    if self.l_queue.get_nowait():
                        break
                except:
                    pass
            print('done')                  
            self.input_stream.stop_stream()

            if not os.path.exists(filename):
                with open(filename, 'w'): pass

            wf = wave.open(filename, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(self.pyaudio.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(frames))
            wf.close()

            wfr = wave.open(filename, 'rb')
            
            
            rec = KaldiRecognizer(self.model, fs)
            rec.SetWords(True)

            while True:
                data = wfr.readframes(chunk)
                if len(data) == 0:
                    break

                rec.AcceptWaveform(data)
            
            

            #audio_frames = wf.readframes(wf.getnframes())
            #audio = np.frombuffer(audio_frames, np.int16)
            obj: dict = json.loads(rec.FinalResult())
            text = obj['text']
            self.l_queue.put(text)


            



        thread = Thread(target=func, name='Speech listening')

        thread.start()

    def end_listen(self):
        if not self.listening:
            return
        #tell listen thread to stop
        self.l_queue.put('stop')
        while not self.l_queue.empty(): 
            pass

        text = self.l_queue.get()
        self.listening = False
        return text