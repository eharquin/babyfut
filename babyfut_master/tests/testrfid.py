from pirc522 import RFID
import signal
import time

rf_reader = RFID()

try:
    print('Starting...')
    while True:
        print('Waiting for a tag')
        rf_reader.wait_for_tag()
        (error, tag_type) = rf_reader.request()
        
        if error:
            print('Error: {}'.format(error))
        else:
            (error, id) = rf_reader.anticoll()
            if error:
                print('Error: {}'.format(error))
            else:
                (error, tag_type) = rf_reader.request()
            print('RFID: {}'.format([hex(x) for x in id]))

except KeyboardInterrupt:
    print('Closing...')
    rf_reader.cleanup()