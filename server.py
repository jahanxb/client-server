import socket
import threading
import time
import pickle
import cv2
import struct
from util import Util
import sys


def send_data(conn, payload, data_id=0):
    '''
    @brief: send payload along with data size and data identifier to the connection
    @args[in]:
        conn: socket object for connection to which data is supposed to be sent
        payload: payload to be sent
        data_id: data identifier
    '''
    # serialize payload

    serialized_payload = pickle.dumps(payload)
    # send data size, data identifier and payload
    conn.sendall(struct.pack('>I', len(serialized_payload)))
    conn.sendall(struct.pack('>I', data_id))
    conn.sendall(serialized_payload)


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


def do_something(conn_name, data):
    '''
    @beief: a sample function to do something with received data
    @args[in]:
        conn_name: connection name from where dat is received
        data: received data
    @args[out]:
        a string response
    '''
    print('Data number {} received from client {}'.format(
        data['data_number'], conn_name))
    temp = data['data_number']
    time.sleep(0.1)
    # return 'Data number {} received on server'.format(data['data_number'])
    return 'File received on server'


def handle_client(conn, conn_name):
    '''
    @brief: handle the connection from client at seperate thread
    @args[in]:
        conn: socket object of connection
        con_name: name of the connection
    '''
    while True:
        try:

            data_id, payload = receive_data(conn)
            # if data identifier is FileData then save the File
            if data_id == data_identifiers['filedata']:
                print('---Recieved DataFile too ---')

                filename = f'{payload.get("filename")}'

                received = payload.get('filedata')
                #print(received)
                file = open(f'received_data/{filename}','wb')
                file.write(received)
                print("filename on Server: ")
                print("filename from client: ", payload.get('filename'))

                # `todo verify client checksum
                server_sha = Util.checksum(f'received_data/{filename}')
                verified_checksum = Util.compare_checksums(payload.get('sha256'),server_sha)
                print('Checking Checksum .....')
                if verified_checksum:
                    print(server_sha)
                    print(payload.get('sha256'))
                    print("checksum is verified !")
                else:
                    print("Checksum not verified")
                    with open('errors.log', 'a+') as error:
                        error.write(f'{filename} checksum Server: {server_sha} checksum Client: {payload.get("sha256")}')
                    error.close()
            # otherwise send the data to do something
            elif data_id == data_identifiers['data']:
                response = do_something(conn_name, payload)

                send_data(conn, response)

            else:
                # if data is 'bye' then break the loop and client connection will be closed
                if payload == 'bye':
                    print(
                        '[INFO]: {} requested to close the connection'.format(conn_name))
                    print('[INFO]: Closing connection with {}'.format(conn_name))
                    send_data(conn, 'You are disconnected from server now')
                    break
                else:
                    print(payload)
        except Exception as e:
            pass
            # print('[WARNING]: There was some issue with connection Exception', e)
    conn.close()


# define identifiers for data which could be used to take certain action for data
data_identifiers = {'info': 0, 'data': 1, 'filedata': 2,
                    'filename': 3}
# key to trust a connection
key_message = 'auth_code'


def main():
    # create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 5050
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(5)
    print('[INFO]: Server Started')

    while True:
        try:
            # accept client connection
            # if first message from client match the defined message
            # then handle it at seperate thread
            # otherwise close the connection
            conn, (address, port) = server_socket.accept()
            conn_name = '{}|{}'.format(address, port)
            print("[INFO]: Accepted the connection from {}".format(conn_name))
            first_payload = receive_data(conn)[1]
            if first_payload == key_message:
                print('Connection could be trusted, rejecting communication')
                send_data(conn, 'Connection accepted')
                threading.Thread(target=handle_client,
                                 args=(conn, conn_name)).start()
            else:
                print('[WARNING]: Accepted connection is an unknown client, \
                      closing the connection')
                send_data(conn, 'You are not authorized')
                conn.close()
        # break the while loop when keyboard intterupt is received and server will be closed
        except Exception as e:
            if e == KeyboardInterrupt:
                print('\n[INFO]: Keyboard Interrupt Received')
                break
            else:
                pass
    server_socket.close()
    print('[INFO]: Server Closed')


if __name__ == '__main__':
    main()
