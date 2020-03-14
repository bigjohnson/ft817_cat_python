'''
Created on 06 May 2016
Updated on 31 Dec 2016

@author: Dmitry Melnichansky 4X5DM ex 4Z7DTF
         https://github.com/4x5dm
         http://www.qrz.com/db/4X5DM

@note: FT897 class which communicates with FT-897 using serial library,
       queries and sets transceiver's frequency and state and generates
       transceiver state strings for printing.

'''

import serial
import sys
class FT897(object):

    # Constants
    # Serial port settings
    SERIAL_SPEED = 9600
    SERIAL_STOPBITS = serial.STOPBITS_TWO
    SERIAL_TIMEOUT = 1.0
    # Transceiver modes and commands
    MODES = ["LSB", "USB", "CW", "CWR", "AM", None, "WFM", None, "FM", None, "DIG", None, "PKT"]
    CMD_READ_FREQ = [0x00, 0x00, 0x00, 0x00, 0x03]
    CMD_READ_RX_STATUS = [0x00, 0x00, 0x00, 0x00, 0xE7]
    CMD_SET_FREQ  = [0x00, 0x00, 0x00, 0x00, 0x01]
    CMD_SET_MODE  = [0x00, 0x00, 0x00, 0x00, 0x07]
    CMD_READ_TX_STATUS = [0x00, 0x00, 0x00, 0x00, 0xF7]
    CMD_READ_TX_METER = [0x00, 0x00, 0x00, 0x00, 0xBD]

    def __init__(self, serial_port, serial_speed=SERIAL_SPEED, serial_stopbits=SERIAL_STOPBITS):
        self._serial = serial.Serial(serial_port, serial_speed, stopbits=serial_stopbits, timeout=FT897.SERIAL_TIMEOUT)
        self._frequency = ""
        self._mode = ""
        self._squelch = True
        self._s_meter = ""
        self._ctcss_dcs = True
        # self._start = True
        self._discriminator = True
        self._t_power = ""
        self._t_alc = ""
        self._t_vswr = ""
        self._t_mod = ""
        # Read frequency tseting radio connection!

        # print("Initializing radio connected to ", end='')
        # print(serial_port, end='')
        # print(" at ", end='')
        # print(serial_speed, end='')
        # print(" bps...")
        self.read_frequency()
        return

    def read_receiving(self):
        self._serial.write(FT897.CMD_READ_TX_STATUS)
        resp = self._serial.read(1)
        #print(resp[0])
        self.check_reponse(resp);
        if resp[0] == 0xff:
            # print("Not tramsitting.")
            return True
        else:
            # print("Trasmitting.")
            return False

    def read_frequency(self):
        '''Queries transceiver RX frequency and mode.
        The response is 5 bytes: first four store frequency and
        the fifth stores mode (AM, FM, SSB etc.)
        '''
        # if self._start:
        #     self._start = False
        # else:
        #     print("Reading frequency...")

        cmd = FT897.CMD_READ_FREQ
        self._serial.write(cmd)
        resp = self._serial.read(5)
        #if len(resp) == 0:
        #    #print("Error: the radio did not respond!")
        #    sys.stderr.write("Error: the radio did not respond!")
        #    exit(1)

        self.check_reponse(resp);

        #resp_bytes = (ord(resp[0]), ord(resp[1]), ord(resp[2]), ord(resp[3]))
        resp_bytes = (resp[0], resp[1], resp[2], resp[3])
        self._frequency = "%02x%02x%02x%02x" % resp_bytes

        # print(resp[0])
        # print(resp[1])
        # print(resp[2])
        # print(resp[3])
        #
        # print()
        # print(int(self._frequency, 10))
        #
        # print()
        # print(self._frequency[0:2])
        # print(self._frequency[2:4])
        # print(self._frequency[4:6])
        # print(self._frequency[6:8])
        #
        # print()
        # print(int(self._frequency[0:2], 16))
        # print(int(self._frequency[2:4], 16))
        # print(int(self._frequency[4:6], 16))
        # print(int(self._frequency[6:8], 16))
        #
        # print("runned")

        #self._mode = FT897.MODES[ord(resp[4])]
        self._mode = FT897.MODES[resp[4]]

    def write_mode(self, mode):

        mode = mode.upper()

        if mode == "LSB" :
            modenum = 0x00
        elif mode == "USB" :
            modenum = 0x01
        elif mode == "CW" :
            modenum = 0x02
        elif mode == "CWR" :
            modenum = 0x03
        elif mode == "AM" :
            modenum = 0x04
        elif mode == "FM" :
            modenum = 0x08
        elif mode == "DIG" :
            modenum = 0x0A
        elif mode == "PKT" :
            modenum = 0x0C
        else:
            modenum = 0x0D

        if modenum < 0x0D:
            FT897.CMD_SET_MODE[0] = modenum
            self._serial.write(FT897.CMD_SET_MODE)
            resp = self._serial.read(1)
            self.check_reponse(resp);
            return True
            # print("Mode is set to ", end='')
            # print(mode, end='')
            # print(".")
        # else:
        #     print("Error: ", end='')
        #     print(mode, end='')
        #     print(" invalid mode!")
        return False

    def write_frequency(self, new_frequency):
        #new_frequency = "14523750"
        # print("Writing new frequency: ", end='')
        # print(new_frequency, end='')
        # print("...")
        if new_frequency.isdigit():
            new_frequency_bytes = [int(new_frequency[0:2], 16), int(new_frequency[2:4], 16), int(new_frequency[4:6], 16), int(new_frequency[6:8], 16)]

            # print()
            # print(new_frequency_bytes[0])
            # print(new_frequency_bytes[1])
            # print(new_frequency_bytes[2])
            # print(new_frequency_bytes[3])
            #
            #

            FT897.CMD_SET_FREQ[0] = new_frequency_bytes[0]
            FT897.CMD_SET_FREQ[1] = new_frequency_bytes[1]
            FT897.CMD_SET_FREQ[2] = new_frequency_bytes[2]
            FT897.CMD_SET_FREQ[3] = new_frequency_bytes[3]

            # print()
            # print(FT897.CMD_SET_FREQ[0])
            # print(FT897.CMD_SET_FREQ[1])
            # print(FT897.CMD_SET_FREQ[2])
            # print(FT897.CMD_SET_FREQ[3])

            self._serial.write(FT897.CMD_SET_FREQ)
            resp = self._serial.read(1)

            self.check_reponse(resp);

            #print(resp)
            if resp[0] == 0:
                #print("Frequency write correctly.")
                return True
            elif resp[0] == 0xF0:
                # sys.stderr.write("Frequency write error.")
                return False
            else:
                # sys.stderr.write("Unknown return code.")
                return False
        else:
            return False

    def read_rx_status(self):
        '''Queries transceiver RX status.
        The response is 1 byte:
        bit 7: Squelch status: 0 - off (signal present), 1 - on (no signal)
        bit 6: CTCSS/DCS Code: 0 - code is matched, 1 - code is unmatched
        bit 5: Discriminator centering: 0 - discriminator centered, 1 - uncentered
        bit 4: Dummy data
        bit 3-0: S Meter data
        '''
        #print("Reading status")
        cmd = FT897.CMD_READ_RX_STATUS
        self._serial.write(cmd)
        resp = self._serial.read(1)

        self.check_reponse(resp);

        #resp_byte = ord(resp[0])
        resp_byte = resp[0]
        self._squelch = True if (resp_byte & 0B10000000) else False
        self._ctcss_dcs = True if (resp_byte & 0B01000000) else False
        self._s_meter = resp_byte & 0x0F

    def read_tx_status(self):
        cmd = FT897.CMD_READ_TX_METER
        self._serial.write(cmd)
        resp = self._serial.read(2)

        self.check_reponse(resp);

        if resp[0] != 0x00:
            self._t_power = resp[0] & 0x0F

            self._t_alc = resp[0] & 0xF0
            self._t_alc = self._t_alc >> 4

            self._t_vswr = resp[1] & 0x0F

            self._t_mod = resp[0] & 0xF0
            self._t_mod = self._t_mod >> 4

        return

    def get_s_meter_rx_string(self, s_meter):
        '''Generates S-Meter string for printing. The string includes
        S value with decibels over 9 is printed and a simple 15 symbols scale.
        Examples:
        S0:      S0+00 ...............
        S3:      S3+00 |||............
        S9:      S9+00 |||||||||......
        S9+20dB: S9+00 |||||||||||....
        '''
        res = "S9" if s_meter >= 9 else "S" + str(s_meter)
        above_nine = s_meter - 9
        if above_nine > 0:
            res += "+%s" % (10 * above_nine)
        else:
            res += "+00"
        res += " "
        res += "|" * s_meter
        res += "." * (15 - s_meter)
        return res

    def get_rx_state_string(self):
        '''Returns transceiver state data for printing.
        '''
        s_meter_str = self.get_s_meter_rx_string(self._s_meter)
        sql_str = 'SQL: ON' if self._squelch else 'SQL: OFF'
        ctcss_dcs_string = 'CTCSS-DCS: DETECTED' if self._ctcss_dcs else 'CTCSS-DCS: UNDETECTED'
        if self._mode == "FM":
            discriminator_string = "DISCRIMINATOR: NOT CENTERED" if self._discriminator else  "DISCRIMINATOR: CENTERED"
            res = "%s0Hz\r\n%s\r\n%s\r\n%s\r\n%s\r\n%s" % (self._frequency, self._mode, sql_str, ctcss_dcs_string, discriminator_string, s_meter_str)
        else:
            res = "%s0Hz\r\n%s\r\n%s\r\n%s\r\n%s" % (self._frequency, self._mode, sql_str, ctcss_dcs_string, s_meter_str)
        return res

    def get_tx_state_string(self):
            res = "%s0HZ\r\n%s\r\nPower: %i\r\nAlc: %i\r\nVswr: %i\r\nMod: %i\r\n" % (self._frequency, self._mode, self._t_power, self._t_alc, self._t_vswr, self._t_mod)
            return res

    def check_reponse(self,reponse):
        if len(reponse) == 0:
            #print("Error: the radio did not respond!")
            sys.stderr.write("Error: Radio not connected!\n")
            #self.RADIO_OK = False
            exit();
            return
        #self.RADIO_OK = True
        return

    def __str__(self):
        '''Overrides __str__() method for using FT897 class with print command.
        '''
        return self.get_trx_state_string()


#     def loop(self, samples_per_sec):
#         '''Infinite loop which queries the transceiver and prints the data.
#         Number of queries per second is passed in samples_per_sec variable.
#         '''
#         delay = 1.0 / samples_per_sec
#         while True:
#             self.read_frequency()
#             self.read_rx_status()
#             self.print_data()
#             time.sleep(delay)
#
# if __name__ == '__main__':
#     ft897 = FT897()
#     ft897.loop(SAMPLES_PER_SEC)
