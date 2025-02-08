from websocket_server import WebsocketServer
import serial
import time
import keyboard  # Requires the keyboard module (pip install keyboard)

# Configure the serial connection to the ESP32
esp_serial = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # Replace '/dev/ttyUSB0' with your ESP32's serial port
time.sleep(2)  # Allow time for the ESP32 to initialize

def send_command_to_esp32(command):
    """
    Send a command to the ESP32 and wait for a response.
    """
    try:
        esp_serial.write((command + '\n').encode())  # Send the command
        response = esp_serial.readline().decode().strip()  # Read the response
        print(f"ESP32 response: {response}")
        return response
    except Exception as e:
        print(f"Error communicating with ESP32: {e}")
        return "ERROR"

def handle_message(client, server, message):
    """
    Handle incoming WebSocket messages and forward them to the ESP32.
    """
    print(f"Received command: {message}")
    response = send_command_to_esp32(message)  # Send the command to the ESP32
    server.send_message(client, f"ESP32 response: {response}")  # Send the response back to the client

# Initialize WebSocket server
server = WebsocketServer(host='0.0.0.0', port=8082)  # Listen on all network interfaces on port 8081
server.set_fn_message_received(handle_message)

print("WebSocket server started. Waiting for commands...")

# Main loop to handle keyboard input
if __name__ == "__main__":
    print("Control the motors and thrusters: Arrow Keys for movement, WASD for thrusters. Press Q to quit.")
    
    # Run the WebSocket server in a separate thread
    import threading
    threading.Thread(target=server.run_forever, daemon=True).start()

    while True:
        if keyboard.is_pressed('left'):  # Move left
            print("Camera moving left...")
            print(send_command_to_esp32("CAM L"))  # Send move left command (-50 steps)
            time.sleep(0.05)  # Debounce delay

        elif keyboard.is_pressed('right'):  # Move right
            print("Camera moving right...")
            print(send_command_to_esp32("CAM R"))  # Send move right command (50 steps)
            time.sleep(0.05)  # Debounce delay

        elif keyboard.is_pressed('down'):  # Move down
            print("Camera moving down...")
            print(send_command_to_esp32("CAM D"))  # Send move down command (-50 steps)
            time.sleep(0.05)  # Debounce delay

        elif keyboard.is_pressed('up'):  # Move up
            print("Camera moving up...")
            print(send_command_to_esp32("CAM U"))  # Send move up command (50 steps)
            time.sleep(0.05)  # Debounce delay

        elif keyboard.is_pressed('w'):  # Thruster forward
            print("Thrusters moving forward...")
            print(send_command_to_esp32("THRUSTER FORWARD"))  # Send forward command for thrusters
            time.sleep(0.05)  # Debounce delay

        elif keyboard.is_pressed('s'):  # Thruster backward
            print("Thrusters moving backward...")
            print(send_command_to_esp32("THRUSTER BACKWARD"))  # Send backward command for thrusters
            time.sleep(0.05)  # Debounce delay

        elif keyboard.is_pressed('a'):  # Rotate left
            print("Thrusters rotating left...")
            print(send_command_to_esp32("THRUSTER LEFT"))  # Send rotate left command for thrusters
            time.sleep(0.05)  # Debounce delay

        elif keyboard.is_pressed('d'):  # Rotate right
            print("Thrusters rotating right...")
            print(send_command_to_esp32("THRUSTER RIGHT"))  # Send rotate right command for thrusters
            time.sleep(0.05)  # Debounce delay

        elif keyboard.is_pressed('space'):  # Rotate right
            print("Thrusters stopping...")
            print(send_command_to_esp32("THRUSTER STOP"))  # Send stop command for thrusters
            time.sleep(0.05)  # Debounce delay

        elif keyboard.is_pressed('q'):  # Quit
            print("Exiting...")
            break

# from websocket_server import WebsocketServer
# import serial
# import time

# # Configure the serial connection to the ESP32
# esp_serial = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # Replace '/dev/ttyUSB0' with your ESP32's serial port
# time.sleep(2)  # Allow time for the ESP32 to initialize

# def send_command_to_esp32(command):
#     """
#     Send a command to the ESP32 and wait for a response.
#     """
#     try:
#         esp_serial.write((command + '\n').encode())  # Send the command
#         response = esp_serial.readline().decode().strip()  # Read the response
#         print(f"ESP32 response: {response}")
#         return response
#     except Exception as e:
#         print(f"Error communicating with ESP32: {e}")
#         return "ERROR"

# def handle_message(client, server, message):
#     """
#     Handle incoming WebSocket messages and forward them to the ESP32.
#     """
#     print(f"Received command: {message}")
#     response = send_command_to_esp32(message)  # Send the command to the ESP32
#     server.send_message(client, f"ESP32 response: {response}")  # Send the response back to the client

# # Initialize WebSocket server
# server = WebsocketServer(host='0.0.0.0', port=8082)  # Listen on all network interfaces on port 8082
# server.set_fn_message_received(handle_message)

# if __name__ == "__main__":
#     print("WebSocket server started. Waiting for commands...")
#     server.run_forever()
