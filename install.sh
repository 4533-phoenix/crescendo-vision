# start
echo "Starting installation"
echo "Hope everything goes well!"

# install coral usb driver
echo "Installing Coral USB driver"
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get install libedgetpu1-max -y

# install python
echo "Installing Python"
sudo apt install git gcc make -y
sudo apt install build-essential python3-dev python3-pip libreadline-dev libbz2-dev libssl-dev libncurses5-dev libffi-dev libsqlite3-dev liblzma-dev -y

curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
. ~/.bashrc

pyenv install 3.9.18
pyenv local 3.9.18

# install packages
echo "Installing packages"
sudo apt install libcap-dev libcamera-dev pkg-config g++ libkms++-dev libfmt-dev libdrm-dev ffmpeg libsm6 libxext6 libatlas-base-dev libopenjp2-7  -y
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# modify config
echo "Modifying config"
sudo echo -e '\n' >> /boot/config.txt
sudo echo '#-------Vision service-------' >> /boot/config.txt
sudo echo 'dtoverlay=vc4-kms-v3d' >> /boot/config.txt
sudo echo 'camera_auto_detect=1' >> /boot/config.txt

# install service
echo "Installing service"
sudo cp install/vision.service /etc/systemd/system/vision.service
sudo sed -i "s|%path%|$(pwd)|g" /etc/systemd/system/vision.service
sudo chmod 644 /etc/systemd/system/vision.service
sudo systemctl enable vision.service

# finish
echo "Installation complete"
echo "Read through logs to ensure everything is working as expected. If so, reboot the system to start the service."
echo "Have a great day!"