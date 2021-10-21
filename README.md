# datalogger / Iridium Transmitter

Here you will find all of the scripts which control the recording and transmission of data.

all of the service files are to be copied into /lib/systemd/system and added to the system daemon to automatically run at startup.
the GPSLogger and TeensyLogger will be reading in GPS location, and temperature/pressure/other data regularly, and writing it to files in the ./data/ subdirectory.
IridiumTransmitter will be regularly reading from those files, and transmitting out.

