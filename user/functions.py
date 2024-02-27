from user import settings
from academy.utils import utils
from academy.camera import cam3
from academy.touch import touch
from user.sound_elements import soundStream
#from user.psychopy_elements import window, square, square2, square3

# when softcode n is called, function n runs once
# then loop n runs until another softcode is called


# draw a temporal white rectange  with task.x, task.y, task.width and task.stim_duration



def function1():
    soundStream.play()


# close door2
def function20():
    if utils.state == 1:  # this only happens for not direct task
        utils.change_to_state = 2  # first action done before min_time

