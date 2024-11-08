import socket
import threading
import json
from typing import Callable, Dict


'''
EXAMPLE USAGE
start connection
user1 = Network("user1", 4000)
user1.start()
user1.connect("user2", 5000)
user1.registerCallback("move", moveHandler)
user1.registerCallback("chat", chatHandler)
user1.registerCallback("network", networkHandler) - network handler could be merged with the chat handler

send messages
user1.sendMove(moveData)
user1.sendChat(chat)

close connection
user1.stop()
'''
class Network:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peerAddress: tuple = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((host, port))
        self.running = False
        self.callbacks: Dict[str, Callable] = {}

    # unsure if this will be necessary depending on main game loop implementation. will remove once tested
    def start(self):
        self.running = True
        self.listenThread = threading.Thread(target=self.listen)
        self.listenThread.daemon = True
        self.listenThread.start()

    def stop(self):
        self.running = False
        self.socket.close()

    def connect(self, peerHost, peerPort):
        self.peerAddress = (peerHost, peerPort)
        # send message to confirm connection
        self.sendMessage({"type": "network", "message": "Connected successfully"})

    def sendMessage(self, message):
        if not self.peerAddress:
            raise ConnectionError("Peer not connected")
        try:
            self.socket.sendto(json.dumps(message).encode(), self.peerAddress)
        except Exception as e:
            print(f"Failed to send message: {e}")

    def registerCallback(self, messageType, callback):
        self.callbacks[messageType] = callback

    def listen(self):
        # messages should be expected as a dict in form {"type": messageType, "message": message}
        while self.running:
            try:
                # probably a high buffer size can be fine-tuned later
                data, addr = self.socket.recvfrom(4096)
                if not self.peerAddress:
                    self.peerAddress = addr
                message = json.loads(data.decode())
                messageType = message.get("type", "")
                if messageType in self.callbacks:
                    self.callbacks[messageType](message)
            except json.JSONDecodeError:
                print("Received bad JSON data")
            except Exception as e:
                if self.running:
                    print(f"Listen loop threading failed: {e}")

    def sendMove(self, move):
        self.sendMessage({"type": "move", "message": move})

    def sendChat(self, chat):
        self.sendMessage({"type": "chat", "message": chat})

    # add any other communication type methods if necessary
