import serial

# Set the COM port and baud rate
com_port = 'COM4'
baud_rate = 115200

# Open a serial connection
ser = serial.Serial(com_port, baud_rate, timeout=1)

# Open a file for writing
output_file = open('received_values.txt', 'w')

try:
    while True:
        # Read a line from the serial port
        line = ser.readline().decode('latin-1').strip()

        try:
            # Convert the received data to an integer
            value = int(line)
            print(f"Received value: {value}")

            # Write the value to the file
            output_file.write(f"{value}\n")
            output_file.flush()  # Ensure data is written immediately

        except ValueError:
            print(f"Invalid data received: {line}")

except KeyboardInterrupt:
    print("Exiting the program.")

finally:
    # Close the serial connection and the file when the program is interrupted
    ser.close()
    output_file.close()


