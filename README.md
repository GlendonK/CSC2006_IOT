# TEAM 2G2G
## CoAP and BLE implementation of a Smart Air-Conditioning System.<br>

### CoAP
This project is based off https://github.com/chrysn/aiocoap.git<br>
For more documentation and help visit https://aiocoap.readthedocs.io/en/latest/
- First enter the aiocoap folder with terminal and install the necessary packages.
     - `pip3 install --upgrade "aiocoap[all]"`
     - `pip3 install --upgrade "[linkheader,oscore,prettyprint,docs]`
     - `pip install LinkHeader`
     - `pip install paho-mqtt`
- Sencondly, run server.py on the server Raspberry Pi.
     - To bind pi ip go to aiocoap/aiocoap/transport/simplesocketserver.py and change ` if bind is None or bind[0] in ('localhost', '', None):` from <br> `class _DatagramServerSocketSimple(asyncio.DatagramProtocol):`
     to <br> ` if bind is None or bind[0] in ('<pi ip address here>', '', None):`
     
 - Third, run clientRunner.py on client Raspberry Pi to try GET, PUT methods on another Raspberry Pi.
 - To run OBSERVE method, run piOneObserve.py, piTwoObserve.py or piThreeObserve.py. 
     - The server Raspberry Pi IP address must be configured in the observe python code. to configure IP address: change <br>
     `request = Message(code=GET, uri='coap://<PI IP address here>/raspi/obs', observe=0)`<br> and
     `url = 'coap://<PI IP address here>/raspi/power'`

   ### BLE
   The BLE implementation of this project is based off https://github.com/IanHarvey/bluepy.git
   - Install the install the necessary packages from https://github.com/IanHarvey/bluepy.git
       - `sudo apt-get install python-pip libglib2.0-dev`
       - `sudo pip install bluepy`
       - `pip install paho-mqtt`
   - First make sure bluetooth is on. Then run `sudo python Central.py` in the BLE folder on the central Raspberry Pi.
   - Next, on all the edge Raspberry Pi, run `sudo python Peripheral.py`.
