import socket


def client_program():
    host = '127.0.0.1'  # loopback address for local testing
    port = 5000  # socket server port number

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 TCP socket
    client_socket.connect((host, port))  # connect to the server

    heroes = []
    enemies = []
    abilities = []

    while True:
        # get initial data from server
        # decide what step it is
        # initate the handling of the step and get response from user
        # send response back to server
        # get result from server
        # if server says to close, then break

        # TODO: replace this with the above logic
        raw = client_socket.recv(1024)  # read up to 1024 bytes; larger messages require multiple recv() calls
        if not raw:
            break
        try:
            data = raw.decode('utf-8')
        except UnicodeDecodeError:
            print("Received non-UTF-8 data from server, skipping")
            continue

        if data[0] == "1":
            heroes, enemies, abilities, count = data[1:].split(",")
            print(heroes)
            print(enemies)
            print(abilities)

            count = int(count)

            ability_idx = -1
            while ability_idx < 0 or ability_idx >= count:
                try:
                    ability_idx = int(input("Select ability:"))
                except ValueError:
                    print(f"Please input only a number 0-{count-1}")
                    ability_idx = -1
                except Exception:
                    print(f"Unexptected Error: Please try again")
                    ability_idx = -1

            client_socket.sendall(str(ability_idx).encode())  # send message

        elif data[0] == "2":
            targets, count = data[1:].split(",")
            
            print(targets)

            count = int(count)

            target_idx = -1
            while target_idx < 0 or target_idx >= count:
                try:
                    target_idx = int(input("Select target:"))
                except ValueError:
                    print(f"Please input only a number 0-{count-1}")
                    target_idx = -1
                except Exception:
                    print(f"Unexptected Error: Please try again")
                    target_idx = -1

            client_socket.sendall(str(target_idx).encode())

        elif data[0] == "3":
            print(data[1:])

        elif data[0] == "4":
            print(data[1:])
            break

        else:
            client_socket.sendall("0".encode())


    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()