import socket
import threading
import time
import pickle
import cv2
import struct
from util import Util
import sys, os


def receive_file_from_client():
    pass


def main():
    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 5050
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    socks.bind((host, port))
    socks.listen(5)
    print(f'[INFO] SOCKET Listening at Server')
    try:
        while True:
            connection, (address, port) = socks.accept()
            # `todo connection is client_socket
            connection_name = f'{address}|{port}'
            print(f'[INFO] Accepted Connection from {connection_name}')
            received = connection.recv(BUFFER_SIZE).decode()
            filename, filesize = received.split(SEPARATOR)
            # remove absolute path if there is
            filename = os.path.basename(filename)
            print(filename)
            # convert to integer
            filesize = int(filesize)
            with open('received_data/' + filename, "wb") as f:
                while True:
                    # read 1024 bytes from the socket (receive)
                    bytes_read = connection.recv(BUFFER_SIZE)
                    if not bytes_read:
                        # nothing is received
                        # file transmitting is done
                        break
                    # write to the file the bytes we just received
                    f.write(bytes_read)
                    # update the progress bar
                    # progress.update(len(bytes_read))
                    # close the client socket
                    connection.close()


            # close the server socket
    # socks.close()

    except Exception as e:
        print(f'[WARN] Exception Thrown at Server Level {e}')

    socks.close()


if __name__ == '__main__':
    main()
