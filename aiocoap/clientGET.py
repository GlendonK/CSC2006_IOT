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
from time import time

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def main(url):
    protocol = await Context.create_client_context()


    startTime = int(time() * 1000)
    request = Message(code=GET, uri=url)

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))
        endTime = int(time() * 1000) - startTime
        print("Time for GET: ", endTime)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
