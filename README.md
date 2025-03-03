# P10 Thesis
This is the repository containing the thesis for 10th semester at AAU.

## Local setup
Install WSL using PowerShell
```powershell
wsl --install
```

Update WSL and Install the following packages: 
```bash
sudo apt update && sudo apt upgrade -y && sudo apt install build-essential git cmake libboost-all-dev libcln-dev libgmp-dev libginac-dev automake libglpk-dev libhwloc-dev libz3-dev libxerces-c-dev libeigen3-dev doxygen libyaml-tiny-perl libfile-homedir-perl
```

Install WSLU (utilities to make links work properly): 
```bash
sudo add-apt-repository ppa:wslutilities/wslu
sudo apt update
sudo apt install wslu
```

Install GH CLI: 
```bash
(type -p wget >/dev/null || (sudo apt update && sudo apt-get install wget -y)) \
	&& sudo mkdir -p -m 755 /etc/apt/keyrings \
        && out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
        && cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
	&& sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
	&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
	&& sudo apt update \
	&& sudo apt install gh -y
```

Login with GH CLI (**Requires WSLU** to work): 
```bash
gh auth login
```

Make sure you select SSH and create a new ssh-token.
```bash
gh auth setup-git
```

Install Tex: 
```bash
mkdir tmp && cd tmp && curl -L -o install-tl-unx.tar.gz https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
```

```bash
zcat < install-tl-unx.tar.gz | tar xf -
```

```bash
cd install-tl-*
```

```bash
./install-tl --texdir=~/texlive/2024 --no-interaction
```

Note: texdir is relevant to the IntelliJ TeXiFy plugin.

prepend ~/texlive/YYYY/bin/PLATFORM to your PATH 
e.g., add:
```bash
export PATH="$HOME/texlive/2024/bin/x86_64-linux:$PATH"
```

to .bashrc.

In case you have missing packages, as reported by the texlive intallation, you may have to run the following command: 
```bash
sudo env PATH="$PATH" tlmgr update --all --reinstall-forcibly-removed
```

You can then clean up by removing the tmp folder you downloaded the texlive distribution to:
```bash
rm -rf tmp/
```

Install Storm: 
```bash
sudo git clone -b stable https://github.com/moves-rwth/storm.git /opt/storm
```

```bash
sudo mkdir /opt/storm/build && cd /opt/storm/build
```

```bash
sudo cmake ..
```

```bash
sudo make -j4
```

Replace the `4` with any amount of cores you want. If you only have 16gb of ram, you might not be able to run with more than 2.

Clone CuPAAL and P10-Thesis repositories.

## Windows stuff
Install VSCode
- Install Remote Development plugin
- install Latex Workshop
Install Docker Desktop

Install IntelliJ
- Texify IDEA plugin
- pdfviewer


### Git
On a fresh computer it is a good idea to follow the official [First Time Git Setup](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup).
