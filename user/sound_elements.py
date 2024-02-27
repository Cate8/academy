from multiprocessing import Process, Value
import sounddevice as sd
import numpy as np
import time
from threading import Thread
from timeit import default_timer as timer
from scipy.signal import firwin, lfilter  # filters



class SoundR:
    def __init__(self, sampleRate=44100, channelsOut=2, latency='low'):

        print("aqui empezamos")

        try:
            device = self.getDevice()
        except:
            print("error in sound device detection")
            device = 1

        sd.default.device = device
        self.soundVec = self.whiteNoiseGen(1.0, 2000, 20000, 0.5, FsOut=44100, Fn=1000)
        


    @staticmethod
    def getDevice():
        devi = sd.query_devices()

        result = 0
        idx = 0

        for dev in devi:
            if dev['name'].startswith('front') and dev['max_output_channels'] == 2:
                result = idx
                break
            if dev['name'].startswith('HDA Intel PCH: ALC887-VD Analog') and dev['max_output_channels'] == 2:
                result = idx
                break
            elif dev['name'].startswith('iec958') and dev['max_output_channels'] == 2:
                result = idx
                print('found')
                break
            idx += 1

        print('found', devi[result])
        return result
    

    @staticmethod
    def whiteNoiseGen(amp, band_fs_bot, band_fs_top, duration, FsOut=192000, Fn=10000, randgen=None):
        """whiteNoiseGen(amp, band_fs_bot, band_fs_top):
        beware this is not actually whitenoise
        amp: float, amplitude
        band_fs_bot: int, bottom freq of the band
        band_fs_top: int, top freq
        duration: float, secs
        FsOut: int, SoundCard samplingrate to use (192k, 96k, 48k...)
        Fn: int, filter len, def 10k
        *** if this takes too long try shortening Fn or using a lower FsOut ***
        adding some values here. Not meant to change them usually.
        randgen: np.random.RandomState instance to sample from

        returns: sound vector (np.array)
        """
        mean = 0
        std = 1
        if randgen is None:
            randgen = np.random

        if type(amp) is float and isinstance(band_fs_top, int) and isinstance(band_fs_bot,
                                                                            int) and band_fs_bot < band_fs_top:
            band_fs = [band_fs_bot, band_fs_top]
            white_noise = amp * randgen.normal(mean, std, size=int(FsOut * (duration + 1)))
            band_pass = firwin(Fn, [band_fs[0] / (FsOut * 0.5), band_fs[1] / (FsOut * 0.5)], pass_zero=False)
            band_noise = lfilter(band_pass, 1, white_noise)
            s1 = band_noise[FsOut:int(FsOut * (duration + 1))]


            sound = np.array([s1, s1])  # left and right channel
            return np.ascontiguousarray(sound.T, dtype=np.float32)
        
            #return s1  # use np.zeros(s1.size) to get equal-size empty vec.
        else:
            raise ValueError('whiteNoiseGen needs (float, int, int, num,) as arguments')
    
        

    def play(self):
        sd.play(self.soundVec)




class FakeSoundR:
    def __init__(self):
        self.name = 'fake'

    def play(self):
        pass




try:
    soundStream = SoundR()
except:
    print("______")
    print("ERROR SOUND")
    print("_______")
    soundStream = FakeSoundR()




