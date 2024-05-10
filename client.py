import socket
import json

# Function to receive menu from server
def receive_menu(server_socket):
    menu_data = server_socket.recv(4096).decode()
    return json.loads(menu_data)

# Function for owner authentication
def owner_authentication(server_socket):
    # Send client type
    server_socket.sendall("owner".encode())

    # Send username and password
    username = input("Enter username: ")
    server_socket.sendall(username.encode())
    password = input("Enter password: ")
    server_socket.sendall(password.encode())

    # Receive authentication result
    auth_result = server_socket.recv(1024).decode()
    print(auth_result)

    if auth_result == "Authentication successful. You can now modify the menu.":
        while True:
            print("Choose an option:")
            print("1. Add a new item")
            print("2. Edit an existing item")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                server_socket.sendall("add".encode())
                new_item_name = input("Enter the name of the new item: ")
                server_socket.sendall(str(len(new_item_name)).encode())

                server_socket.sendall(new_item_name.encode())
                new_item_price = input("Enter the price of the new item: ")
                server_socket.sendall(new_item_price.encode())
                response = server_socket.recv(1024).decode()
                print(response)
            elif choice == "2":
                server_socket.sendall("edit".encode())
                item_to_edit = input("Enter the name of the item to edit: ")
                server_socket.sendall(item_to_edit.encode())
                new_price = input("Enter the new price: ")
                server_socket.sendall(new_price.encode())
                response = server_socket.recv(1024).decode()
                print(response)
            elif choice == "3":
                server_socket.sendall("exit".encode())
                break
            else:
                print("Invalid choice. Please try again.")

# Function for customer ordering
# Function for customer ordering
def customer_ordering(server_socket, menu_data):
    # Display menu to customer
    print("Menu:")
    for item, price in menu_data.items():
        print(f"{item}: ${price}")

    # Get customer's order
    order = {}
    while True:
        item = input("Enter the name of the item you want to order (or type 'done' to finish): ")
        if item.lower() == "done":
            server_socket.sendall("done".encode())
            print("Sent 'done' message to server.")  # Debug print
            break
        quantity = int(input(f"Enter the quantity of {item}: "))
        order[item] = quantity

    # Send customer's order to the server
    server_socket.sendall(json.dumps(order).encode())

    # Receive delivery address from customer
    delivery_address = input("Enter your delivery address: ")
    server_socket.sendall(delivery_address.encode())

    # Receive confirmation message from the server
    confirmation_message = server_socket.recv(4096).decode()
    print(confirmation_message)

    # Close the connection to the server
    server_socket.close()


# Main function to connect to the server
def main():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect(("localhost", 9999))
        print("Connected to server.")

        menu_data = receive_menu(server_socket)

        # Choose client type
        client_type = input("Are you an owner or a customer? Enter 'owner' or 'customer': ")

        if client_type == "owner":
            owner_authentication(server_socket)
        elif client_type == "customer":
            customer_ordering(server_socket, menu_data)
        else:
            print("Invalid client type.")

    except ConnectionAbortedError:
        print("Connection aborted. Please check your network connection.")
    except ConnectionResetError:
        print("Connection reset by peer. Please check your network connection.")

if __name__ == "__main__":
    main()

