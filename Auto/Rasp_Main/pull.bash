rm -r ~/Phuc/bk_VGU
mv ~/Phuc/VGU ~/Phuc/bk_VGU
mkdir ~/Phuc/VGU
sshpass -p "crossfire.datMS9" scp -r donot@192.168.1.50:C:/Users/donot/OneDrive/Desktop/Workspace/Pi/Main/* ~/Phuc/VGU/
chmod +x /home/pi/Phuc/VGU/*
echo "Done"
