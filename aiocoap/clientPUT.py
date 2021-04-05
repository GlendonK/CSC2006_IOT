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

"""
@params b""
"""
async def main(url, level):
    """Perform a single PUT request to localhost on the default port, URI
    "/other/block". The request is sent 2 seconds after initialization.

    The payload is bigger than 1kB, and thus sent as several blocks."""

    context = await Context.create_client_context()

    await asyncio.sleep(2)

    payload = level
    startTime = int(time() * 1000)
    request = Message(code=PUT, payload=payload, uri=url)

    response = await context.request(request).response

    print('Result: %s\n%r'%(response.code, response.payload))
    endTime = int(time() * 1000) - startTime
    print("Time for PUT: ", endTime)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
