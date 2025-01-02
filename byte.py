FLAG = 0x7E      
ESC = 0x7D       
FLAG_ESC = 0x5E  
ESC_ESC = 0x5D   

def byte_stuffing(data):
    """Simulate byte stuffing by escaping FLAG and ESC bytes in the data."""
    stuffed_data = bytearray()
    stuffed_data.append(FLAG)  
    for byte in data:
        if byte == FLAG:
            
            stuffed_data.append(ESC)
            stuffed_data.append(FLAG_ESC)
        elif byte == ESC:
            
            stuffed_data.append(ESC)
            stuffed_data.append(ESC_ESC)
        else:
            
            stuffed_data.append(byte)
    stuffed_data.append(FLAG)  
    return stuffed_data

def byte_unstuffing(stuffed_data):
    """Simulate byte unstuffing by reversing the escape sequences."""
    if stuffed_data[0] != FLAG or stuffed_data[-1] != FLAG:
        raise ValueError("Frame is not correctly flagged")

    unstuffed_data = bytearray()
    i = 1  
    while i < len(stuffed_data) - 1:  
        byte = stuffed_data[i]
        if byte == ESC:
            i += 1  
            if i < len(stuffed_data) - 1:
                escaped_byte = stuffed_data[i]
                if escaped_byte == FLAG_ESC:
                    unstuffed_data.append(FLAG)  
                elif escaped_byte == ESC_ESC:
                    unstuffed_data.append(ESC)   
                else:
                    raise ValueError(f"Invalid escape sequence at index {i}: {escaped_byte}")
        else:
            
            unstuffed_data.append(byte)
        i += 1
    return unstuffed_data

def main():
    
    original_data = bytearray([0x01, 0x02, FLAG, 0x03, ESC, 0x04, 0x05, FLAG])
    
    print("Original Data:", list(original_data))

    
    stuffed_data = byte_stuffing(original_data)
    print("Stuffed Data:", list(stuffed_data))

    
    unstuffed_data = byte_unstuffing(stuffed_data)
    print("Unstuffed Data:", list(unstuffed_data))

    
    if unstuffed_data == original_data:
        print("Byte unstuffing successful: Data matches original!")
    else:
        print("Byte unstuffing failed: Data does not match original!")

if __name__ == "__main__":
    main()
