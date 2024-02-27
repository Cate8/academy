# import numpy as np
# import cv2 as cv


# codec_video = 'mp4v'
# port = '/dev/video-Cam1'

# fourcc_out = cv.VideoWriter_fourcc(*codec_video)
# cap = cv.VideoCapture(port)


# out_video = cv.VideoWriter('/home/delarocha6/academy//video.avi', fourcc_out, 30, (640, 480))

# #out_video = cv.VideoWriter(self.path_video, self.fourcc_out, self.fps, (self.width, self.height))



# if not cap.isOpened():
#     print("Cannot open camera")
#     exit()
# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     # if frame is read correctly ret is True
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break
#     # Our operations on the frame come here
#     gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#     # Display the resulting frame
#     cv.imshow('frame', gray)
#     if cv.waitKey(1) == ord('q'):
#         break
# # When everything done, release the capture
# cap.release()
# cv.destroyAllWindows()







# from pybpodapi.protocol import Bpod, StateMachine


# try:
#     bpod = Bpod()
#     sma = StateMachine(bpod)
#     sma.add_state(
#         state_name='End',
#         state_timer=0.1,
#         state_change_conditions={Bpod.Events.Tup: 'exit'},
#         output_actions=[(Bpod.OutputChannels.SoftCode, 20)]
#     )
#     bpod.send_state_machine(sma)
#     bpod.run_state_machine(sma)
#     bpod.close()
#     i = 4
#     connection = True

#     print("ok")
# except Exception:
#     time.sleep(2)
#     i += 1

#     print("nor")










from multiprocessing import Process, Value
import sounddevice as sd
import numpy as np
import time
from threading import Thread
from timeit import default_timer as timer
from scipy.signal import firwin, lfilter  # filters




def getDevice():
    devi = sd.query_devices()

    print(devi)

    result = 0
    idx = 0

    for dev in devi:
        print(dev['name'])

        print(dev)
        if dev['name'].startswith('HDA Intel PCH: ALC887-VD Analog'):
            result = idx
            print('found')
        idx += 1

    return result

devi = getDevice()



print("starting")
sd.default.device = 1
sd.default.samplerate = 44100
print("before channels")
sd.default.channels = 2
print("after channels")



def whiteNoiseGen(amp, band_fs_bot, band_fs_top, duration, FsOut=192000, Fn=10000, randgen=None):
    """whiteNoiseGen(amp, band_fs_bot, band_fs_top):
    beware this is not actually whitenoise
    amp: float, amplitude
    band_fs_bot: int, bottom freq of the band
    band_fs_top: int, top freq
    duration: secs
    FsOut: SoundCard samplingrate to use (192k, 96k, 48k...)
    Fn: filter len, def 10k
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
        return s1  # use np.zeros(s1.size) to get equal-size empty vec.
    else:
        raise ValueError('whiteNoiseGen needs (float, int, int, num,) as arguments')
    

sound = whiteNoiseGen(1.0, 2000, 20000, 0.5, FsOut=44100, Fn=1000)

sd.play(sound)

time.sleep(3)





   