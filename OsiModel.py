
def application_layer(message):
    header = "Application Layer Header | "
    new_message = header + message
    print("After Application Layer:", new_message)
    presentation_layer(message)

def presentation_layer(message):
    header = "Presentation Layer Header | "
    new_message = header + message
    print("After Presentation Layer:", new_message)
    session_layer(message)

def session_layer(message):
    header = "Session Layer Header | "
    new_message = header + message
    print("After Session Layer:", new_message)
    transport_layer(message)

def transport_layer(message):
    header = "Transport Layer Header | "
    new_message = header + message
    print("After Transport Layer:", new_message)
    network_layer(message)

def network_layer(message):
    header = "Network Layer Header | "
    new_message = header + message
    print("After Network Layer:", new_message)
    data_link_layer(message)

def data_link_layer(message):
    header = "Data Link Layer Header | "
    new_message = header + message
    print("After Data Link Layer:", new_message)
    physical_layer(message)

def physical_layer(message):
    header = "Physical Layer Header | "
    new_message = header + message
    print("After Physical Layer:", new_message)

def main():
    input_message = input("Enter the application message: ")
    application_layer(input_message)

if __name__ == "__main__":
    main()
