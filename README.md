# Pi-Housemate-Dectector

Use Python, and a Raspberry Pi, to detect who is home!

### How it works

The python script scans the network to look for the MAC addresses of your smartphones, and then illuminates the corresponding LED to show who's home. If the MAC address is not present on the network for the timeout period, then that person's LED is turned off.   

## Usage 

This script relies on the command line tool arp-scan to scan for the MAC addresses.

To install this on Raspbian use the following commands:

```
sudo apt-get update
sudo apt-get install arp-scan
```
Then test arp-scan installed and is working, try running this command:

```
sudo arp-scan -l
```
This should return a list of devices connected to your local network.

Once arp-scan is installed and working, download and place Pi-Housemate-Detector.py in a directory on your Raspberry Pi. 

Then edit the following lines with your names, MAC addresses of your smartphones, and the GPIO pins the LEDs are wired to on the Pi:

```
# Names of housemates
housemates = ["Adam","Chris","Conor"]

# Corresponding MAC addresses for phones
addresses = ["b4:f1:da:b8:df:cc","ac:5f:3e:30:b2:71","90:2b:d2:f4:da:ae"]

# Corresponding led pin on the Pi
pins = [17,22,27]
```

Save these changes and run the script to test it out:

```
sudo python /path/to/script/Pi-Housemate-Detector.py
```

This should result in an output something like this:

```
Starting presence detection @  2019-05-27 14:21:47.863885                                                                                                                          
Chris's device detected @ 2019-05-27 14:22:02.879145
Chris's device timed out @ 2019-05-27 14:27:05.582073
```

To get the script to run when the Pi starts up, we can add the script to root's crontab.

The prefered way to edit the crontab file with the crontab command, like so:

```
sudo crontab -e
```

And add the following lines:

```
@reboot python /path/to/script/Pi-Housemate-Detector.py &
```

Save and exit your chosen editor, then reboot the Pi to ensure it's works!

