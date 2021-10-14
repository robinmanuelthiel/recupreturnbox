# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import asyncio
import datetime
import json
import os
import sys
import threading
import time

from azure.iot.device.aio import IoTHubModuleClient
from six.moves import input

from predict import initialize, predict_image

# FOR DEBUGGING
try:
    import ptvsd

    ptvsd.enable_attach(("0.0.0.0", 5679))

except ImportError:
    pass


async def main():
    ptvsd.break_into_debugger()

    try:
        if not sys.version >= "3.5.3":
            raise Exception(
                "The sample requires python 3.5.3+. Current version of Python: %s"
                % sys.version
            )
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

                try:
                    # I don't know how message.data looks like. This might come handy later:
                    # imageData = io.BytesIO(request.get_data())

                    print("the data in the message received on input1 was ")
                    print(f"input_message.data: {input_message}")
                    print(f"type(input_message.data): {type(input_message.data)}")

                    # Try predicting something
                    results = predict_image(input_message.data)
                    print(results)
                except Exception as e:
                    print(f"Inference failed with exception ({type(e)}): '{str(e)}'")

                print("custom properties are")
                print(input_message.custom_properties)
                print("forwarding mesage to output1")

                result = [
                    {
                        "tagName": "recup",
                        "probability": 0.95,
                        "tagId": "",
                        "boundingBox": None,
                    },
                    {
                        "tagName": "other",
                        "probability": 0.05,
                        "tagId": "",
                        "boundingBox": None,
                    },
                ]

                response = {
                    "id": "",
                    "project": "",
                    "iteration": "",
                    "created": datetime.utcnow().isoformat(),
                    "predictions": result,
                }

                response_string = json.dump(response, indent=2)

                await module_client.send_message_to_output(
                    input_message, response_string
                )

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

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

    # If using Python 3.7 or above, you can use following code instead:
    # asyncio.run(main())
