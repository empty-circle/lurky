import requests
import json
from bs4 import BeautifulSoup
from websocket import WebSocketApp

# Replace with the URL of the website you want to scrape
url = "https://www.example.com"

def find_chatrooms(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        chatroom_urls = [a['href'] for a in soup.find_all('a', href=True) if 'ws' in a['href']]
        return chatroom_urls
    else:
        print("Error: Unable to fetch the webpage.")
        return []


def on_open(ws):
    print("Connected to the chat room.")


def on_message(ws, message):
    data = json.loads(message)
    print(f"Received a message: {data}")


def on_error(ws, error):
    print(f"Error: {error}")


def on_close(ws):
    print("Disconnected from the chat room.")


def start_chat_monitor(chatroom_url):
    ws = WebSocketApp(
        chatroom_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever()

def main():
    url = input("Please enter the website URL to check for chat rooms: ")
    chatrooms = find_chatrooms(url)

    if chatrooms:
        for chatroom_url in chatrooms:
            print(f"Monitoring chat room: {chatroom_url}")
            start_chat_monitor(chatroom_url)
    else:
        print("No chat rooms found.")

if __name__ == "__main__":
    main()
