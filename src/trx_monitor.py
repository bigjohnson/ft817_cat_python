'''
Created on Dec 31, 2016

@author: 4X5DM

@note: The program uses the FT897 class to query the transceiver and to print
       its state.
       Serial port name is defined by SERIAL_PORT constant.
'''

from ft897 import FT897
import time

# Constants
SERIAL_PORT = "COM8"
# Set the corect speed on radio or program
SERIAL_SPEED = 38400

if __name__ == '__main__':
    print ("Starting FT-897D monitor...")
    try:
        ft897 = FT897(SERIAL_PORT, SERIAL_SPEED,)

        #Valid frequency
        #ft897.write_frequency("4423750")
        #Invalid frequency
        #ft897.write_frequency("60000000")

        #ft897.write_mode("FM")

        ft897.read_frequency()
        if ft897.read_receiving():
            print("Receiving")
            ft897.read_rx_status()
            #print(ft897.get_s_meter_rx_string(ft897._s_meter))
            print(ft897.get_rx_state_string())
        else:
            print("Trasmitting")
            ft897.read_tx_status()
            print(ft897.get_tx_state_string())


            #ft897.read_frequency()
            #print(ft897._frequency)
            #print(ft897._mode)

    except KeyboardInterrupt:
        # KeyboardInterrupt exception is thrown when CTRL-C or CTRL-Break is pressed.
        pass
    except Exception as msg:
        print ("\r\nError has occured. Error message:")
        print (msg)
        print ("\r\n")
#    finally:
#        print ("See you later. 73!")
