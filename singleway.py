import socket, sys
import random
import asyncio


class ChatApp (object):

    def __init__ (self, port = 12345):
        self.socket = socket
        self.hostname = self.socket.gethostname()
        self.socket_o = self.socket.socket()
        self.port = port
        self.socket_o.bind((self.hostname, self.port))
        print(f"Host name is {self.hostname} and port is {self.port}")

    
    def connect (self, hostname, port):
        try:
            self.socket_o.connect((hostname,port))
            print(f"Connected to {hostname} at port {port}")
        except:
            print(f"Hostname and port combination does not exit")

    

if __name__ == "__main__":
    app = ChatApp(port = random.randint(1050,1200))
    runtime = True
    while runtime:
        data = input("Input hostname and port of user to connect to, both separated by a space, or if you are awaiting a connection, type L, else if you wanna quit, type Q: \n")
        args = data.strip().split()
        if len(args) == 2:
            app.connect(args[0], int(args[1]))
            address = app.socket_o.getpeername()
            inner_runtime = True
            while inner_runtime:
                msg = input("Message: ")
                app.socket_o.sendto(msg.encode("ascii"),address)
        else:
            if args[0].lower() == "l":
                app.socket_o.listen(100)
                check_runtime = True
                while check_runtime:
                    recapp, address = app.socket_o.accept()
                    if address:
                        check_runtime = False
                print("Connected to {address}")
                inner_runtime = True
                while inner_runtime:
                    rec = recapp.recv(4096)
                    print(rec.decode("utf-8") if rec else "")

            elif args[0].lower() == "q":
                print("Thank you for using ChatBot!")
                sys.exit()
            else:
                print("Error: wrong input, please try again.")
         
        
