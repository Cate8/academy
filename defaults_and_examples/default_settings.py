# THIS IS A BACKUP FILE. DO NOT CHANGE IT.
# THE FIRST TIME THE APPLICATION IS LAUNCHED, A COPY OF THIS FILE IS CREATED IN THE USER DIRECTORY.
# ALWAYS MODIFY THE WORKING VERSION IN THE USER DIRECTORY.


import pkg_resources
import os

# default bpod values (not to be changed)
TARGET_BPOD_FIRMWARE_VERSION = "22"
PYBPOD_BAUDRATE = 1312500 # by default we can also try: 12000000
PYBPOD_SYNC_CHANNEL = 255
PYBPOD_SYNC_MODE = 1
PYBPOD_API_MODULES = []
SESSION_NAME = 'session'
DISTRIBUTION_DIRECTORY = pkg_resources.get_distribution('academy').location
TASKS_DIRECTORY = os.path.join(DISTRIBUTION_DIRECTORY, 'tasks')
USER_DIRECTORY = os.path.join(DISTRIBUTION_DIRECTORY, 'user')
DATA_DIRECTORY = os.path.join(DISTRIBUTION_DIRECTORY, 'data')
BACKUP_TASKS_DIRECTORY = os.path.join(DATA_DIRECTORY, 'backup_tasks')
SESSIONS_DIRECTORY = os.path.join(DATA_DIRECTORY, 'sessions')
VIDEOS_DIRECTORY = os.path.join(DATA_DIRECTORY, 'videos')
ECOHAB_DIRECTORY = os.path.join(DATA_DIRECTORY, 'ecohab')
DROPBOX_SESSIONS_DIRECTORY = os.path.join(DATA_DIRECTORY, 'sessions')

# serial and net ports
ARDUINO_SERIAL_PORT = '/dev/ttyACM-Arduino'                                         # <-- TO CHANGE ttyACM sometimes
ARDUINO_INSIDE_SERIAL_PORT = '/dev/ttyUSB-Arduino_inside'                           # <-- TO CHANGE
PYBPOD_SERIAL_PORT = '/dev/ttyACM-BPOD09'                                            # <-- TO CHANGE
PYBPOD_NET_PORT = 36000  # network port to receive remote commands like softcodes
TOUCHSCREEN_PORT = '/dev/input/by-id/usb-Touch__KiT_Touch_Computer_INC.-event-if00' # <-- TO CHANGE
CAMERA1_PORT = "/dev/video-Cam1"
CAMERA2_PORT = "/dev/video-Cam2"
CAMERA3_PORT = "/dev/video-Cam3"

# bpod ports
BPOD_BNC_PORTS_ENABLED = [False, False]
BPOD_WIRED_PORTS_ENABLED = [False, False]
BPOD_BEHAVIOR_PORTS_ENABLED = [False, True, True, False, True, False, False, False]  # ports that are activated
BPOD_BEHAVIOR_PORTS_WATER = [False, True, False, False, True, False, False, False]  # ports that deliver water

# touchscreen
XINPUT = 'xinput map-to-output "Touch__KiT Touch  Computer INC." HDMI1'   # <-- TO CHANGE
WIN_SIZE = [403, 252]  # in mm
WIN_RESOLUTION = [1440, 900]
TOUCH_RESOLUTION = [4096, 4096]
SCREEN_NUMBER = 1
VIEW_POSITION = [-int(WIN_RESOLUTION[0] / 2), -int(WIN_RESOLUTION[1] / 2)]
WIN_COLOR = [-1, -1, -1]
PIXELS_PER_MM = 3.57
STIM_WIDTH = 40  # mm
TIME_BETWEEN_RESPONSES = 0.5
ONLY_X = True
MULTITOUCH = True


# mouse detection
NOMICEDOOR2 = 200  # if area_doors2 > NOMICEDOOR2 animal can not exit    # no se usa
FLOORMOUSE = 50                                                          # no se usa








NOMICECAGE = 50  # if area_cage > NOMICECAGE animal can not enter
NOMICEDOOR1 = 80  # if area_doors1 > NOMICEDOOR1 animal can not enter

ONEMOUSE = 3800  # if area_total > ONEMOUSE animal can not enter
SEVERALMICE = 5580 # if area_box > SEVERALMICE, alarm 2 mice inside box 

THRESHOLD_DAY_DOOR2 = 120    
THRESHOLD_DAY_DOOR1 = 140 
THRESHOLD_DAY_CAGE = 110                    

THRESHOLD_NIGHT_DOOR2 = 120
THRESHOLD_NIGHT_DOOR1 = 140
THRESHOLD_NIGHT_CAGE = 120 

CAM3_THRESHOLD = 50     


CAM1_DOORS2_ZONE = [120, 230, 215, 250]   # left, right, top, bottom    640x480
CAM1_DOORS1_ZONE = [230, 430, 215, 250]   # left, right, top, bottom    640x480
CAM1_CAGE_ZONE = [450, 610, 140, 250]      # left, right, top, bottom    640x480

CAM3_DOORS1_ZONE = [100, 540, 20, 450]   # left, right, top, bottom    640x480








                                            

DURATION_TAG = 0.5  # seconds the rfid lecture is stored
DURATION_TAGS = 15  # seconds tags are stored if there is a tag different than current animal can not enter
HOUR_DAY = 8  # night is more restrictive so it last 1 minute more when changing
MINUTE_DAY = 1
HOUR_NIGHT = 20 # in winter may change to 7-19
MINUTE_NIGHT = 1
TIME_TO_ENTER = 4 # time between session and session (hours)            # <-- TO CHANGE
LONGER_TIME_TO_ENTER = [] #animals with longer inter session times      # <-- TO CHANGE

# camera
CAM1_NUMBER = 1
CAM1_NAME_VIDEO = 'Cam1'
CAM1_WIDTH = 640
CAM1_HEIGHT = 480
CAM1_FPS = 120
CAM1_CODEC_VIDEO = 'H264'
CAM1_STATES = {}
CAM1_DURATION_VIDEO = 1800
CAM1_NUMBER_OF_VIDEOS = 50
CAM1_THRESHOLD = 0
CAM1_TEXT_X = 100                         # <-- TO CHANGE
CAM1_TEXT_Y = 300                         # <-- TO CHANGE

CAM2_NUMBER = 2
CAM2_NAME_VIDEO = 'Cam2'
CAM2_WIDTH = 640
CAM2_HEIGHT = 480
CAM2_FPS = 120
CAM2_CODEC_VIDEO = 'H264'
CAM2_STATES = {}
CAM2_DURATION_VIDEO = 0
CAM2_NUMBER_OF_VIDEOS = 0
CAM2_THRESHOLD = 30
CAM2_CAGE_ZONE = None
CAM2_DOORS1_ZONE = None
CAM2_DOORS2_ZONE = None

CAM3_NUMBER = 3
CAM3_NAME_VIDEO = 'Cam3'
CAM3_WIDTH = 640
CAM3_HEIGHT = 480
CAM3_FPS = 120
CAM3_CODEC_VIDEO = 'H264'
CAM3_STATES = {"Correct": (600, 30),
               "Incorrect": (600, 70),
               "Punish": (600, 100),
               "Miss": (600, 130),
               "Resp Win": (600, 160),
               "On": (30, 30)}
CAM3_DURATION_VIDEO = 0
CAM3_NUMBER_OF_VIDEOS = 0
CAM3_THRESHOLD_MOUSE = 0 #detection for opto         # <-- NO VALE PARA NADA
CAM3_THRESHOLD_LED = 0 #detection of the led opto   # <-- NO VALE PARA NADA
CAM3_CAGE_ZONE = None
CAM3_DOORS2_ZONE = [1, 2, 1, 2]    # <-- NO VALE PARA NADA
CAM3_DOORS3_ZONE = None   # <-- TO CHANGE  
CAM3_FLOOR1_ZONE = None   # <-- TO CHANGE
CAM3_FLOOR2_ZONE = None  # <-- TO CHANGE
CAM3_TRACKING_POSITION = False
CAM3_FLOOR_ON = False


# telegram
TELEGRAM_TOKEN = '6566547683:AAFEhx5sJdg8y6vHOrvGKVoaohopK0JBWaM'             # <-- TO CHANGE
TELEGRAM_CHAT = '-4001231768'                                                  # <-- TO CHANGE
TELEGRAM_USERS = {  # dictionary of users that can send telegram messages
    'balma': '1079223749',
    'rafa': '343291206',
    'jaime': '455652844',
    'eva': '1219420492',
    'cate': '1606786243'
}


#AWS
OPERATION_TABLE = 'operation_times4'          # <-- TO CHANGE
TASK_TABLE = 'task_times4'                    # <-- TO CHANGE

# other
BOX_NAME = 9                                # <-- TO CHANGE

DEFAULT_TRIALS_MIN = 0
DEFAULT_DURATION_MIN = 0  # seconds
DEFAULT_DURATION_TIRED = 3600  # seconds    # <-- TO CHANGE
DEFAULT_TRIALS_TIRED = 0
DEFAULT_TRIALS_MAX = 1000
DEFAULT_DURATION_MAX = 36000  # seconds     # <-- TO CHANGE

MINIMUM_WATER_24 = 400  # in 24 hours
MINIMUM_WATER_48 = 1000  # in 48 hours

MINIMUM_WEIGHT = 70  # in percentage
MAXIMUM_WEIGHT = 200  # in percentage

MINIMUM_TEMPERATURE = 19
MAXIMUM_TEMPERATURE = 27
MAXIMUM_TIME = 3600  # in seconds         # <-- TO CHANGE

INACTIVE_SUBJECTS = ['None', 'manual']  # subjects that don't raise alarms and not save data
TESTING = True  # if true academy works without cams, arduino, screen or bpod

OVERDETECTIONS = 50000 # rise alarms

PULSEPAL_CONNECTED = False
PSYCHOPY_CONNECTED = False
