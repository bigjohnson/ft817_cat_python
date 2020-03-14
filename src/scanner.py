# The frequencies.csv format is:
# two coulumn with frequency and scan
# the frequency is 8 digit
# the scan could be yes or no, if is yes the frequency is scanned if no isn't
# the firts row is the heading
#
# Sample:
#
# frequency,scan
# 14520000,YES
# 14521250,YES
# 14522500,NO
# 14523750,YES
# 14525000,NO
# 14526250,YES
# 14527500,NO
# 14528750,YES
# 14530000,NO
# 14531250,YES

from ft897 import FT897
from datetime import datetime
import time
import csv

# Constants
SERIAL_PORT = "COM8"
# Set the corect speed on radio or program
SERIAL_SPEED = 38400
DELAY = 0.5

if __name__ == '__main__':
    print ("Starting FT-897D monitor...")
    try:
        ft897 = FT897(SERIAL_PORT, SERIAL_SPEED,)
        while True:
            #with open('frequencies.csv') as csv_file:
            with open('miei.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count > 0:
                        frequency = row[0]
                        scan = row[1]
                        if scan.upper() == "YES":
                            ft897.write_frequency(frequency)
                            time.sleep(DELAY)
                            now = datetime.now()
                            ft897.read_rx_status()
                            if ft897._squelch == False:
                                print(frequency, end = '')
                                print(",", end = '')
                                print(now)
                            # else:
                            #     print(line_count)
                    line_count += 1

            csv_file.close()
    # print(f'Processed {line_count} lines.')

        #Valid frequency
        #ft897.write_frequency("4423750")
        #Invalid frequency
        #ft897.write_frequency("60000000")

        #ft897.write_mode("FM")

        #
        # ft897.read_frequency()
        # if ft897.read_receiving():
        #     print("Receiving")
        #     ft897.read_rx_status()
        #     #print(ft897.get_s_meter_rx_string(ft897._s_meter))
        #     print(ft897.get_rx_state_string())
        # else:
        #     print("Trasmitting")
        #     ft897.read_tx_status()
        #     print(ft897.get_tx_state_string())




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
