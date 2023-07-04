# Citation for the following code:
# Date: 6/9/2023
# Adapted from:
# Kurose, J. F., &amp; Ross, K. W. (2021). Computer networking: A top-down approach. Pearson.

from socket import *


def pick_mode(socket, mode):
    """
    Takes two parameters, client socket and mode(chat, Rock Paper Scissors, or /q).
    Allows server to switch between all three modes.
    """

    while True:
        if mode == 'chat':
            mode = start_chat(socket)
        if mode == 'play rps':
            mode = start_rps(socket)
        if mode == '/q':
            return


def start_chat(socket):
    """
    Takes client socket as a parameter.
    Allows server to chat with client.
    Returns a different mode selected by server or client.
    """

    print('--- mode: chat ---\n'
          'Wait for the input prompt\n'
          'Type a message and press ENTER to send message\n'
          'Type "/q" and press ENTER to exit ChatteR\n')

    while True:
        client_reply = socket.recv(4096).decode()

        if client_reply == '/q':
            print('Client has requested shutdown. Shutting down ChatteR, goodbye!')
            return '/q'

        if client_reply == 'play rps':
            print('Client has challenged you to a game of Rock Paper Scissors, get ready!\n')
            return 'play rps'

        print(client_reply)

        response = input('Enter Input >')
        # validate server's response
        while response == '' or len(response.encode()) > 4096:
            if response == '':
                response = input('Input cannot be blank, try again! >')
            if len(response.encode()) > 4096:
                response = input('Input should not exceed 4096 characters, try again! >')

        if response == '/q':
            socket.send(response.encode())
            return '/q'

        socket.send(response.encode())


def start_rps(socket):
    """
    Takes client socket as a parameter.
    Allows server to play Rock Paper Scissors with client.
    Returns a different mode selected by server or client.
    """

    print('--- mode: Rock Paper Scissors ---\n'
          'Wait for the input prompt\n'
          'Type "/q" and press ENTER to exit ChatteR\n'
          'Type one of the options below and press Enter to respond to client\n'
          'r for rock\n'
          'p for paper\n'
          's for scissors\n')

    client_score = 0
    server_score = 0

    print(f"client: {client_score}\n"
          f"server: {server_score}\n")
    # dictionary of possible choices and their counters
    counters = {
        'r': ['Rock', 's', 'p'],
        'p': ['Paper', 'r', 's'],
        's': ['Scissors', 'p', 'r']
    }

    while True:
        print("Waiting for client's move...\n")

        client_reply = socket.recv(4096).decode()

        if client_reply == '/q':
            print('Client has requested shutdown. Shutting down ChatteR, goodbye!')
            return '/q'

        if client_reply == 'chat':
            print('Client would rather chat, exiting Rock Paper Scissors...')
            return 'chat'

        choice = input('Enter your choice >')

        if choice == '/q':
            socket.send(choice.encode())
            return '/q'
        # validate server's choice
        while True:
            if choice not in counters:
                print('Invalid Input!\n'
                      'Enter:\n'
                      'r for rock\n'
                      'p for paper\n'
                      's for scissors\n')
                choice = input('Enter your choice >')
            else:
                break
        # determine winner based on client and server choices
        for c in counters:
            if c == choice:
                if client_reply == c:
                    print(counters[client_reply][0])
                    print('Draw')
                elif client_reply == counters[c][1]:
                    print(counters[client_reply][0])
                    print(f"{counters[c][0]} beats {counters[client_reply][0]}, you win!\n")
                    server_score += 1
                else:
                    print(counters[client_reply][0])
                    print(f"{counters[client_reply][0]} beats {counters[c][0]}, you lose!\n")
                    client_score += 1
        # display updated scores
        print(f"client: {client_score}\n"
              f"server: {server_score}\n")

        socket.send(choice.encode())


serverSocket = socket(AF_INET, SOCK_STREAM)

serverAddress = ('localhost', 4000)

serverSocket.bind(serverAddress)

serverSocket.listen(1)

print('Server listening on {}:{}'.format(*serverAddress))

while True:
    print('Waiting for a client to connect...')

    clientSocket, clientAddress = serverSocket.accept()

    print(f"Client connected: {clientAddress}\n")

    while True:
        print("Waiting on client's decision...\n")

        clientMessage = clientSocket.recv(4096).decode()
        # server redirected based on client's message
        if clientMessage == 'chat':
            print('Client has initiated a chat session')
            pick_mode(clientSocket, 'chat')
            break
        if clientMessage == 'play rps':
            print('Client has challenged you to a game of Rock Paper Scissors, get ready!')
            pick_mode(clientSocket, 'play rps')
            break
        if clientMessage == '/q':
            print('Client has requested shutdown. Shutting down ChatteR, goodbye!')
            break

    clientSocket.close()

    break

serverSocket.close()






