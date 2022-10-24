import os
import socket
import threading
import time
from dotenv import load_dotenv

from tables import device_table, location_table, oxygen_table, ph_table, conduct_table, chlorophyll_table
from data_saver import InsertData

insert_data = InsertData(device_table, location_table,
                         oxygen_table, ph_table, conduct_table, chlorophyll_table)


def binder(client_socket, addr):

    try:
        while True:
            receive_data = client_socket.recv(73)
            if not receive_data:
                print(addr, "to quit!")
                print("Waiting for next data...")
                break

            msg = receive_data.hex()
            print("Data received.", time.strftime(
                '%Y-%m-%d'), time.strftime('%H:%M:%S'))

            if msg:
                print('Received from', addr, msg)
                lat = int(msg[10:18], 16)/1000000
                lon = int(msg[18:26], 16)/1000000

                if lon > 1 and lat > 1:
                    insert_data.device_insert(msg)
                    insert_data.location_insert(msg)
                    insert_data.oxygen_insert(msg)
                    insert_data.ph_insert(msg)
                    insert_data.conduct_insert(msg)
                    insert_data.chlorophyll_insert(msg)
                else:
                    print('Wrong GPS value', lat, lon)
                    pass

                length = len(receive_data)
                client_socket.sendall(length.to_bytes(4, byteorder="big"))
                client_socket.sendall(receive_data)

                # msg = "echo : " + msg
                # echo_msg = msg.encode()

                # length = len(echo_msg)

                # client_socket.sendall(length.to_bytes(4, byteorder="big"))
                # client_socket.sendall(echo_msg)
                # print(echo_msg)

    except ConnectionResetError as e:
        print(e, addr)

    finally:
        print("Client socket close.")
        client_socket.close()


def main():
    load_dotenv()
    IP = os.environ.get('SERVER_IP')
    PORT = os.environ.get('SOCKET_PORT')

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP, int(PORT)))
    server_socket.listen()
    print('Server start up!')

    try:
        while True:
            print('Receiving data...')
            client_socket, addr = server_socket.accept()
            th = threading.Thread(target=binder, args=(client_socket, addr))
            th.start()
            print("Device address. : ", addr)

    except socket.error as e:
        print(e)

    finally:
        print("Server socket close.")
        server_socket.close()


if __name__ == '__main__':
    main()

# 도커를 로컬 환경으로 실행시 명령어
# docker run -p <PORT>:<PORT> <IMAGE> python socket_server.py
