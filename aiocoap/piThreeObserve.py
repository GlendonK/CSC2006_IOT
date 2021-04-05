#!/usr/bin/env python3

# This file is part of the Python aiocoap library project.
#
# Copyright (c) 2012-2014 Maciej Wasilak <http://sixpinetrees.blogspot.com/>,
#               2013-2014 Christian Amsüss <c.amsuess@energyharvesting.at>
#
# aiocoap is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

"""This is a usage example of aiocoap that demonstrates how to implement a
simple client. See the "Usage Examples" section in the aiocoap documentation
for some more information."""

import logging
import asyncio
import json
import clientPUT
import mqtt_client
from time import time
from aiocoap import *
#import csv

logging.basicConfig(level=logging.INFO)

setTemp = 40
setHum = 40

async def main():
    protocol = await Context.create_client_context()

    request = Message(code=GET, uri='coap://192.168.43.67/raspi/obs', observe=0)
    

    startTime = int(time() * 1000)

    pr = protocol.request(request)

    r = await pr.response
    print("First response: %s\n%r"%(r, r.payload))

    async for r in pr.observation:
        #print("Next result: %s\n%r"%(r, r.payload))
        data = json.loads(r.payload)
        temp = data["T"]
        hum = data["H"]
        temp_mqtt = float(temp)
        hum_mqtt = float(hum)
        mqtt_client.send(temp_mqtt,hum_mqtt, "temp3", "hum3")
        print("TEMPERATURE: {}".format(temp))
        print("HUMIDITY: {}".format(hum))
        endTime = int(time() * 1000) - startTime
        print("Time for Observe: ", endTime)
        #rows = [[endTime]]
        #filename = "room3.csv"
        
        #with open(filename, 'a') as csvfile: 
            # creating a csv writer object 
            #csvwriter = csv.writer(csvfile)          
            # writing the data rows 
            #csvwriter.writerows(rows)
            
        startTime = int(time() * 1000)

        url = 'coap://192.168.43.67/raspi/power'

        if temp > setTemp+2:
            level = b'high'
            context = await Context.create_client_context()
            await asyncio.sleep(2) # sleep 2 sec before send request
            payload = level
            request = Message(code=PUT, payload=payload, uri=url)
            response = await context.request(request).response

            print('Result: %s\n%r'%(response.code, response.payload))
            
        
        if temp > setTemp and temp <= setTemp+1:
            level = b'medium'
            context = await Context.create_client_context()
            await asyncio.sleep(2)# sleep 2 sec before send request
            payload = level
            request = Message(code=PUT, payload=payload, uri=url)
            response = await context.request(request).response

            print('Result: %s\n%r'%(response.code, response.payload))
            
            if hum >setHum+2:
                level = b'high'
                context = await Context.create_client_context()
                await asyncio.sleep(2) # sleep 2 sec before send request
                payload = level
                request = Message(code=PUT, payload=payload, uri=url)
                response = await context.request(request).response

                print('Result: %s\n%r'%(response.code, response.payload))
     

        if temp <= setTemp:
            level = b'low'
            context = await Context.create_client_context()
            await asyncio.sleep(2)# sleep 2 sec before send request
            payload = level
            request = Message(code=PUT, payload=payload, uri=url)
            response = await context.request(request).response

            print('Result: %s\n%r'%(response.code, response.payload))

            if hum >setHum+2:
                level = b'high'
                context = await Context.create_client_context()
                await asyncio.sleep(2) # sleep 2 sec before send request
                payload = level
                request = Message(code=PUT, payload=payload, uri=url)
                response = await context.request(request).response

                print('Result: %s\n%r'%(response.code, response.payload))

            if hum > setHum and hum <=setHum+2:
                level = b'medium'
                context = await Context.create_client_context()
                await asyncio.sleep(2)# sleep 2 sec before send request
                payload = level
                request = Message(code=PUT, payload=payload, uri=url)
                response = await context.request(request).response

                print('Result: %s\n%r'%(response.code, response.payload))

            if hum <= setHum:
                level = b'low'
                context = await Context.create_client_context()
                await asyncio.sleep(2)# sleep 2 sec before send request
                payload = level
                request = Message(code=PUT, payload=payload, uri=url)
                response = await context.request(request).response

                print('Result: %s\n%r'%(response.code, response.payload))

            

        #pr.observation.cancel()
        #break
    print("Loop ended, sticking around")
    await asyncio.sleep(5)

if __name__ == "__main__":
    setTemp = float(input("Set Your Temperature: "))
    setHum = float(input("Set Your Humidity: "))
    asyncio.get_event_loop().run_until_complete(main())
