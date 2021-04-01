import clientPUT
import clientGET
import asyncio

async def getClient(url):
    await clientGET.main(url)

if __name__ == "__main__":
    while True:
        
        method = input("GET or PUT? :")

        if method == "GET":

            pi = input("which pi? : 1, 2, 3")

            if pi == 1 or pi == "1":
                ip = "192.168.43.10"
                typeOfData = input("GET temp or hum? :")

                if typeOfData == "temp":
                    url = "coap://{}/raspi/{}".format(ip, typeOfData)
                    
                    asyncio.run(getClient(url))
                    break


                if typeOfData == "hum":
                    url = "coap://{}/raspi/{}".format(ip, typeOfData)
                    asyncio.run(getClient(url))
                    break

            else:
                print("input error... try again.")



        if method =="PUT":

            pi = input("which pi? : 1, 2, 3")
            if pi == 1 or pi == "1":
                ip = "192.168.43.10"
                level = input("PUT what power level? low, meduim, high:")

                if level == "low":
                    level = b"%b" %level.encode('utf8')
                    url = "coap://{}/raspi/power".format(ip)
                    asyncio.run(clientPUT.main(url, level))
                    break

                if level == "medium":
                    level = b"%b" %level.encode('utf8')
                    url = "coap://{}/raspi/power".format(ip, level)
                    asyncio.run(clientPUT.main(url, level))
                    break
                
                if level == "high":
                    level = b"%b" %level.encode('utf8')
                    url = "coap://{}/raspi/power".format(ip, level)
                    asyncio.run(clientPUT.main(url, level))
                    break

                else:
                    print("input error... try again.")

            else:
                print("input error... try again.")
                



        else:
            print("input error... try again.")
