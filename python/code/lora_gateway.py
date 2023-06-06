from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD

from parser import *

BOARD.setup()

class LoRaRcvCont(LoRa):
    def __init__(self, verbose = False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        #self.set_dio_mapping([1,0,0,0,0,0])

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(.5)
            rssi_value = self.get_rssi_value()
            status = self.get_modem_status()
            sys.stdout.write("\r%d %d %d" % (rssi_value, status['rx_ongoing'], status['modem_clear']))
            #sys.stdout.write("\n")
            sys.stdout.write("Waiting for inputs...")
            sys.stdout.flush()
            
    
    def on_rx_done(self):
        print("\nReceived: ")
        self.clear_irq_flags(RxDone = 1)
        payload = self.read_payload(nocheck = True)
        #data = ''.join([chr(c) for c in payload])
        #print(data)
        #string = bytes(payload).decode("utf-8",'ignore')
        #print(string)
        print(payload)
        string = payload
        #print(bytes(payload).decode("utf-8",'ignore'))
        
        print("\nSending Payload to Parser:")
        rssi_value = self.get_rssi_value()
        #parser(string, rssi_value);
        
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

lora = LoRaRcvCont(verbose = False)
lora.set_mode(MODE.STDBY)
#initializing lora to 434.0 MHz, Bw = 125kHz
lora.set_pa_config(pa_select = 1)

try:
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("")
    sys.stderr.write("Keyboard Interrupt\n")
finally:
    sys.stdout.flush()
    print("")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
