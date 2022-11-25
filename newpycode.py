import time
import serial
import RPi.GPIO as GPIO
from os.path import exists
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def sleep_ms (ms):
    time.sleep(ms/1000)
    
def cmd(cmd_string):
    cmd_string = cmd_string.encode()
    lora.write(cmd_string)
    
def send(adress, str_to_send):
    send_str = "AT+SEND={},{},{}\r\n"
    encoded_send = send_str.format(adress,len(str_to_send),str_to_send)
    cmd(encoded_send)

def ask_address():
    ask_string = "AT+ADDRESS?\r\n"
    cmd(ask_string)

def set_address(address):
    set_address_string = "AT+ADDRESS={}\r\n"
    cmd_address = set_address_string.format(address)
    cmd(cmd_address)
        
def ask_networkID():
    ask_string = "AT+NETWORKID?\r\n"
    cmd(ask_string)

def set_networkID(new_ID):
    set_networkID_string = "AT+NETWORKID={}\r\n"
    cmd_networkID = set_networkID_string.format(new_ID)
    cmd(cmd_networkID)
        
if _name_ == "_main_":
    
    path_to_file = "lora_log.txt"
    
    if exists(path_to_file):
        f = open("path_to_file", "a")
    else:
        f = open("path_to_file", "x")
    
    print("Main, setup lora")
    lora = serial.Serial(
        '/dev/ttyS0',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS)
    time.sleep(1)
    set_address(1)
    sleep_ms(10)
    set_networkID(11)
    sleep_ms(100)
    if lora.inWaiting() != 0:
        reply = lora.readline()
    print("Setup done")
    try:
        print("Starting listening")
        while True:
            if lora.inWaiting() != 0:
                reply = lora.readline()
                print(reply.decode().strip('\r\n'))
                f.write(reply.decode().strip('\r\n'))

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    except Exception as e:
        print(e)
    finally:
        print("Cleaning connections, pins and files")
        GPIO.cleanup()
        lora.close()
        f.close()