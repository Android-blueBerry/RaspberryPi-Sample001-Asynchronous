# v1.0(2022/03/01)

import bluetooth
import subprocess
import threading

subprocess.call("sudo hciconfig hci0 piscan", shell=True) # discoverable on

HOST = ""
PORT = bluetooth.PORT_ANY
UUID = "00001101-0000-1000-8000-00805F9B34FB"

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

# 서비스 클래스 및 프로파일 등록
name = "raspberrypi"
service_id = UUID
service_classes = [UUID, bluetooth.SERIAL_PORT_CLASS]
profiles = [bluetooth.SERIAL_PORT_PROFILE]

bluetooth.advertise_service(server_socket, name, service_id, service_classes, profiles)
print("advertising...")

# accept
client_socket, client_address = server_socket.accept()
print("accept! ", client_address)

# receive (Sub Thread<Demon>)
''' 메인 스레드가 종료되면 자동으로 종료됩니다. '''
def receive():
    while True:
        try:
            data: str = client_socket.recv(1024).decode('utf-8')
            print("receive:", data)

        except:
            print("receive error")
            client_socket.close()
            break


receive_thread = threading.Thread(target=receive)
receive_thread.daemon = True
receive_thread.start()

# send (Main Thread)
while True:
    try:
        data = input("전송: ")
        client_socket.send(data)

    except:
        print("send error")
        client_socket.close()
        break