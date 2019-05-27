import subprocess
from datetime import datetime
from datetime import timedelta
from time import sleep
from threading import Thread
import RPi.GPIO as GPIO

# Set RPi GPIO pin mapping, this may require tweaking depending on your Pi
GPIO.setmode(GPIO.BCM)

# Names of housemates
housemates = ["Adam","Chris","Conor"]

# Corresponding MAC addresses for phones
addresses = ["b4:f1:da:b8:df:cc","ac:5f:3e:30:b2:71","90:2b:d2:f4:da:ae"]

# Corresponding led pin on the Pi
pins = [17,22,27]

if len(housemates) != len(addresses):
    print "housemates and address arrays are different lengths! Exiting"
    exit()
    
if len(housemates) != len(pins):
    print "housemates and pins arrays are different lengths! Exiting"
    exit()
    
# Array to hold last detected time for each housemate
detectedTime = [datetime(2000,1,1)] * len(housemates)

# Array to hold previous detected status of device, reduces unnecessary printing and GPIO operations
previousStatus = [False] * len(housemates)

# Initial delay to allow network to connect etc
sleep(30)

print "Starting presence detection @ " , datetime.now()

# Function that monitors arp-scan output for address i
def monitor(i):
    
    GPIO.setup(pins[i], GPIO.OUT)
    GPIO.output(pins[i], GPIO.LOW)
    
    # Short delay to wait for output to be populated
    sleep(10)

    # Loop through checking for devices and counting if they're not present
    while True:
    
        # Keep a copy of the global array so we can wait for it to change later
        usedArray = output

        # If a listed device address is present
        
        if addresses[i] in output:
            
            # If the previous status was not detected
            if previousStatus[i] == False:
                print(housemates[i] + "'s device detected @") , datetime.now()
                
                # Turn the LED on
                GPIO.output(pins[i], GPIO.HIGH)
            
            # When a device is detected, reset the timeout counter
            detectedTime[i] = datetime.now()
            
            # Set the previous status to detected
            previousStatus[i] = True
            
        # If a listed device address is not present
        else:
            # If the timeout period has passed from the last time the device was detected
            if datetime.now() >= (detectedTime[i] + timeoutDelta):
                
                # If the previous status was detected
                if previousStatus[i]:
                    print(housemates[i] + "'s device timed out @") , datetime.now()
                    
                    # Turn the LED off
                    GPIO.output(pins[i], GPIO.LOW)

                # Set the previous status to not detected
                previousStatus[i] = False

        # While the output is the same as the array we have already checked
        # This will mean each thread will process the new output as soon as the main thread updates it
        while output == usedArray:
            
            # if there has been a Keyboard Interrupt
            if interrupted == True: 
                exit()
            
            sleep(1)

# Main thread

try:

    # A variable to signal to other threads an interrupt has occured
    global interrupted
    interrupted = False
    
    # This specifies how long a device has to undetected for before we consider the person away
    global timeoutDelta 
    timeoutDelta = timedelta(seconds=300)
    
    # Start a thread for every housemate
    for i in range(len(housemates)):
        t = Thread(target=monitor, args=(i,))
        t.start()

    while True:        
        # Make global output to contain result of arp-scan
        global output
        output = subprocess.check_output("arp-scan -l", shell=True)
        
        # Wait between scans
        sleep(10)

except KeyboardInterrupt:
    # If a Keyboard interrupt occurs, signal this to the other threads 
    interrupted = True
    GPIO.cleanup()
    exit()
