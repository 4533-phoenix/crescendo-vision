# install coral usb driver
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get install libedgetpu1-max -y

# install python
sudo apt install git gcc make -y
sudo apt install libreadline-dev libbz2-dev libssl-dev libncurses5-dev libffi-dev libsqlite3-dev liblzma-dev -y

curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

pyenv install 3.9.18
pyenv local 3.9.18

# install packages
sudo apt install libcap-dev libcamera-dev pkg-config g++ -y
pip install --upgrade pip
pip install --extra-index-url https://google-coral.github.io/py-repo/ pycoral~=2.0
pip install -r requirements.txt

# copy install/vision.service to /etc/systemd/system/vision.service
sudo cp install/vision.service /etc/systemd/system/vision.service
sudo systemctl enable vision.service
sudo systemctl start vision.service