cd VGU/arduino_build
mv libraries/ lib/
mv sketch/ src/
ino build -m pro5v328
echo "Uploading"
ino upload -m pro5v328 -p /dev/serial0
