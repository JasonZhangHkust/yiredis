import socket
import threading
import time
import logging
import select
import ConfigParser
import pickle
f2 = open("redis.txt", "rb")
load_list = pickle.load(f2)
f2.close()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class simpleserver(object):
    redis_demo = load_list
    cf = ConfigParser.ConfigParser()
    cf.read("auth.conf")
    auth = {}
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def __del__(self):
        print "Deleting"
        f1 = open("redis.txt", "wb")
        pickle.dump(self.redis_demo, f1)
        f1.close()

    @staticmethod
    def parse_message(data):
        command = None
        key = None
        value = None
        try:
            command = data.strip().split(':')[0]
            if command.upper() == "GET":
                command, key = map(str.strip, data.strip().split(':'))
            elif command.upper() in ["AUTH", "URL", "SET"]:
                print data
                command, key, value = map(str.strip, data.strip().split(':'))
                print key
        except Exception as e:
            print
        return command, key, value

    def handle_set(self, key, value):
        try:
            self.redis_demo[key] = value
        except:
            raise Exception('Wrong Key')

    def handle_get(self, key):
        try:
            value = self.redis_demo.get(key)
            if not value:
                value = "None"
        except:
            raise Exception("No such Error")
        return value

    #@staticmethod
    #def handle_url(key, value):

    def save_redis(self):
        f1 = open("redis.txt", "wb")
        pickle.dump(self.redis_demo,f1)
        f1.close()

    def handle_auth(self, usr_name, password):
        try:
            if password == self.cf.get("users", usr_name):
                return True
            else:
                return False
        except:
            return False

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            print address
            client.settimeout(50)
            threading.Thread(target=self.listen_to_client, args=(client, address)).start()

    def listen_to_client(self, client, address):
        size = 1024
        data = None
        usr_name = None
        try:
            while True:
                ready = select.select([client], [], [], 500
                                      )
                print ready[0]
                if ready[0]:
                    data = client.recv(size)
                    if data == 'exit':
                        if data == 'exit':
                            if usr_name:
                                self.auth[usr_name] = False
                        print "No data Close"
                        break
                    elif data:
                        command, key, value = self.parse_message(data)
                        if command == "GET":
                            value = self.handle_get(key)
                            client.send(value)
                        elif command == "SET":
                            self.handle_set(key, value)
                            client.send("ok")
                        elif command == "AUTH":
                            passed = self.handle_auth(key, value)
                            print key
                            if passed:
                                usr_name = key
                                self.auth[key] = True
                                client.send('0')
                            else:
                                self.auth[key] = False
                                client.send('-1')
                            print("demo")
                        elif command == "URL":
                            if self.auth.get(usr_name):
                                client.send('URL~~')
                else:
                    break
                time.sleep(1)
        except socket.error:
            print "Client disconnect"
            return False
        except Exception as e:
            print e
        print("Close")
        client.close()
        return False


def exit_handler():
    print 'My application is ending!'


if __name__ == "__main__":
    host = "localhost"
    port = 5678
    my_server = simpleserver(host, port)
    try:
        my_server.listen()
    except KeyboardInterrupt:
        logger.debug("saving redis")
        my_server.save_redis()
