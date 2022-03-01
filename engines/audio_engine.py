from click import option
from vosk import Model, KaldiRecognizer, SetLogLevel
from queue import Queue
from threading import Thread
from pydub import AudioSegment
from pydub.playback import play
import modules.logger as log
import pyaudio, wave, os, json, io

#stt
speech_chunk = 1024
speech_sample_format = pyaudio.paInt16
speech_channels = 1
speech_fs = 44100
speech_filename = './resources/temp/speech.wav'
vosk_model_filename ='./resources/vosk-model'
speech_max_listening = 60 #seconds

SetLogLevel(-1)

#tts
voice_folder = './resources/voice'
voice_mode = 'f'

def readVoiceSample(word: str, neutral = False) -> bytes:
    if neutral:
        filename = '{}/{}.mp3'.format(voice_folder, word)
    else:
        filename = '{}/{}_{}.mp3'.format(voice_folder, voice_mode, word)
    data = open(filename, 'rb').read()
    return data

class engine():
    def __init__(self):

        self.pyaudio = pyaudio.PyAudio()
        self.l_queue = Queue()

        log.log_boot('Loading stt')    
        #stt
        self.model = Model(vosk_model_filename)
        self.input_stream = self.pyaudio.open(format=speech_sample_format,
        channels=speech_channels, rate=speech_fs,
        frames_per_buffer=speech_chunk,
        input=True)
        self.input_stream.stop_stream()
        self.listening = False

        self.questioned = False
    
    def startListen(self):
        #print(self.listening)
        if self.listening:
            return
        self.listening = True

        frames = []

        #store data 
        def func():
            self.input_stream.start_stream()
            print('started listening')
            
            for i in range(0, int(speech_fs/speech_chunk * speech_max_listening)):
                data = self.input_stream.read(speech_chunk)
                frames.append(data)
                
                try:
                    if self.l_queue.get_nowait():
                        break
                except:
                    pass
            print('done')                  
            self.input_stream.stop_stream()

            if not os.path.exists(speech_filename):
                with open(speech_filename, 'w'): pass

            wf = wave.open(speech_filename, 'wb')
            wf.setnchannels(speech_channels)
            wf.setsampwidth(self.pyaudio.get_sample_size(speech_sample_format))
            wf.setframerate(speech_fs)
            wf.writeframes(b''.join(frames))
            wf.close()

            wfr = wave.open(speech_filename, 'rb')
            
            
            rec = KaldiRecognizer(self.model, speech_fs)
            rec.SetWords(True)

            while True:
                data = wfr.readframes(speech_chunk)
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

    def endListen(self) -> str:
        if not self.listening:
            return
        #tell listen thread to stop
        self.l_queue.put('stop')
        while not self.l_queue.empty(): 
            pass

        text = self.l_queue.get()
        self.listening = False
        return text

    #speech
    def say(self, text: list[str]) -> bool:
        final_data: bytes = b''
        for sample in text:
            s_data = readVoiceSample(sample.lower())
            if s_data == None:
                if final_data == b'':
                    return False
                else:
                    break
            final_data += s_data
        final_audio = AudioSegment.from_file(io.BytesIO(final_data), format='mp3')
        print('{} says: {}'.format(os.environ.get('assistant_name'),' '.join(text)))
        play(final_audio)


    
   
