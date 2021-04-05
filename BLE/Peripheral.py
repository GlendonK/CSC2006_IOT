import dbus
from sense_hat import SenseHat
from advertisement import Advertisement
from service import Application, Service, Characteristic, Descriptor

senseHatController = SenseHat()
senseHatController.clear()
senseHatController.low_light = True

def changeSpeed(fanSpeed):
    print("Changing speed to "+str(fanSpeed))
    humidity = senseHatController.get_humidity()
    if(humidity >= 53):
        senseHatController.show_letter(str(fanSpeed), (255, 0, 0))
    elif(humidity < 53 and humidity>=50):
        senseHatController.show_letter(str(fanSpeed), (255, 255, 0))
    elif(humidity < 50 and humidity>=48):
        senseHatController.show_letter(str(fanSpeed), (0, 255, 0))
    else:
        senseHatController.show_letter(str(fanSpeed), (255, 255, 255))
    

class MainAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("Room 1")
        self.include_tx_power = True

class MainService(Service):
    MAIN_SVC_UUID = "bc45161a-015b-4e8f-908f-2a5fb020317b"
    
    def __init__(self, index):

        Service.__init__(self, index, self.MAIN_SVC_UUID, True)
        self.add_characteristic(TempCharacteristic(self))
        self.add_characteristic(HumidCharacteristic(self))
        self.add_characteristic(FanCharacteristic(self))
        
class TempCharacteristic(Characteristic):
    TEMP_CHR_UUID = "83a2cbfa-3eb4-43d2-8cf7-c3b2719eb1c3"
    
    def __init__(self, service):
        self.notifying = False

        Characteristic.__init__(self, self.TEMP_CHR_UUID,["notify", "read"], service)
        self.add_descriptor(TempDescriptor(self))

    def get_temperature(self):
        value = []
        temp = senseHatController.get_temperature()

        strtemp = str(round(temp, 1)) + " C"
        for c in strtemp:
            value.append(dbus.Byte(c.encode()))

        return value

    def set_temperature_callback(self):
        if self.notifying:
            value = self.get_temperature()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = self.get_temperature()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_temperature()
        return value
    

class TempDescriptor(Descriptor):
    TEMP_DESCRIPTOR_UUID = "1000"
    TEMP_DESCRIPTOR_VALUE = "Room Temperature"
    
    def __init__(self, characteristic):
        Descriptor.__init__(self, self.TEMP_DESCRIPTOR_UUID,["read"],characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.TEMP_DESCRIPTOR_VALUE

        for c in desc:
            value.append(dbus.Byte(c.encode()))

        return value

class HumidCharacteristic(Characteristic):
    HUMIDITY_CHR_UUID = "9ffd5835-08bd-4af8-80fa-c67ce445a0b7"
    
    def __init__(self, service):
        self.notifying = False

        Characteristic.__init__(self, self.HUMIDITY_CHR_UUID,["notify", "read"], service)
        self.add_descriptor(HumidDescriptor(self))

    def get_humidity(self):
        value = []
        humidity = senseHatController.get_humidity()

        strtemp = str(round(humidity, 1))
        for c in strtemp:
            value.append(dbus.Byte(c.encode()))

        return value

    def set_humidity_callback(self):
        if self.notifying:
            value = self.get_humidity()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = self.get_humidity()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_humidity()

        return value
    
class HumidDescriptor(Descriptor):
    HUMIDITY_DESCRIPTOR_UUID = "2000"
    HUMIDITY_DESCRIPTOR_VALUE = "Room Humidity"
    
    def __init__(self, characteristic):
        Descriptor.__init__(self, self.HUMIDITY_DESCRIPTOR_UUID,["read"],characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.HUMIDITY_DESCRIPTOR_VALUE

        for c in desc:
            value.append(dbus.Byte(c.encode()))

        return value

class FanCharacteristic(Characteristic):
    global t2
    FAN_CHR_UUID = "27cdab00-3890-41db-b760-47881963f5c8"
    
    def __init__(self, service):
        self.notifying = False

        Characteristic.__init__(self, self.FAN_CHR_UUID,["notify", "read", "write"], service)
        self.add_descriptor(FanDescriptor(self))

    def get_fanSpeed(self):
        value = []
        fanSpeed = "0"

        value.append(dbus.Byte(fanSpeed.encode()))

        return value

    def set_fanSpeed_callback(self):
        if self.notifying:
            value = self.get_fanSpeed()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = self.get_fanSpeed()
        
        print("Fan speed changed to "+value)
        
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_fanSpeed()

        return value
    
    def WriteValue(self, value, options):
        print('Fan Speed WriteValue called')
        fanSpeed = int(''.join([str(v) for v in value]))
        changeSpeed(fanSpeed)

class FanDescriptor(Descriptor):
    FAN_DESCRIPTOR_UUID = "3000"
    FAN_DESCRIPTOR_VALUE = "Fan Speed"
    
    def __init__(self, characteristic):
        Descriptor.__init__(self, self.FAN_DESCRIPTOR_UUID,["read"],characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.FAN_DESCRIPTOR_VALUE

        for c in desc:
            value.append(dbus.Byte(c.encode()))

        return value

app = Application()
app.add_service(MainService(0))
app.register()

adv = MainAdvertisement(0)
adv.register()

try:
    app.run()
except KeyboardInterrupt:
    app.quit()