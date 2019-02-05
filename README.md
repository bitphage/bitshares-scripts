bitshares-scripts
=================

This is a small scripts collection for doing various stuff in Bitshares

Installation using pipenv
-------------------------

1. Make sure you have installed required packages: `apt-get install gcc make libssl-dev`
2. Install [pipenv](https://docs.pipenv.org/) or:

```
# Install pip and pipenv
sudo apt install python3-pip python3-dev
pip3 install --user pipenv

# Add pipenv (and other python scripts) to PATH
echo "PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc
source ~/.bashrc
```

3. Run `pipenv install` to install the dependencies
4. Copy `common.yml.example` to `common.yml` and change variables according to your needs
5. Now you're ready to run scripts:

```
pipenv shell
./script.py
exit
```

**Note:** some scripts are sending transactions, you need to add private active keys for your accounts via `uptick addkey`
