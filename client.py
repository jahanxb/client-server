import pathlib
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


def send_data(conn, payload, data_id=0):
    """
                @brief: send payload along with data size and data identifier to the connection
                @args[in]:
                    conn: socket object for connection to which data is supposed to be sent
                    payload: payload to be sent
                    data_id: data identifier
                """
    if payload is 'bye':
        print('Payload is completed, Connection Closed')
    # serialize payload
    else:

        serialized_payload = pickle.dumps(payload)
        # send data size, data identifier and payload

        conn.sendall(struct.pack('>I', len(serialized_payload)))
        conn.sendall(struct.pack('>I', data_id))
        conn.sendall(serialized_payload)
        # conn.sendall(base_name)


def receive_data(conn):
    '''
                @brief: receive data from the connection assuming that
                    first 4 bytes represents data size,
                    next 4 bytes represents data identifier and
                    successive bytes of the size 'data size'is payload
                @args[in]:
                    conn: socket object for conection from which data is supposed to be received
                '''
    # receive first 4 bytes of data as data size of payload
    data_size = struct.unpack('>I', conn.recv(4))[0]
    # receive next 4 bytes of data as data identifier
    data_id = struct.unpack('>I', conn.recv(4))[0]
    # receive payload till received payload size is equal to data_size received
    received_payload = b""
    reamining_payload_size = data_size
    while reamining_payload_size != 0:
        received_payload += conn.recv(reamining_payload_size)
        reamining_payload_size = data_size - len(received_payload)
    payload = pickle.loads(received_payload)
    return (data_id, payload)


# define category in which you would like to define data
data_identifiers = {'info': 0, 'data': 1, 'filedata': 2, 'filename': 3}
# key to be trusted by server
key_message = 'auth_code'
# a sample dictionary data
data = {'data_number': 0,
        'message': 'A new message has been arrived from client'}


def client_main(folder_name, concurrency):
    with ThreadPoolExecutor(max_workers=int(concurrency)) as executor:
        started = time.time()
        executor.map(main(folder_name, concurrency))
        time.sleep(0.2)

    elapsed = time.time()
    print(f'Time taken MultiProcess :{elapsed - started} On concurrency Level: {concurrency}')
    return dict(time_taken=elapsed - started, concurrency_rate=concurrency)


def main(folder_name, concurrency):
    # create client socket object and connect it to server
    # time.sleep(0.2)
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(('127.0.0.1', 5050))
    send_data(conn, key_message)
    first_payload = receive_data(conn)[1]
    if first_payload == 'You are not authorized':
        print('[ERROR]: Access denied')
    else:
        # send a dictionary data and file data in loop till keyboard interrupt is received
        while True:
            try:
                total_elapsed = list()
                arr = os.listdir(folder_name)
                for filename in arr:
                    # send dict
                    data['data_number'] += 1
                    base_name = os.path.basename(filename)
                    data['filename'] = base_name
                    send_data(conn, data, data_identifiers['data'])

                    print(receive_data(conn)[1])

                    sha256 = Util.checksum(f'{folder_name}/{filename}')
                    # `todo To Save checksum value and filename in redis
                    # Util.redis_new_entry(base_name, sha256)

                    with open(f'{folder_name}/{filename}', 'rb') as file:
                        bytes_read = file.read()
                        if not bytes_read:
                            break
                        else:
                            data_to_send = dict(filedata=bytes_read, filename=filename, sha256=sha256)
                            # print(data_to_send)
                        file.close()
                    with ThreadPoolExecutor(max_workers=int(concurrency)) as executor:
                        started = time.time()

                        executor.map(send_data(conn, data_to_send, data_identifiers['filedata']))
                        time.sleep(0.2)
                        elapsed = time.time()
                        total_elapsed.append(elapsed - started)
                        print(
                            f'Time taken MultiProcess :{elapsed - started} On concurrency Level: {concurrency}')
                    print(f'Total Time Taken: {sum(total_elapsed)} at Concurrency Level: {concurrency}')

            except Exception as e:
                if e == KeyboardInterrupt:
                    # once keyboard interrupt is received, send signal to server for closing connection
                    print(receive_data(conn)[1])
                    print('\n[INFO]: Keyboard Interrupt received')
                    break
                elif e == ConnectionAbortedError:
                    print("File Upload Completed")
                    pass
                else:
                    print('Exception Thrown:', e)
                    pass

            send_data(conn, 'bye')
            print('[Info] Connection is Closed from Client side')
            break

            # print(receive_data(conn)[1])

        # close connection
    conn.close()
    print('[INFO]: Connection closed')


if __name__ == '__main__':
    # print(os.path.abspath(sys.argv[1]))
    #
    main(os.path.abspath(sys.argv[1]), sys.argv[2])

    '''
    Testing code on different concurrency levels and generating graph
    '''
    # import pandas as pd
    # from matplotlib import pyplot as plt
    #
    # list_data = list()
    # c1 = client_main('dataset', 1)
    # c2 = client_main('dataset', 2)
    # c3 = client_main('dataset', 4)
    # c4 = client_main('dataset', 8)
    # list_data.append(c1)
    # list_data.append(c2)
    # list_data.append(c3)
    # list_data.append(c4)
    # df = pd.DataFrame(list_data)
    # # Using scatter plot
    # plt.scatter(df['concurrency_rate'], df['time_taken'])
    # plt.title('Concurrency throughput')
    # plt.ylabel('Time Taken in Seconds')
    # plt.xlabel('Concurrency rate')
    # plt.show()
