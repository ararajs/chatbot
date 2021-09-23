import socket
import random
from netifaces import interfaces, ifaddresses, AF_INET
from multiprocessing import Process


def host():
    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
        addresses = "".join(addresses)
        if "127.0" not in addresses and "No IP addr" != addresses:
            return addresses
        
host = host()

class ChatBot (object):
    def __init__ (self, host=host, send_port = 9123, receive_port = 9124):
        self.host = host
        self.send_sock = socket.socket()
        self.rec_sock = socket.socket()
        self.send_port = send_port
        self.rec_port = receive_port
        self.send_sock.bind((self.host, self.send_port))
        self.rec_sock.bind((self.host, self.rec_port))
        print(f"Initiated two sockets at {host}. Send port is {send_port} and Receive Port is {receive_port}")

    
    def connect (self, rechost, recport):
        try:
            self.send_sock.connect((rechost, recport))
            print("Succesfully connected to {rechost} at port {recport}}")
        except:
            print("Error: Incorrect hostname/port")

def setup(ChatBot: ChatBot):
    setup_input = input("For setup, do you want to act as sender (S) or receiver (R)?: ")

    if setup_input.lower() ==  "s":
        args = input("Enter host name and port sepearted by a space: ").strip().split()
        ChatBot.send_sock.connect((args[0], int(args[1])))
        address = ChatBot.send_sock.getpeername()
        ChatBot.rec_sock.listen(100)
        for _ in range(2):
            msg = input("Input: ")
            ChatBot.send_sock.sendto(f"{msg}".encode("ascii"), address)
        check_runtime = True
        while check_runtime:
            send_sock, send_address = ChatBot.rec_sock.accept()
            if send_address:
                check_runtime = False
        return send_sock, address

    elif setup_input.lower() == "r":
        ChatBot.rec_sock.listen(100)
        check_runtime = True
        while check_runtime:
            send_sock, send_address = ChatBot.rec_sock.accept()
            if send_address:
                print("Connected to {send_address} at {send_address}")
                check_runtime = False

        data_runtime = True
        output_array = []
        while data_runtime:
            rec_msg = send_sock.recv(4096)
            if rec_msg:
                print(rec_msg.decode("utf-8"))
                output_array.append(rec_msg.decode("utf-8"))
            if len(output_array) == 2:
                data_runtime = False
        ChatBot.send_sock.connect((output_array[0], int(output_array[1])))
        address = ChatBot.send_sock.getpeername()
        return send_sock, address

def IncomingMessage(rec_sock):
    msg = rec_sock.recv(4096)
    if msg:
        print(msg.decode("utf-8"))
        return
    else:
        return


def OutgoingMessage(chatbot, address):
    msg = input("Message: ")
    chatbot.send_sock.sendto(msg.encode("ascii"), address)
    return



if __name__ == "__main__":
    chatbot = ChatBot(host = host, send_port=random.randint(1025,10000), receive_port=random.randint(1025,10000))
    rec_sock, rec_addr = setup(chatbot)
    print("Connection complete, you may talk now.")

    upload = Process(target = OutgoingMessage(chatbot, rec_addr))
    download = Process(target = IncomingMessage(rec_sock))
    download.start()
    upload.start()
    download.join()
    upload.join()
        #OutgoingMessage(chatbot, rec_addr)
        #IncomingMessage(rec_sock)

        
        

    


