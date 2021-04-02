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

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def put(url, level):
    await asyncio.run(clientPUT.main(url, level))

async def main():
    protocol = await Context.create_client_context()

    request = Message(code=GET, uri='coap://192.168.43.10/raspi/obs', observe=0)

    pr = protocol.request(request)

    r = await pr.response
    print("First response: %s\n%r"%(r, r.payload))

    async for r in pr.observation:
        #print("Next result: %s\n%r"%(r, r.payload))
        data = json.loads(r.payload)
        temp = data["T"]
        hum = data["H"]
        print("TEMPERATURE: {}".format(temp))
        print("HUMIDITY: {}".format(hum))

        url = 'coap://192.168.43.10/raspi/power'

        if temp > 42:
            level = b'high'
            context = await Context.create_client_context()
            await asyncio.sleep(2) # sleep 2 sec before send request
            payload = level
            request = Message(code=PUT, payload=payload, uri=url)
            response = await context.request(request).response

            print('Result: %s\n%r'%(response.code, response.payload))
            
        
        if temp > 41 and temp <= 42:
            level = b'medium'
            context = await Context.create_client_context()
            await asyncio.sleep(2)# sleep 2 sec before send request
            payload = level
            request = Message(code=PUT, payload=payload, uri=url)
            response = await context.request(request).response

            print('Result: %s\n%r'%(response.code, response.payload))
            
            if hum >54:
                level = b'high'
                context = await Context.create_client_context()
                await asyncio.sleep(2) # sleep 2 sec before send request
                payload = level
                request = Message(code=PUT, payload=payload, uri=url)
                response = await context.request(request).response

                print('Result: %s\n%r'%(response.code, response.payload))
     

        if temp <= 41:
            level = b'low'
            context = await Context.create_client_context()
            await asyncio.sleep(2)# sleep 2 sec before send request
            payload = level
            request = Message(code=PUT, payload=payload, uri=url)
            response = await context.request(request).response

            print('Result: %s\n%r'%(response.code, response.payload))

            if hum >54:
                level = b'high'
                context = await Context.create_client_context()
                await asyncio.sleep(2) # sleep 2 sec before send request
                payload = level
                request = Message(code=PUT, payload=payload, uri=url)
                response = await context.request(request).response

                print('Result: %s\n%r'%(response.code, response.payload))

            if hum > 52 and hum <=54:
                level = b'medium'
                context = await Context.create_client_context()
                await asyncio.sleep(2)# sleep 2 sec before send request
                payload = level
                request = Message(code=PUT, payload=payload, uri=url)
                response = await context.request(request).response

                print('Result: %s\n%r'%(response.code, response.payload))

            if hum <= 52:
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
    asyncio.get_event_loop().run_until_complete(main())
