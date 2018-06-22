import serial

ser = serial.Serial('/dev/ttyACM0', 9600) #link arduino serial data

# To find the right serial address for above, unplug the arduino from
# the serial port, type "ls /dev/tty*" into raspberry pi console.
# then plug in the arduino and retype the command. The new address
# that shows up is the one to use for the arduino

#return ppm
def readppm() :
    # Reads unformated ppm from arduino.
    read = ser.readline()   
    
    ppm = ''

    # Formats ppm.
    for letter in read :    
        if letter.isnumeric():
            ppm += str(letter)
        if letter == '.':
            ppm += letter

    # First serial communication will return 0
    if float(ppm) == 0 :   
        return -1
    return ppm




