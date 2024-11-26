# """
# ----------------------------------------------------------------------------
# This file is part of the Sanworks Pulse Pal repository
# Copyright (C) 2016 Sanworks LLC, Sound Beach, New York, USA
# ----------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
# This program is distributed  WITHOUT ANY WARRANTY and without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# """


# import struct
# import math
# import serial

# class PulsePalObject(object):

#     def __init__(self):
#         self.serialObject = None
#         self.OpMenuByte = 213
#         self.firmwareVersion = 0
#         self.model = 0
#         self.dac_bitMax = 0
#         self.cycleFrequency = 20000
#         self.isBiphasic = [float('nan'), 0, 0, 0, 0]
#         self.phase1Voltage = [float('nan'), 5, 5, 5, 5]
#         self.phase2Voltage = [float('nan'), -5, -5, -5, -5]
#         self.restingVoltage = [float('nan'), 0, 0, 0, 0]
#         self.phase1Duration = [float('nan'), 0.001, 0.001, 0.001, 0.001]
#         self.interPhaseInterval = [float('nan'), 0.001, 0.001, 0.001, 0.001]
#         self.phase2Duration = [float('nan'), 0.001, 0.001, 0.001, 0.001]
#         self.interPulseInterval = [float('nan'), 0.01, 0.01, 0.01, 0.01]
#         self.burstDuration = [float('nan'), 0, 0, 0, 0]
#         self.interBurstInterval = [float('nan'), 0, 0, 0, 0]
#         self.pulseTrainDuration = [float('nan'), 1, 1, 1, 1]
#         self.pulseTrainDelay = [float('nan'), 0, 0, 0, 0]
#         self.linkTriggerChannel1 = [float('nan'), 1, 1, 1, 1]
#         self.linkTriggerChannel2 = [float('nan'), 0, 0, 0, 0]
#         self.customTrainID = [float('nan'), 0, 0, 0, 0]
#         self.customTrainTarget = [float('nan'), 0, 0, 0, 0]
#         self.customTrainLoop = [float('nan'), 0, 0, 0, 0]
#         self.triggerMode = [float('nan'), 0, 0]
#         self.outputParameterNames = ['isBiphasic', 'phase1Voltage','phase2Voltage', 'phase1Duration',
#                                      'interPhaseInterval', 'phase2Duration','interPulseInterval', 'burstDuration',
#                                      'interBurstInterval', 'pulseTrainDuration', 'pulseTrainDelay',
#                                      'linkTriggerChannel1', 'linkTriggerChannel2', 'customTrainID', 'customTrainTarget',
#                                      'customTrainLoop', 'restingVoltage']
#         self.triggerParameterNames = ['triggerMode']

#     def connect(self, serialPortName):
#         self.serialObject = serial.Serial(serialPortName, 12000000, timeout=1, rtscts=True)
#         handshakeByteString = struct.pack('BB', self.OpMenuByte, 72)
#         self.serialObject.write(handshakeByteString)
#         Response = self.serialObject.read(5)
#         fvBytes = Response[1:5]
#         self.firmwareVersion = struct.unpack('<I',fvBytes)[0]
#         if self.firmwareVersion < 20:
#             self.model = 1
#             self.dac_bitMax = 255
#         else:
#             self.model = 2
#             self.dac_bitMax = 65535
#         if self.firmwareVersion == 20:
#             print("Notice: NOTE: A firmware update is available.")
#             print("It fixes a bug in Pulse Gated trigger mode when used with multiple inputs.")
#             print("To update, follow the instructions at https://sites.google.com/site/pulsepalwiki/updating-firmware")
#         message = bytearray(list('YPYTHON'.encode()))
#         self.serialObject.write(message)

#     def disconnect(self):
#         terminateByteString = struct.pack('BB', self.OpMenuByte, 81)
#         self.serialObject.write(terminateByteString)
#         self.serialObject.close()

#     def programOutputChannelParam(self, paramName, channel, value):
#         originalValue = value
#         if isinstance(paramName, str):
#             paramCode = self.outputParameterNames.index(paramName)+1
#         else:
#             paramCode = paramName

#         if 2 <= paramCode <= 3:
#             value = math.ceil(((value+10)/float(20))*self.dac_bitMax) # Convert volts to bits
#             if self.model == 1:
#                 programByteString = struct.pack('BBBBB',self.OpMenuByte,74,paramCode,channel,value)
#             else:
#                 programByteString = struct.pack('<BBBBH',self.OpMenuByte,74,paramCode,channel,value)
#         elif paramCode == 17:
#             value = math.ceil(((value+10)/float(20))*self.dac_bitMax) # Convert volts to bits
#             if self.model == 1:
#                 programByteString = struct.pack('BBBBB',self.OpMenuByte,74,paramCode,channel,value)
#             else:
#                 programByteString = struct.pack('<BBBBH',self.OpMenuByte,74,paramCode,channel,value)
#         elif 4 <= paramCode <= 11:
#             value = int(value*self.cycleFrequency)
#             programByteString = struct.pack('<BBBBL',self.OpMenuByte,74,paramCode,channel,value)
#         else:
#             programByteString = struct.pack('BBBBB',self.OpMenuByte,74,paramCode,channel,value)
#         self.serialObject.write(programByteString)
#         # Receive acknowledgement
#         ok = self.serialObject.read(1)
#         if len(ok) == 0:
#             raise PulsePalError('Error: Pulse Pal did not return an acknowledgement byte after a call to programOutputChannelParam.')
#         # Update the PulsePal object's parameter fields
#         if paramCode == 1:
#             self.isBiphasic[channel] = originalValue
#         elif paramCode == 2:
#             self.phase1Voltage[channel] = originalValue
#         elif paramCode == 3:
#             self.phase2Voltage[channel] = originalValue
#         elif paramCode == 4:
#             self.phase1Duration[channel] = originalValue
#         elif paramCode == 5:
#             self.interPhaseInterval[channel] = originalValue
#         elif paramCode == 6:
#             self.phase2Duration[channel] = originalValue
#         elif paramCode == 7:
#             self.interPulseInterval[channel] = originalValue
#         elif paramCode == 8:
#             self.burstDuration[channel] = originalValue
#         elif paramCode == 9:
#             self.interBurstInterval[channel] = originalValue
#         elif paramCode == 10:
#             self.pulseTrainDuration[channel] = originalValue
#         elif paramCode == 11:
#             self.pulseTrainDelay[channel] = originalValue
#         elif paramCode == 12:
#             self.linkTriggerChannel1[channel] = originalValue
#         elif paramCode == 13:
#             self.linkTriggerChannel2[channel] = originalValue
#         elif paramCode == 14:
#             self.customTrainID[channel] = originalValue
#         elif paramCode == 15:
#             self.customTrainTarget[channel] = originalValue
#         elif paramCode == 16:
#             self.customTrainLoop[channel] = originalValue
#         elif paramCode == 17:
#             self.restingVoltage[channel] = originalValue

#     def programTriggerChannelParam(self, paramName, channel, value):
#         originalValue = value
#         if isinstance(paramName, str):
#             paramCode = self.triggerParameterNames.index(paramName)+1
#         else:
#             paramCode = paramName
#         messageBytes = struct.pack('BBBBB',self.OpMenuByte,74,paramCode,channel,value)
#         self.serialObject.write(messageBytes)
#         # Receive acknowledgement
#         ok = self.serialObject.read(1)
#         if len(ok) == 0:
#             raise PulsePalError('Error: Pulse Pal did not return an acknowledgement byte after a call to programTriggerChannelParam.')
#         if paramCode == 1:
#             self.triggerMode[channel] = originalValue

#     def syncAllParams(self):
#         # First make a list data-type with all param values in an iteration of the loop.
#         # Then pack them by data-type and append to string with + operation
#         programByteString = struct.pack('BB',self.OpMenuByte, 73)

#         # Add 32-bit time params
#         programValues = [0]*32
#         pos = 0
#         for i in range(1,5):
#             programValues[pos] = int(self.phase1Duration[i]*self.cycleFrequency)
#             pos+=1
#             programValues[pos] = int(self.interPhaseInterval[i]*self.cycleFrequency)
#             pos+=1
#             programValues[pos] = int(self.phase2Duration[i]*self.cycleFrequency)
#             pos+=1
#             programValues[pos] = int(self.interPulseInterval[i]*self.cycleFrequency)
#             pos+=1
#             programValues[pos] = int(self.burstDuration[i]*self.cycleFrequency)
#             pos+=1
#             programValues[pos] = int(self.interBurstInterval[i]*self.cycleFrequency)
#             pos+=1
#             programValues[pos] = int(self.pulseTrainDuration[i]*self.cycleFrequency)
#             pos+=1
#             programValues[pos] = int(self.pulseTrainDelay[i]*self.cycleFrequency)
#             pos+=1

#         # Pack 32-bit times to bytes and append to program byte-string
#         programByteString = programByteString + struct.pack('<LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL' , *programValues)

#         # Add 16-bit voltages
#         if self.model == 2:
#             programValues = [0]*12
#             pos = 0
#             for i in range(1,5):
#                 value = math.ceil(((self.phase1Voltage[i]+10)/float(20))*self.dac_bitMax) # Convert volts to bits
#                 programValues[pos] = value
#                 pos+=1
#                 value = math.ceil(((self.phase2Voltage[i]+10)/float(20))*self.dac_bitMax) # Convert volts to bits
#                 programValues[pos] = value
#                 pos+=1
#                 value = math.ceil(((self.restingVoltage[i]+10)/float(20))*self.dac_bitMax) # Convert volts to bits
#                 programValues[pos] = value
#                 pos+=1
#             programByteString = programByteString + struct.pack('<HHHHHHHHHHHH' , *programValues)
#         # Add 8-bit params
#         if self.model == 1:
#             programValues = [0]*28
#         else:
#             programValues = [0]*16
#         pos = 0
#         for i in range(1,5):
#             programValues[pos] = self.isBiphasic[i]
#             pos+=1
#             if self.model == 1:
#                 value = math.ceil(((self.phase1Voltage[i]+10)/float(20))*self.dac_bitMax) # Convert volts to bits
#                 programValues[pos] = value
#                 pos+=1
#                 value = math.ceil(((self.phase2Voltage[i]+10)/float(20))*self.dac_bitMax) # Convert volts to bits
#                 programValues[pos] = value
#                 pos+=1
#             programValues[pos] = self.customTrainID[i]
#             pos+=1
#             programValues[pos] = self.customTrainTarget[i]
#             pos+=1
#             programValues[pos] = self.customTrainLoop[i]
#             pos+=1
#             if self.model == 1:
#                 value = math.ceil(((self.restingVoltage[i]+10)/float(20))*self.dac_bitMax) # Convert volts to bits
#                 programValues[pos] = value
#                 pos+=1
#         # Pack 8-bit params to bytes and append to program byte-string
#         if self.model == 1:
#             programByteString = programByteString + struct.pack('BBBBBBBBBBBBBBBBBBBBBBBBBBBB', *programValues)
#         else:
#             programByteString = programByteString + struct.pack('BBBBBBBBBBBBBBBB', *programValues)
#         # Add trigger channel link params
#         programValues = [0]*8
#         pos = 0
#         for i in range(1,5):
#             programValues[pos] = self.linkTriggerChannel1[i]
#             pos+=1
#         for i in range(1,5):
#             programValues[pos] = self.linkTriggerChannel2[i]
#             pos+=1
#         # Pack 8-bit params to bytes and append to program byte-string
#         programByteString = programByteString + struct.pack('BBBBBBBB', *programValues)

#         # Add trigger mode params
#         programByteString = programByteString + struct.pack('BB', self.triggerMode[1], self.triggerMode[2])

#         # Send program byte string to PulsePal
#         self.serialObject.write(programByteString)
#         # Receive acknowledgement
#         ok = self.serialObject.read(1)
#         if len(ok) == 0:
#             raise PulsePalError('Error: Pulse Pal did not return an acknowledgement byte after a call to syncAllParams.')

#     def sendCustomPulseTrain(self, customTrainID, pulseTimes, pulseVoltages):
#         nPulses = len(pulseTimes)
#         for i in range(0,nPulses):
#             pulseTimes[i] = int(pulseTimes[i]*self.cycleFrequency) # Convert seconds to multiples of minimum cycle (100us)
#             pulseVoltages[i] = math.ceil(((pulseVoltages[i]+10)/float(20))*self.dac_bitMax) # Convert volts to bytes
#         if customTrainID == 1:
#             messageBytes = struct.pack('BB', self.OpMenuByte , 75) # Op code for programming train 1
#         else:
#             messageBytes = struct.pack('BB', self.OpMenuByte , 76) # Op code for programming train 2
#         if self.model == 1:
#             messageBytes = messageBytes + struct.pack('<BL', 0, nPulses) # 0 is the USB packet correction byte. See PulsePal wiki
#         else:
#             messageBytes = messageBytes + struct.pack('<L', nPulses)
#         messageBytes = messageBytes + struct.pack(('<' + 'L'*nPulses), *pulseTimes) # Add pulse times
#         if self.model == 1:
#             messageBytes = messageBytes + struct.pack(('B'*nPulses), *pulseVoltages) # Add pulse times
#         else:
#             messageBytes = messageBytes + struct.pack(('<' + 'H'*nPulses), *pulseVoltages) # Add pulse times
#         self.serialObject.write(messageBytes)
#         # Receive acknowledgement
#         ok = self.serialObject.read(1)
#         if len(ok) == 0:
#             raise PulsePalError('Error: Pulse Pal did not return an acknowledgement byte after a call to sendCustomPulseTrain.')

#     def sendCustomWaveform(self, customTrainID, pulseWidth, pulseVoltages): # For custom pulse trains with pulse times = pulse width

#         nPulses = len(pulseVoltages)
#         pulseTimes = [0]*nPulses
#         pulseWidth = pulseWidth*self.cycleFrequency # Convert seconds to to multiples of minimum cycle (100us)
#         for i in range(0,nPulses):
#             pulseTimes[i] = int(pulseWidth*i) # Add consecutive pulse
#             pulseVoltages[i] = math.ceil(((pulseVoltages[i]+10)/float(20))*self.dac_bitMax) # Convert volts to bytes
#         if customTrainID == 1:
#             messageBytes = struct.pack('BB', self.OpMenuByte , 75) # Op code for programming train 1
#         else:
#             messageBytes = struct.pack('BB', self.OpMenuByte , 76) # Op code for programming train 2
#         if self.model == 1:
#             messageBytes = messageBytes + struct.pack('<BL', 0, nPulses) # 0 is the USB packet correction byte. See PulsePal wiki
#         else:
#             messageBytes = messageBytes + struct.pack('<L', nPulses)
#         messageBytes = messageBytes + struct.pack(('<' + 'L'*nPulses), *pulseTimes) # Add pulse times
#         if self.model == 1:
#             messageBytes = messageBytes + struct.pack(('B'*nPulses), *pulseVoltages) # Add pulse times
#         else:
#             messageBytes = messageBytes + struct.pack(('<' + 'H'*nPulses), *pulseVoltages) # Add pulse times
#         self.serialObject.write(messageBytes) # Send custom waveform
#         # Receive acknowledgement
#         ok = self.serialObject.read(1)
#         if len(ok) == 0:
#             raise PulsePalError('Error: not return an acknowledgement byte after a call to sendCustomWaveform.')

#     def triggerOutputChannels(self, channel1, channel2, channel3, channel4):
#         triggerByte = 0
#         triggerByte = triggerByte + (1*channel1)
#         triggerByte = triggerByte + (2*channel2)
#         triggerByte = triggerByte + (4*channel3)
#         triggerByte = triggerByte + (8*channel4)
#         messageBytes = struct.pack('BBB',self.OpMenuByte,77,triggerByte)
#         self.serialObject.write(messageBytes)

#     def abortPulseTrains(self):
#         messageBytes = struct.pack('BB',self.OpMenuByte, 80)
#         self.serialObject.write(messageBytes)

#     def setContinuousLoop(self, channel, state):
#         messageBytes = struct.pack('BBBB',self.OpMenuByte, 82, channel, state)
#         self.serialObject.write(messageBytes)

#     def setFixedVoltage(self, channel, voltage):
#         voltage = math.ceil(((voltage+10)/float(20))*self.dac_bitMax) # Convert volts to bytes
#         if self.model == 1:
#             messageBytes = struct.pack('BBBB',self.OpMenuByte, 79, channel, voltage)
#         else:
#             messageBytes = struct.pack('<BBBH',self.OpMenuByte, 79, channel, voltage)
#         self.serialObject.write(messageBytes)
#         # Receive acknowledgement
#         ok = self.serialObject.read(1)
#         if len(ok) == 0:
#             raise PulsePalError('Error: Pulse Pal did not return an acknowledgement byte after a call to setFixedVoltage.')

#     def setDisplay(self, row1String, row2String):
#         row1List = list(row1String.encode())
#         row2List = list(row2String.encode())
#         message = row1List + [254] + row2List
#         message = [213, 78] + [len(message)] + message
#         messageBytes = bytearray(message)
#         self.serialObject.write(messageBytes)

#     def saveSDSettings(self, fileName):
#         if self.model == 1:
#             raise PulsePalError('Pulse Pal 1.X has no microSD card, and therefore does not support on-board settings files.')
#         else:
#             fileNameSize = len(fileName)
#             messageBytes = chr(self.OpMenuByte) + chr(90) + chr(1) + chr(fileNameSize) + fileName
#             self.serialObject.write(messageBytes)

#     def deleteSDSettings(self, fileName):
#         if self.model == 1:
#             raise PulsePalError('Pulse Pal 1.X has no microSD card, and therefore does not support on-board settings files.')
#         else:
#             fileNameSize = len(fileName)
#             messageBytes = chr(self.OpMenuByte) + chr(90) + chr(3) + chr(fileNameSize) + fileName
#             self.serialObject.write(messageBytes)

#     def loadSDSettings(self, fileName):
#         if self.model == 1:
#             raise PulsePalError('Pulse Pal 1.X has no microSD card, and therefore does not support on-board settings files.')
#         else:
#             fileNameSize = len(fileName)
#             messageBytes = chr(self.OpMenuByte) + chr(90) + chr(2) + chr(fileNameSize) + fileName
#             self.serialObject.write(messageBytes)
#             response = self.serialObject.read(178)
#             ind = 0
#             cFreq = float(self.cycleFrequency)
#             for i in range(1,5):
#                 self.phase1Duration[i] = struct.unpack("<L",response[ind:ind+4])[0]/cFreq
#                 ind+=4
#                 self.interPhaseInterval[i] = struct.unpack("<L",response[ind:ind+4])[0]/cFreq
#                 ind+=4
#                 self.phase2Duration[i] = struct.unpack("<L",response[ind:ind+4])[0]/cFreq
#                 ind+=4
#                 self.interPulseInterval[i] = struct.unpack("<L",response[ind:ind+4])[0]/cFreq
#                 ind+=4
#                 self.burstDuration[i] = struct.unpack("<L",response[ind:ind+4])[0]/cFreq
#                 ind+=4
#                 self.interBurstInterval[i] = struct.unpack("<L",response[ind:ind+4])[0]/cFreq
#                 ind+=4
#                 self.pulseTrainDuration[i] = struct.unpack("<L",response[ind:ind+4])[0]/cFreq
#                 ind+=4
#                 self.pulseTrainDelay[i] = struct.unpack("<L",response[ind:ind+4])[0]/cFreq
#                 ind+=4
#             for i in range(1,5):
#                 voltageBits = struct.unpack("<H",response[ind:ind+2])[0]
#                 ind+=2
#                 self.phase1Voltage[i] = round((((voltageBits/float(self.dac_bitMax))*20)-10)*100)/100
#                 voltageBits = struct.unpack("<H",response[ind:ind+2])[0]
#                 ind+=2
#                 self.phase2Voltage[i] = round((((voltageBits/float(self.dac_bitMax))*20)-10)*100)/100
#                 voltageBits = struct.unpack("<H",response[ind:ind+2])[0]
#                 ind+=2
#                 self.restingVoltage[i] = round((((voltageBits/float(self.dac_bitMax))*20)-10)*100)/100
#             for i in range(1,5):
#                 self.isBiphasic[i] = struct.unpack("B",response[ind])[0]
#                 ind+=1
#                 self.customTrainID[i] = struct.unpack("B",response[ind])[0]
#                 ind+=1
#                 self.customTrainTarget[i] = struct.unpack("B",response[ind])[0]
#                 ind+=1
#                 self.customTrainLoop[i] = struct.unpack("B",response[ind])[0]
#                 ind+=1
#             for i in range(1,5):
#                 self.linkTriggerChannel1[i] = struct.unpack("B",response[ind])[0]
#                 ind+=1
#             for i in range(1,5):
#                 self.linkTriggerChannel2[i] = struct.unpack("B",response[ind])[0]
#                 ind+=1
#             self.triggerMode[1] = struct.unpack("B",response[ind])[0]
#             ind+=1
#             self.triggerMode[2] = struct.unpack("B",response[ind])[0]

#     def __str__(self):
#         sb = []
#         for key in self.__dict__:
#             sb.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))

#         return ', '.join(sb)

#     def __repr__(self):
#         return self.__str__()








from decimal import Decimal
import numpy as np
import math
import serial
import time


class ArCom(object):
    def __init__(self, serial_port_name, baud_rate):
        """  Initializes the ArCOM object and opens the USB serial port
             Args:
                 serial_port_name (string) The name of the USB serial port as known to the OS
                                           Examples = 'COM3' (Windows), '/dev/ttyACM0' (Linux)
                 baud_rate (uint32) The speed of the target USB serial device (bits/second)
             Returns:
                 none
        """
        self._typeNames = ('uint8', 'int8', 'char', 'uint16', 'int16', 'uint32', 'int32', 'single', 'double')
        self._typeBytes = (1, 1, 1, 2, 2, 4, 4, 8)
        self.serialObject = serial.Serial(serial_port_name, baud_rate, timeout=10, rtscts=True)

    def close(self):
        """  Closes the USB serial port
             Args:
                 none
             Returns:
                 none
         """
        self.serialObject.close()

    def bytes_available(self):
        """  Returns the number of bytes available to read from the USB serial buffer
             Args:
                 none
             Returns:
                 nBytes (int) the number of bytes available to read
         """
        return self.serialObject.inWaiting()

    def write(self, *arg):
        """  Write bytes to the USB serial buffer
             Args:
                 Arguments containing a message to write. The message format is:
                 # First value:
                     Arg 1. A single value or list of values to write
                     Arg 2. The datatype of the data in Arg 1 (must be supported, see self._typeBytes)
                 # Additional values (optional) given as pairs of arguments
                     Arg N. An additional value or list of values to write
                     Arg N+1. The datatype of arg N
             Returns:
                 none
         """
        n_types = int(len(arg)/2)
        arg_pos = 0
        message_bytes = b''
        for i in range(0, n_types):
            data = arg[arg_pos]
            arg_pos += 1
            datatype = arg[arg_pos]
            arg_pos += 1
            if (datatype in self._typeNames) is False:
                raise ArCOMError('Error: ' + datatype + ' is not a data type supported by ArCOM.')
            datatype_pos = self._typeNames.index(datatype)
            
            if type(data).__module__ == np.__name__:
                npdata = data.astype(datatype)
            else:
                npdata = np.array(data, dtype=datatype)
            message_bytes += npdata.tobytes()
        self.serialObject.write(message_bytes)

    def read(self, *arg):
        """  Read bytes from the USB serial buffer
             Args:
                 Arguments containing a message to read. The message format is:
                 # First value:
                     Arg 1. The number of values to read
                     Arg 2. The datatype of the data in Arg 1 (must be supported, see self._typeBytes)
                 # Additional values (optional) given as pairs of arguments
                     Arg N. An additional value number of values to read
                     Arg N+1. The datatype of arg N
                     Note: If additional args are given, the data will be returned as a list
                           with each requested value in the next sequential list position
             Returns:
                 The data requested, returned as a numpy ndarray
                (or a list of ndarrays if multiple values were requested)
         """
        num_types = int(len(arg)/2)
        arg_pos = 0
        outputs = []
        for i in range(0, num_types):
            num_values = arg[arg_pos]
            arg_pos += 1
            datatype = arg[arg_pos]
            if (datatype in self._typeNames) is False:
                raise ArCOMError('Error: ' + datatype + ' is not a data type supported by ArCOM.')
            arg_pos += 1
            type_index = self._typeNames.index(datatype)
            byte_width = self._typeBytes[type_index]
            n_bytes2read = num_values*byte_width
            message_bytes = self.serialObject.read(n_bytes2read)
            n_bytes_read = len(message_bytes)
            if n_bytes_read < n_bytes2read:
                raise ArCOMError('Error: serial port timed out. ' + str(n_bytes_read) +
                                 ' bytes read. Expected ' + str(n_bytes2read) + ' byte(s).')
            this_output = np.frombuffer(message_bytes, datatype)
            outputs.append(this_output)
        if num_types == 1:
            outputs = this_output
        return outputs

    def __del__(self):
        self.serialObject.close()


class ArCOMError(Exception):
    pass




class PulsePalObject(object):
    # Constants
    OP_MENU_BYTE = 213
    HANDSHAKE_OPCODE = 72
    HANDSHAKE_RESPONSE = 75
    DAC_BITMAX_MODEL_1 = 255
    DAC_BITMAX_MODEL_2 = 65535
    CYCLE_FREQUENCY = 20000  # Hz
    
    def __init__(self, port_name):
        """
        Initializes a new instance of the PulsePalObject.

        Args:
            port_name (str): The name of the USB serial port to which the Pulse Pal is connected (e.g. COM3 on Windows)

        Raises:
            PulsePalError: If there is a problem initializing the connection.
        """
        self.Port = ArCom(port_name, 12000000)  # ArCom (Arduino Communication) wraps PySerial
        #                                         to simplify data transactions with Arduino
        self._model = 0
        self._dac_bitMax = self._toDecimal(0)
        
        # handshake to confirm connectivity
        self.Port.write((self.OP_MENU_BYTE, self.HANDSHAKE_OPCODE), 'uint8')
        handshake = self.Port.read(1, 'uint8')
        if handshake != self.HANDSHAKE_RESPONSE:
            raise PulsePalError('Error: incorrect handshake returned.')
        
        # setup
        firmware_version = self.Port.read(1, 'uint32')
        if firmware_version < 20:  # Model can be inferred from firmware version. Model 1 spanned firmware v1-19.
            self._model = 1
            self._dac_bitMax = self._toDecimal(self.DAC_BITMAX_MODEL_1)
        else:
            self._model = 2
            self._dac_bitMax = self._toDecimal(self.DAC_BITMAX_MODEL_2)
        self.firmware_version = firmware_version
        if self.firmware_version == 20:
            print("Notice: NOTE: A firmware update is available. It fixes a bug in Pulse Gated trigger mode when used with multiple inputs.")
            print("To update, follow the instructions at https://sites.google.com/site/pulsepalwiki/updating-firmware")
        self.Port.write((self.OP_MENU_BYTE, 89, 80, 89, 84, 72, 79, 78), 'uint8')  # Client name op + 'PYTHON' in ASCII
        self.outputParameterNames = ['isBiphasic', 'phase1Voltage', 'phase2Voltage', 'phase1Duration', 
                                     'interPhaseInterval', 'phase2Duration', 'interPulseInterval', 'burstDuration', 
                                     'interBurstInterval', 'pulseTrainDuration', 'pulseTrainDelay', 
                                     'linkTriggerChannel1', 'linkTriggerChannel2', 'customTrainID',
                                     'customTrainTarget', 'customTrainLoop', 'restingVoltage']
        self.triggerParameterNames = ['triggerMode']
        self.set2DefaultParams()  # Initializes all parameters to default values
        self.syncAllParams()  # Sets all parameters on the device to the current class parameters

    def set2DefaultParams(self):
        """
           Returns all params to the defaults. This is called by the constructor, and may be
           subsequently called by the user (e.g. before running a new experiment)
        """
        self.isBiphasic = [float('nan'), 0, 0, 0, 0]
        self.phase1Voltage = [float('nan'), 5, 5, 5, 5]
        self.phase2Voltage = [float('nan'), -5, -5, -5, -5]
        self.restingVoltage = [float('nan'), 0, 0, 0, 0]
        self.phase1Duration = [float('nan'), 0.001, 0.001, 0.001, 0.001]
        self.interPhaseInterval = [float('nan'), 0.001, 0.001, 0.001, 0.001]
        self.phase2Duration = [float('nan'), 0.001, 0.001, 0.001, 0.001]
        self.interPulseInterval = [float('nan'), 0.01, 0.01, 0.01, 0.01]
        self.burstDuration = [float('nan'), 0, 0, 0, 0]
        self.interBurstInterval = [float('nan'), 0, 0, 0, 0]
        self.pulseTrainDuration = [float('nan'), 1, 1, 1, 1]
        self.pulseTrainDelay = [float('nan'), 0, 0, 0, 0]
        self.linkTriggerChannel1 = [float('nan'), 1, 1, 1, 1]
        self.linkTriggerChannel2 = [float('nan'), 0, 0, 0, 0]
        self.customTrainID = [float('nan'), 0, 0, 0, 0]
        self.customTrainTarget = [float('nan'), 0, 0, 0, 0]
        self.customTrainLoop = [float('nan'), 0, 0, 0, 0]
        self.triggerMode = [float('nan'), 0, 0]

    def setFixedVoltage(self, channel, voltage):
        """
        Sets a fixed voltage for the specified output channel.

        Args:
            channel (int): The channel number to set (1-4)
            voltage (float): The voltage level to set. Units = Volts.

        Raises:
            PulsePalError: If the device does not acknowledge the command.
        """
        voltage_bits = self._volts2Bits(voltage)
        if self._model == 1:
            self.Port.write((self.OP_MENU_BYTE, 79, channel, voltage_bits), 'uint8')
        else:
            self.Port.write((self.OP_MENU_BYTE, 79, channel), 'uint8', voltage_bits, 'uint16')
        ok = self.Port.read(1, 'uint8')  # Receive acknowledgement
        if len(ok) == 0:
            raise PulsePalError('Error: Pulse Pal did not return an acknowledgement after a call to setFixedVoltage().')
        
    def programOutputChannelParam(self, param_name, channel, value):
        """
        Programs a parameter for an output channel on the Pulse Pal device.

        Args:
            param_name (str): The name of the parameter to program. Names are given above in self.outputParameterNames.
            channel (int): The output channel number to program the parameter for (1-4)
            value: The value to set for the parameter. Units: Voltage (if volts), Seconds (if time), Integer (if item)

        Raises:
            PulsePalError: If the device does not acknowledge the command.
        """
        original_value = value
        if isinstance(param_name, str):
            param_code = self.outputParameterNames.index(param_name)+1
        else:
            param_code = param_name
        if 2 <= param_code <= 3 or param_code == 17:
            value = self._volts2Bits(value)
            if self._model == 1:
                self.Port.write((self.OP_MENU_BYTE, 74, param_code, channel, value), 'uint8')
            else:
                self.Port.write((self.OP_MENU_BYTE, 74, param_code, channel), 'uint8', value, 'uint16')
        elif 4 <= param_code <= 11:
            self.Port.write((self.OP_MENU_BYTE, 74, param_code, channel), 'uint8', self._seconds2Cycles(value), 'uint32')
        else:
            self.Port.write((self.OP_MENU_BYTE, 74, param_code, channel, value), 'uint8')

        # Receive acknowledgement
        ok = self.Port.read(1, 'uint8')
        if len(ok) == 0:
            raise PulsePalError('Pulse Pal did not return an acknowledgement after call to programOutputChannelParam().')

        # Update the PulsePal object's parameter fields
        if param_code == 1:
            self.isBiphasic[channel] = original_value
        elif param_code == 2:
            self.phase1Voltage[channel] = original_value
        elif param_code == 3:
            self.phase2Voltage[channel] = original_value
        elif param_code == 4:
            self.phase1Duration[channel] = original_value
        elif param_code == 5:
            self.interPhaseInterval[channel] = original_value
        elif param_code == 6:
            self.phase2Duration[channel] = original_value
        elif param_code == 7:
            self.interPulseInterval[channel] = original_value
        elif param_code == 8:
            self.burstDuration[channel] = original_value
        elif param_code == 9:
            self.interBurstInterval[channel] = original_value
        elif param_code == 10:
            self.pulseTrainDuration[channel] = original_value
        elif param_code == 11:
            self.pulseTrainDelay[channel] = original_value
        elif param_code == 12:
            self.linkTriggerChannel1[channel] = original_value
        elif param_code == 13:
            self.linkTriggerChannel2[channel] = original_value
        elif param_code == 14:
            self.customTrainID[channel] = original_value
        elif param_code == 15:
            self.customTrainTarget[channel] = original_value
        elif param_code == 16:
            self.customTrainLoop[channel] = original_value
        elif param_code == 17:
            self.restingVoltage[channel] = original_value
            
    def programTriggerChannelParam(self, param_name, channel, value):
        """
        Programs a parameter for the trigger channel on the Pulse Pal device.

        Args:
            param_name (str): The name of the parameter to program. Names are given above in self.triggerParameterNames.
            channel (int): The trigger channel number to program the parameter for (1-2)
            value: The value to set for the parameter.

        Raises:
            PulsePalError: If the device does not acknowledge the command.
        """
        original_value = value
        if isinstance(param_name, str):
            param_code = self.triggerParameterNames.index(param_name)+128
        else:
            param_code = param_name
        self.Port.write((self.OP_MENU_BYTE, 74, param_code, channel, value), 'uint8')
        # Receive acknowledgement
        ok = self.Port.read(1, 'uint8')
        if len(ok) == 0:
            raise PulsePalError('Error: Pulse Pal did not return acknowledgement after call to programTriggerChannelParam().')
        if param_code == 1:
            self.triggerMode[channel] = original_value
            
    def syncAllParams(self):
        """
        Synchronizes all current parameters of the PulsePalObject to the device

        Raises:
            PulsePalError: If the device does not acknowledge the synchronization command.
        """
        # Preallocate
        program_values_16 = []
        program_values_32 = []
        if self._model == 1:
            program_values_8 = [0]*28
        else:
            program_values_8 = [0]*16

        # Prepare 32-bit time params
        pos = 0
        for i in range(1, 5):
            program_values_32.extend([
                self._seconds2Cycles(self.phase1Duration[i]),
                self._seconds2Cycles(self.interPhaseInterval[i]),
                self._seconds2Cycles(self.phase2Duration[i]),
                self._seconds2Cycles(self.interPulseInterval[i]),
                self._seconds2Cycles(self.burstDuration[i]),
                self._seconds2Cycles(self.interBurstInterval[i]),
                self._seconds2Cycles(self.pulseTrainDuration[i]),
                self._seconds2Cycles(self.pulseTrainDelay[i])
            ])
        
        # Prepare 16-bit voltages for Pulse Pal v2 (Pulse Pal v1 has 8-bit voltages set with other 8-bit params below)
        if self._model == 2:
            pos = 0
            for i in range(1, 5):
                program_values_16.extend([
                    self._volts2Bits(self.phase1Voltage[i]),
                    self._volts2Bits(self.phase2Voltage[i]),
                    self._volts2Bits(self.restingVoltage[i])
                ])

        # Prepare 8-bit params
        pos = 0
        for i in range(1, 5):
            program_values_8[pos] = self.isBiphasic[i]
            pos += 1
            if self._model == 1:
                program_values_8[pos] = self._volts2Bits(self.phase1Voltage[i])
                pos += 1
                program_values_8[pos] = self._volts2Bits(self.phase2Voltage[i])
                pos += 1
            program_values_8[pos] = self.customTrainID[i]
            pos += 1
            program_values_8[pos] = self.customTrainTarget[i]
            pos += 1
            program_values_8[pos] = self.customTrainLoop[i]
            pos += 1
            if self._model == 1:
                program_values_8[pos] = self._volts2Bits(self.restingVoltage[i])
                pos += 1

        # Prepare trigger channel link params
        program_values_tl = [0]*8
        pos = 0
        for i in range(1, 5):
            program_values_tl[pos] = self.linkTriggerChannel1[i]
            pos += 1
        for i in range(1, 5):
            program_values_tl[pos] = self.linkTriggerChannel2[i]
            pos += 1
            
        # Send all params to device
        if self._model == 1:
            self.Port.write(
                (self.OP_MENU_BYTE, 73), 'uint8',
                program_values_32, 'uint32',
                program_values_8, 'uint8',
                program_values_tl, 'uint8',
                self.triggerMode[1:3], 'uint8')
        if self._model == 2:
            self.Port.write(
                (self.OP_MENU_BYTE, 73), 'uint8',
                program_values_32, 'uint32',
                program_values_16, 'uint16',
                program_values_8, 'uint8',
                program_values_tl, 'uint8',
                self.triggerMode[1:3], 'uint8')

        # Receive acknowledgement
        ok = self.Port.read(1, 'uint8')
        if len(ok) == 0:
            raise PulsePalError('Error: Pulse Pal did not return an acknowledgement byte after a call to syncAllParams().')
        
    def sendCustomPulseTrain(self, custom_train_id, pulse_times, pulse_voltages):
        """
        Sends a custom pulse train to the Pulse Pal device.

        Args:
            custom_train_id (int): The ID of the custom train to send (1-2)
            pulse_times (list of float): The times at which each pulse should occur. Units = seconds.
            pulse_voltages (list of float): The voltages for each pulse. Units = volts.

        Raises:
            PulsePalError: If the device does not acknowledge the command.
        """
        if isinstance(pulse_times, np.ndarray):
            pulse_times = pulse_times.tolist()
        if isinstance(pulse_voltages, np.ndarray):
            pulse_voltages = pulse_voltages.tolist()
        n_pulses = len(pulse_times)
        for i in range(0, n_pulses):
            pulse_times[i] = self._seconds2Cycles(pulse_times[i])  # Convert seconds to multiples of update cycle (100us)
            pulse_voltages[i] = self._volts2Bits(pulse_voltages[i])
        
        op_code = custom_train_id + 74  #Serial op codes are 75 if custom train 1, 76 if 2
        if self._model == 1:
            self.Port.write((self.OP_MENU_BYTE, op_code, 0), 'uint8', n_pulses, 'uint32', pulse_times, 'uint32', pulse_voltages, 'uint8')
        else:
            self.Port.write((self.OP_MENU_BYTE, op_code), 'uint8', n_pulses, 'uint32', pulse_times, 'uint32', pulse_voltages, 'uint16')
        ok = self.Port.read(1, 'uint8')  # Receive acknowledgement
        if len(ok) == 0:
            raise PulsePalError('Error: Pulse Pal did not return an acknowledgement byte after a call to sendCustomPulseTrain().')
        
    def sendCustomWaveform(self, custom_train_id, pulse_width, pulse_voltages):  # For custom pulse trains with pulse times = pulse width
        """
        Sends a custom waveform to the Pulse Pal device.

        Args:
            custom_train_id (int): The ID of the custom waveform train to send (1-2)
            pulse_width (float): The width of each pulse in the waveform. Units = seconds.
            pulse_voltages (list of float): The voltages for each pulse in the waveform. Units = volts.

        Raises:
            PulsePalError: If the device does not acknowledge the command.
        """
        n_pulses = len(pulse_voltages)
        pulse_times = [0]*n_pulses
        pulse_width_cycles = self._seconds2Cycles(pulse_width)  # Convert seconds to multiples of minimum cycle (100us)
        if isinstance(pulse_voltages, np.ndarray):
            pulse_voltages = pulse_voltages.tolist()
        for i in range(0, n_pulses):
            pulse_times[i] = pulse_width_cycles*i  # Add consecutive pulse
            pulse_voltages[i] = self._volts2Bits(pulse_voltages[i])
        op_code = custom_train_id + 74  # 75 if custom train 1, 76 if 2
        if self._model == 1:
            self.Port.write((self.OP_MENU_BYTE, op_code, 0), 'uint8', n_pulses, 'uint32', pulse_times, 'uint32', pulse_voltages, 'uint8')
        else:
            self.Port.write((self.OP_MENU_BYTE, op_code), 'uint8', n_pulses, 'uint32', pulse_times, 'uint32', pulse_voltages, 'uint16')
        # Receive acknowledgement
        ok = self.Port.read(1, 'uint8')
        if len(ok) == 0:
            raise PulsePalError('Error: Pulse Pal did not return an acknowledgement byte after a call to sendCustomWaveform().')

    def setContinuousLoop(self, channel, state):
        """
        Sets the continuous loop state for a specified output channel.

        Args:
            channel (int): The output channel number to set the continuous loop state (1-4)
            state (int): The state to set for the continuous loop (1 for on, 0 for off).
        """
        self.Port.write((self.OP_MENU_BYTE, 82, channel, state), 'uint8')

    def triggerOutputChannels(self, channel1, channel2, channel3, channel4):
        """
        Triggers the output channels on the Pulse Pal device.

        Args:
            channel1 (int): 1 to trigger Ch1, 0 if not
            channel2 (int): 1 to trigger Ch2, 0 if not
            channel3 (int): 1 to trigger Ch3, 0 if not
            channel4 (int): 1 to trigger Ch4, 0 if not
        """
        trigger_byte = (1*channel1) + (2*channel2) + (4*channel3) + (8*channel4)
        self.Port.write((self.OP_MENU_BYTE, 77, trigger_byte), 'uint8')

    def abortPulseTrains(self):
        """
        Aborts all pulse trains currently being output by the Pulse Pal device.
        """
        self.Port.write((self.OP_MENU_BYTE, 80), 'uint8')

    def _toDecimal(self, value):
        """
        Converts a value to a Decimal with a Pulse Pal's required precision.

        Args:
            value (float): The value to convert to Decimal.

        Returns:
            Decimal: The value converted to a Decimal with fixed precision (0.0000)
        """
        return Decimal(value).quantize(Decimal('1.0000'))

    def _volts2Bits(self, value):
        """
        Converts a voltage value in range -10V to +10V to its corresponding bit value for the 12-bit DAC.

        Args:
            value (float): The voltage value to convert.

        Returns:
            int: The bit value corresponding to the given voltage.
        """
        return math.ceil(((self._toDecimal(value) + 10) / self._toDecimal(20)) * self._dac_bitMax)

    def _seconds2Cycles(self, value):
        """
        Converts a time value in seconds to the corresponding number of refresh cycles for the Pulse Pal device.

        Args:
            value (float): The time value in seconds to convert.

        Returns:
            Decimal: The number of cycles corresponding to the given time value.
        """
        return self._toDecimal(value)*self._toDecimal(self.CYCLE_FREQUENCY)

    def __del__(self):
        """
        Destructor method that ensures the Pulse Pal connection is closed if the object is deleted.
        """
        self.Port.write((self.OP_MENU_BYTE, 81), 'uint8')
        self.Port.close()









class PulsePalError(Exception):
    pass


class PulsePal:
    def __init__(self, address, channel=1):

        self.com = PulsePalObject(port_name=address)
        
        self.channel = channel
        self.com.programTriggerChannelParam('triggerMode', channel, 0)
        self.com.isBiphasic[1:5] = [0] * 4
        self.com.phase1Voltage[1:5] = [10] * 4
        self.com.restingVoltage[1:5] = [0] * 4
        self.com.syncAllParams()
        self.pulse_width = [0, 0, 0]
        self.c1, self.c2, self.c3, self.c4 = 0, 0, 0, 0

        if self.channel == 1:
            self.c1 = 1
        elif self.channel == 2:
            self.c2 = 2
        elif self.channel == 3:
            self.c3 = 1
        else:
            self.c4 = 1

    def disconnect(self):
        self.com.disconnect()

    # assigning the pulses takes aprox 50 ms for each second of duration of the pulse
    # so you need to assign the pulses at the beggining of the task
    # there can be 2 pulses stored at the same time: pulse_number=1 and pulse_number=2
    def assign_pulse(self, pulse, pulse_number):
        if pulse_number not in [1, 2]:
            print('you can only use pulse_number 1 or 2')
            raise
        pulse_width = pulse[0]
        voltages = pulse[1]

        try:
            self.com.sendCustomWaveform(pulse_number, pulse_width, voltages)
        except:
            time.sleep(0.1)
            self.com.sendCustomWaveform(pulse_number, pulse_width, voltages)
            print("------------- pulse assigned in second attempt")
            
        self.pulse_width[pulse_number] = pulse_width

        #self.com.programOutputChannelParam('customTrainID', self.channel, pulse_number)
        #self.com.programOutputChannelParam('phase1Duration', self.channel, self.pulse_width[pulse_number])

    # this is super fast, less than 1 ms
    def trigger_pulse(self, pulse_number):
        try:
            self.com.programOutputChannelParam('customTrainID', self.channel, pulse_number)
            self.com.programOutputChannelParam('phase1Duration', self.channel, self.pulse_width[pulse_number])
            self.com.abortPulseTrains()
            self.com.triggerOutputChannels(self.c1, self.c2, self.c3, self.c4)
        except:
            time.sleep(0.1)
            self.com.programOutputChannelParam('customTrainID', self.channel, pulse_number)
            self.com.programOutputChannelParam('phase1Duration', self.channel, self.pulse_width[pulse_number])
            self.com.abortPulseTrains()
            self.com.triggerOutputChannels(self.c1, self.c2, self.c3, self.c4)
            print("------------- pulse triggered in second attempt")

    def stop_pulse(self):
        self.com.abortPulseTrains()


    # methods to create different types of pulses
    # need to return (pulse_width=float, voltages=[floats])
    @staticmethod
    def create_square_pulse(duration, duration_ramp_in, duration_ramp_off, voltage, samples_per_second= 500):
        duration_samples = int(duration * samples_per_second)
        duration_ramp_in_samples = duration_ramp_in * samples_per_second
        duration_ramp_off_samples = duration_ramp_off * samples_per_second
        start_ramp_off_samples = duration_samples - duration_ramp_off_samples
        voltages = list(range(0, duration_samples))
        for i in voltages:
            if i < duration_ramp_in_samples:
                voltages[i] = i * voltage / duration_ramp_in_samples
            elif i > start_ramp_off_samples:
                voltages[i] = voltage - (i - start_ramp_off_samples) * voltage / duration_ramp_off_samples
            else:
                voltages[i] = voltage
        pulse_width = 1 / samples_per_second
        pulse = (pulse_width, voltages)
        return pulse


    @staticmethod
    def create_square_pulsetrain(duration, time_on, time_off, voltage, samples_per_second= 1000):
        duration_samples = int(duration * samples_per_second)
        voltages = list(range(0, duration_samples))
        samples_on = time_on * samples_per_second
        samples_off = time_off * samples_per_second
        samples_pulse = samples_on + samples_off
        for i in voltages:
            j = i % samples_pulse
            if j < samples_on:
                voltages[i] = voltage
            else:
                voltages[i] = 0
        pulse_width = 1 / samples_per_second
        pulse = (pulse_width, voltages)

        return pulse



class FakePulsePal():
    def __init__(self, address, channel=1):

        self.address = address
        self.name = "fake"


    def disconnect(self):
        pass

    def assign_pulse(self, pulse, pulse_number):
        pass

    def trigger_pulse(self, pulse_number):
        pass

    def stop_pulse(self):
        pass

    @staticmethod
    def create_square_pulse(duration, duration_ramp_in, duration_ramp_off, voltage, samples_per_second= 1000):
        pass


    @staticmethod
    def create_square_pulsetrain(duration, time_on, time_off, voltage, samples_per_second= 1000):
        pass
