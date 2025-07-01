import serial
import threading

# Configure the serial port
ser = serial.Serial(
    port='/dev/ttyAMA10',
    baudrate=9600,
    timeout=0
)

# Event to signal shutdown
stop_event = threading.Event()

def read_serial():
    while not stop_event.is_set():
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8', errors='ignore').strip()
            if data:
                print(f"Received: {data}")
                write_to_file("ttl-log.txt", data)
                
def write_serial():
    try:
        while True:
            msg = input()  # Read from keyboard
            if msg.lower() == "exit":
                stop_event.set()  # Signal the read thread to stop
                break
            ser.write((msg + '\n').encode('utf-8'))  # Send to serial

    except KeyboardInterrupt:
        stop_event.set()

def read_from_file():
    pass # todo save input ttl messages into json objects that can be read from file later and retransmitted. 

def write_to_file(filename: str, data: str):
    fn = filename.split('.')
    if fn[len(fn) - 1] == "json": # check file extension
        pass # add write json to file

    elif fn[len(fn) - 1] == "txt":
        with open(filename, "a") as f:
            f.write(f"{data}\n")
    else:
        print("Error: Unsupported file type for file write.")


try:
    print("Type to send. Type 'exit' to quit.\n")
    
    # Run receiver in background thread
    thread = threading.Thread(target=read_serial)
    thread.start()

    # Run sender on main thread
    write_serial()

    # Wait for thread to finish
    thread.join()

finally:
    ser.close()
    print("Serial port closed.")

