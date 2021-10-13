# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import asyncio
import os
import sys
import threading
import time

import ptvsd
from azure.iot.device.aio import IoTHubModuleClient
from PIL import Image
from six.moves import input

from predict import initialize, predict_image

# FOR DEBUGGING
ptvsd.enable_attach(("0.0.0.0", 5678))


async def main():
    try:
        print("IoT Hub Client for Python")

        # The client object is used to interact with your Azure IoT hub.
        module_client = IoTHubModuleClient.create_from_edge_environment()

        # connect the client.
        await module_client.connect()

        # define behavior for receiving an input message on input1
        async def input1_listener(module_client):
            while True:
                input_message = await module_client.receive_message_on_input(
                    "input1"
                )  # blocking call
                print("the data in the message received on input1 was ")
                print(input_message.data)
                print("custom properties are")
                print(input_message.custom_properties)
                print("forwarding mesage to output1")

                # TODO: FIGURE OUT HOW TO CONVERT message.data to imageData
                # imageData = None
                # if "imageData" in request.files:
                #     imageData = request.files["imageData"]
                # elif "imageData" in request.form:
                #     imageData = request.form["imageData"]
                # else:
                #     imageData = io.BytesIO(request.get_data())

                img = Image.open(input_message.data)
                results = predict_image(img)

                await module_client.send_message_to_output(input_message, results)

        # define behavior for halting the application
        def stdin_listener():
            while True:
                try:
                    selection = input("Press Q to quit\n")
                    if selection == "Q" or selection == "q":
                        print("Quitting...")
                        break
                except:
                    time.sleep(10)

        # Schedule task for C2D Listener
        listeners = asyncio.gather(input1_listener(module_client))

        print("The sample is now waiting for messages. ")

        # Run the stdin listener in the event loop
        loop = asyncio.get_event_loop()
        user_finished = loop.run_in_executor(None, stdin_listener)

        # Wait for user to indicate they are done listening for messages
        await user_finished

        # Cancel listening
        listeners.cancel()

        # Finally, disconnect
        await module_client.disconnect()

    except Exception as e:
        print("Unexpected error %s " % e)
        raise


if __name__ == "__main__":
    initialize()

    asyncio.run(main())
