import socket
import pickle
import time

import cv2
import struct
import os
from util import Util
import sys, timeit
import threading
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import process, Pool


def main(folder):
    host = '127.0.0.1'
    port = 5050
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096  # send 4096 bytes each time step
    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks.connect((host, port))
    try:

        files = os.listdir(folder)
        for file in files:
            filename = folder + '/' + file

            # get the file size
            filesize = os.path.getsize(filename)
            socks.send(f"{filename}{SEPARATOR}{filesize}".encode())
            with open(filename, "rb") as f:
                while True:
                    # read the bytes from the file
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        # file transmitting is done
                        break
                    # we use sendall to assure transimission in
                    # busy networks
                    print(f'Sending file {filename} to Server .....')
                    socks.sendall(bytes_read)
                    print(bytes_read.hex())
                    f.close()
                    break
                    # update the progress bar
                    # progress.update(len(bytes_read))
        socks.close()

    except Exception as e:
        print(f'[WARN] Exception Thrown at Client Level {e}')


if __name__ == '__main__':
    main('dataset')
