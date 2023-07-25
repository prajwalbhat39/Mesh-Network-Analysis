import os
# import socket
# import threading

myIp = input("Configure your IP address: ")

os.system("systemctl stop NetworkManager")
os.system("sudo ip link set wlo1 down")
os.system("sudo iwconfig wlo1 mode ad-hoc")
os.system("sudo iwconfig wlo1 channel 1")
os.system("sudo iwconfig wlo1 essid Kavach")
os.system("sudo iwconfig wlo1 key 1234567890")
os.system("sudo iwconfig wlo1 ap 12:3E:30:39:BE:A1")
os.system("sudo ip link set wlo1 up")
os.system(f"sudo ip addr add 168.254.{myIp}/16 dev wlo1")

# # Set the IP address and port number of the remote node to chat with
# REMOTE_PORT = 12345

# # Create a UDP socket for sending and receiving messages
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# def receive_messages():
#     # Continuously receive messages from the remote node
#     while True:
#         message, address = sock.recvfrom(1024)
#         print(f"From {address[0]}")
#         print(f"Received message: {message.decode('utf-8')}\n")

# def send_messages():
#     # Continuously send messages to the remote node
#     while True:
#         REMOTE_HOST = input("Reciever IP")
#         message = input("Enter a message: ")
#         sock.sendto(message.encode("utf-8"), (f"192.168.{REMOTE_HOST}", REMOTE_PORT))

# # Start a thread to receive messages
# threading.Thread(target=receive_messages, daemon=True).start()

# # Start a thread to send messages
# threading.Thread(target=send_messages, daemon=False).start()
