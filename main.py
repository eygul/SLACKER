# THIS IS THE SOURCE CODE FOR SLACKER BY EREN GUL.
# SLACKER IS AN OPEN SOURCE SMART COFFEE POT PROJECT.
# IT UTILIZES PYTHON FOR CREATION OF THE CHATBOT FOR COMMUNICATION WITH THE USER AND THE COFFEE POT.
# SLACKER IS A COFFEE POT MODERNIZATION SYSTEM.
import serial
import asyncio
import aiohttp
import slack_sdk
import os
from dotenv import load_dotenv
from slack_sdk.errors import SlackApiError
from slack_sdk.rtm import RTMClient
import RPi.GPIO as GPIO




def get_client():
    env_path = "../.env"
    load_dotenv(env_path)
    client = slack_sdk.WebClient(os.environ['SLACK_BOT_TOKEN'])
    rtm_client = RTMClient(token=os.environ['SLACK_BOT_TOKEN'])
    return client, rtm_client


def post_msg(client):
    client.chat_postMessage(channel="experimental-chatbot", text=f"Hello dear Sir, your coffee is on the way!")
    GPIO.setmode(GPIO.BCM)  # GPIO Numbers instead of board numbers


def post_msg_not(client):
    client.chat_postMessage(channel="experimental-chatbot", text=f"Okay Sir, no coffee!")


async def ret_msg(client):
    try:
        response = await asyncio.to_thread(client.conversations_history, channel="C052DQD3N9G", limit=1)
        message = response["messages"][0]["text"]
        print(message)
        return message
    except SlackApiError as e:
        print("Error retrieving messages: {}".format(e))


async def main():
    a = get_client()
    b = await ret_msg(a[0])
    if "don't" in b or "not" in b:
        post_msg_not(a[0])
    if "make" in b and "coffee" in b and not "don't" in b and not "not" in b:
        post_msg(a[0])


if __name__ == "__main__":
    asyncio.run(main())
