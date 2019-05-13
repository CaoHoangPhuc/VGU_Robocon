rm arduino/.build/pro5v328/firmware.hex arduino/.build/pro5v328/firmware.elf
cp VGU/arduino_build/VGU_auto.ino.hex arduino/.build/pro5v328/firmware.hex 
cp VGU/arduino_build/VGU_auto.ino.elf arduino/.build/pro5v328/firmware.elf 
cd arduino/
echo "Uploading..."
ino upload -m pro5v328 -p /dev/serial0
