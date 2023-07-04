# Citation for the following code:
# Date: 6/9/2023
# Adapted from:
# Kurose, J. F., &amp; Ross, K. W. (2021). Computer networking: A top-down approach. Pearson.

from socket import *


def pick_mode(socket, mode):
    """
    Takes two parameters, client socket and mode(chat, Rock Paper Scissors, or /q).
    Allows client to switch between all three modes.
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
    Allows client to chat with server.
    Returns a different mode selected by client or server.
    """

    print('--- mode: chat ---\n'
          'Wait for the input prompt\n'
          'Type a message and press ENTER to send message\n'
          'Type "play rps" and press ENTER to play a game of Rock Paper Scissors\n'
          'Type "/q" and press ENTER to exit ChatteR\n')

    while True:
        message = input('Enter Input >')
        # validate client's message
        while message == '' or len(message.encode()) > 4096:
            if message == '':
                message = input('Input cannot be blank, try again! >')
            if len(message.encode()) > 4096:
                message = input('Input should not exceed 4096 characters, try again! >')

        if message == '/q':
            socket.send(message.encode())
            return '/q'

        if message == 'play rps':
            socket.send(message.encode())
            return 'play rps'

        socket.send(message.encode())

        server_reply = socket.recv(4096).decode()

        if server_reply == '/q':
            print('Server has requested shutdown. Shutting down ChatteR, goodbye!')
            return '/q'

        print(server_reply)


def start_rps(socket):
    """
    Takes client socket as a parameter.
    Allows client to play Rock Paper Scissors with server.
    Returns a different mode selected by client or server.
    """

    print('--- mode: Rock Paper Scissors ---\n'
          'Wait for the input prompt\n'
          'Type "chat" and press ENTER to start chatting\n'
          'Type "/q" and press ENTER to exit ChatteR\n'
          'Type one of the options below and press Enter to start game\n'
          'r for rock\n'
          'p for paper\n'
          's for scissors\n')
    # dictionary of possible choices and their counters
    counters = {
        'r': ['Rock', 's', 'p'],
        'p': ['Paper', 'r', 's'],
        's': ['Scissors', 'p', 'r']
    }

    client_score = 0
    server_score = 0

    print(f"client: {client_score}\n"
          f"server: {server_score}\n")

    while True:
        choice = input('Enter your choice >')

        if choice == '/q':
            socket.send(choice.encode())
            return '/q'

        if choice == 'chat':
            socket.send(choice.encode())
            return 'chat'
        # validate client's choice
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

        socket.send(choice.encode())

        server_reply = socket.recv(4096).decode()

        if server_reply == '/q':
            print('Server has requested shutdown. Shutting down ChatteR, goodbye!')
            return '/q'
        # determine winner based on client and server choices
        for c in counters:
            if c == choice:
                if server_reply == c:
                    print(counters[server_reply][0])
                    print('Draw')
                elif server_reply == counters[c][1]:
                    print(counters[server_reply][0])
                    print(f"{counters[c][0]} beats {counters[server_reply][0]}, you win!\n")
                    client_score += 1
                else:
                    print(counters[server_reply][0])
                    print(f"{counters[server_reply][0]} beats {counters[c][0]}, you lose!\n")
                    server_score += 1
        # display updated scores
        print(f"client: {client_score}\n"
              f"server: {server_score}\n")


clientSocket = socket(AF_INET, SOCK_STREAM)

serverAddress = ('localhost', 4000)

clientSocket.connect(serverAddress)

print('Connected to server on {}:{}\n'.format(*serverAddress))

while True:
    print('Welcome to ChatteR!\n'
          'Wait for the input prompt\n'
          'Type "chat" and press ENTER to start chatting\n'
          'Type "play rps" and press ENTER to play a game of Rock Paper Scissors\n'
          'Type "/q" and press ENTER to exit ChatteR\n')

    message = input('Enter Input >')

    while True:
        # client redirected based on input
        if message == 'chat':
            clientSocket.send(message.encode())
            pick_mode(clientSocket, 'chat')
            break
        if message == 'play rps':
            clientSocket.send(message.encode())
            pick_mode(clientSocket, 'play rps')
            break
        if message == '/q':
            clientSocket.send(message.encode())
            break
        # client input is invalid, re-prompted
        print('Invalid Input!\n'
              'Type "chat" and press ENTER to start chatting\n'
              'Type "play rps" and press ENTER to play a game of Rock Paper Scissors\n'
              'Type "/q" and press ENTER to exit ChatteR\n')

        message = input('Enter Input >')

    clientSocket.close()

    break
