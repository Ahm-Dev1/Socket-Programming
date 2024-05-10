import socket
import json

# Function to load menu data from file
def load_menu():
    try:
        with open("menu.json", "r") as menu_file:
            menu_data = json.load(menu_file)
        return menu_data
    except FileNotFoundError:
        return {}

# Function to save menu data to file
def save_menu(menu_data):
    with open("menu.json", "w") as menu_file:
        json.dump(menu_data, menu_file)

# Function to authenticate owner
def authenticate_owner(username, password):
    # You can implement your authentication logic here
    # For simplicity, let's assume a hardcoded list of owners
    owners = {"ibrahim": "123", "owner2": "password2"}
    return owners.get(username) == password

# Function to handle client connections
# Function to handle client connections
def handle_client(client_socket):
    # Send menu to client
    menu_data = load_menu()
    client_socket.sendall(json.dumps(menu_data).encode())

    # Receive owner/customer type
    client_type = client_socket.recv(1024).decode()

    if client_type == "owner":
        # Owner authentication
        username = client_socket.recv(1024).decode()
        password = client_socket.recv(1024).decode()
        if authenticate_owner(username, password):
            client_socket.sendall("Authentication successful. You can now modify the menu.".encode())
            while True:
                # Receive owner's choice
                owner_choice = client_socket.recv(1024).decode()
                if owner_choice == "add":
                    # Receive new item details from owner
                    new_item_name = client_socket.recv(1024).decode()
                    new_item_price = client_socket.recv(1024).decode()
                    # Add new item to menu
                    menu_data[new_item_price] = new_item_name
                    # Save menu data to file
                    save_menu(menu_data)
                    client_socket.sendall("Item added successfully.".encode())
                elif owner_choice == "edit":
                    # Receive item to edit and its new details from owner
                    item_to_edit = client_socket.recv(1024).decode()
                    new_price = client_socket.recv(1024).decode()
                    if item_to_edit in menu_data:
                        # Update item price
                        menu_data[item_to_edit] = new_price
                        # Save menu data to file
                        save_menu(menu_data)
                        client_socket.sendall("Item edited successfully.".encode())
                    else:
                        client_socket.sendall("Item not found in the menu.".encode())
                elif owner_choice == "exit":
                    break
            # Handle menu modification
            # Add your menu modification logic here
        else:
            client_socket.sendall("Authentication failed. Please try again.".encode())
    # Handle customer order
    # Handle customer order
    elif client_type == "customer":
        # Handle customer order
        order = {}
        while True:
            order_data = client_socket.recv(4096).decode()
            print("Received:", order_data)  # Debug print
            if order_data == "done":
                print("Received 'done' message from client.")  # Debug print
                break
            order = json.loads(order_data)
            # Process each order item

        # Receive delivery address from customer
        delivery_address = client_socket.recv(1024).decode()
        print("Received delivery address:", delivery_address)  # Debug print

        # Calculate total price
        total_price = sum(menu_data[item] * quantity for item, quantity in order.items() if item in menu_data)

        # Send confirmation message
        confirmation_message = f"Thank you for your order! Your total price is ${total_price}. We will deliver to {delivery_address}."
        client_socket.sendall(confirmation_message.encode())

        # Close the connection to the client after sending the confirmation message
        client_socket.close()


# Main function to start the server
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 9999))
    server_socket.listen(5)
    print("Server started. Listening for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        handle_client(client_socket)
        client_socket.close()

if __name__ == "__main__":
    main()
