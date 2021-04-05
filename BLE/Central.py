from bluepy.btle import *
import mqtt_client
import time

MACADD1 = ""
MACADD2 = ""
MACADD3 = ""

room1Temp = 0.0
room2Temp = 0.0
room3Temp = 0.0

room1Bool = True
room2Bool = True
room3Bool = True
        
def aggregate(tempReading, humidityReading, roomName):
    global room1Temp, room2Temp, room3Temp
    
    print("current temp is: "+str(tempReading))
    
    #Divide by room name
    if(roomName == "Room 1"):
        mqtt_client.send(tempReading, humidityReading, "temp1", "hum1")
        print("Temp set to:"+str(room1Temp))
        differ = tempReading-room1Temp
        if tempReading<=room1Temp:
            return 0
        elif differ>0 and differ<3:
            return 1
        elif differ>=3 and differ<5:
            return 2
        else:
            return 3

    elif(roomName == "Room 2"):
        mqtt_client.send(tempReading, humidityReading, "temp2", "hum2")
        print("Temp set to:"+str(room2Temp))
        differ = tempReading-room2Temp
        if tempReading<=room2Temp:
            return 0
        elif differ>0 and differ<3:
            return 1
        elif differ>=3 and differ<5:
            return 2
        else:
            return 3
        
    elif(roomName == "Room 3"):
        mqtt_client.send(tempReading, humidityReading, "temp3", "hum3")
        print("Temp set to:"+str(room3Temp))
        differ = tempReading-room3Temp
        if tempReading<=room3Temp:
            return 0
        elif differ>0 and differ<3:
            return 1
        elif differ>=3 and differ<5:
            return 2
        else:
            return 3

def getSetCharacteristics(macadd, uuidService, uuidTemp, uuidHumid, uuidFan, roomName):
    #Variable declaration
    returnedTemp = 0.0
    returnedHumidity = 0.0

    #Sanity check for Address
    t1 = time.time()
    if macadd != "":
        print("Connecting to "+roomName+"...")
        conn = Peripheral(macadd, ADDR_TYPE_PUBLIC)
        print("Getting "+roomName+" service")
        service = conn.getServiceByUUID(uuidService)
        collCharacteristics = service.getCharacteristics()
        for characteristicsA in collCharacteristics:
            if characteristicsA.uuid == uuidTemp:
                if characteristicsA.supportsRead():
                    tempString = characteristicsA.read().decode('utf-8')
                    returnedTemp = round(float(tempString.split()[0]),1)
                else:
                    print("Unable to read temperature characteristic")
    
            #Humidity Characteristic
            elif characteristicsA.uuid == uuidHumid:
                if characteristicsA.supportsRead():
                    returnedHumidity = round(float(characteristicsA.read().decode('utf-8')),1)
                else:
                    print("Unable to read humidity characteristic")

            #Fan Characteristic
            elif characteristicsA.uuid == uuidFan:
                returnedFanSpeed = aggregate(returnedTemp, returnedHumidity, roomName)
                print("Setting fan speed to "+str(returnedFanSpeed))
                characteristicsA.write(bytes(str(returnedFanSpeed).encode()))
                print("Written new fan speed")
        
        t2 = time.time()
        print(str((t2-t1)*1000))
        conn.disconnect()

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

###############################
#   START MAIN RUNNING SPACE  #
###############################

while room1Bool:
    try:
        room1Temp = round(float(input("Please enter temperature for Room 1\n")),1)
        room1Bool = False
    except:
        print("Invalid input. Please input a correct temperature format (eg. 32.5)\n")

while room2Bool:
    try:
        room2Temp = round(float(input("Please enter temperature for Room 2\n")),1)
        room2Bool = False
    except:
        print("Invalid input. Please input a correct temperature format (eg. 32.5)\n")

while room3Bool:
    try:
        room3Temp = round(float(input("Please enter temperature for Room 3\n")),1)
        room3Bool = False
    except:
        print("Invalid input. Please input a correct temperature format (eg. 32.5)\n")

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

for dev in devices:
    for (adtype, desc, value) in dev.getScanData():
        if value == "Room 1":
            MACADD1 = str(dev.addr)
        elif value == "Room 2":
            MACADD2 = str(dev.addr)
        elif value == "Room 3":
            MACADD3 = str(dev.addr)

while True:
    print("\n\n\nWE WILL BE BACK AFTER THESE MESSAGES\n\n\n")
    time.sleep(7)
    
    #Room 1
    getSetCharacteristics(MACADD1,"bc45161a-015b-4e8f-908f-2a5fb020317b","83a2cbfa-3eb4-43d2-8cf7-c3b2719eb1c3","9ffd5835-08bd-4af8-80fa-c67ce445a0b7","27cdab00-3890-41db-b760-47881963f5c8","Room 1")
    
    #Room 2
    getSetCharacteristics(MACADD2,"1919f6c8-3f35-48d4-a016-610aa8723300","fe3732db-2827-4dc3-bc7e-8d9408a32332","96d077c7-8af7-4b17-a736-a50892344ea1","3c779608-5b6c-4249-8154-2d8953ac3431","Room 2")

    #Room 3
    getSetCharacteristics(MACADD3,"b6704fd8-4875-4ce5-afaa-25c70f457b69","4537c62b-c334-4d35-99d6-8e2f53761170","3de1307a-13ae-450e-b1a5-b2057159c5f6","33983793-e4ec-4244-bbcd-f42303a4f16a","Room 3")           
