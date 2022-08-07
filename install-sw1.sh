# pip install pipx
# pipx install poetry
# pipx ensurepath
# source ~/.bashrc

# curl -sSL https://install.python-poetry.org | python3 -
# -C- continue -S show error -o output
curl -sSL -C- -o install-poetry.py  https://install.python-poetry.org
python install-poetry.py
rm install-poetry.py
echo export PATH=~/.local/bin:$PATH > ~/.bashrc
source ~/.bashrc
# ~/.local/bin/poetry install

wget -c https://deb.nodesource.com/setup_12.x
bash setup_14.x
apt-get install -y nodejs
npm install -g npm@latest
npm install -g nodemon
rm setup_124.x

# pytorch cpu
#  pip3 install torch==1.8.2+cpu torchvision==0.9.2+cpu torchaudio==0.8.2 -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html

# install sshd and publickey
apt-get install openssh-server
echo ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOl+SiDFL1ZUh1QJ0454eYKtamkMCVs2hhuv3cWN1LU7 id_ed25519_colab >> ~/.ssh/authorized_keys

# apt update  # alerady done in apt-get install -y nodejs
apt install byobu -y > /dev/null 2>&1
byobu-enable
cd /usr/src/app
byobu
