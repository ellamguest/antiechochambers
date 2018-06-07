if [[ ! -e env]]; then
    sudo apt-get update upgrade
    sudo apt-get install -y build-essential bzip2
    cd /tmp
    curl -O https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh
    source ~/.bashrc


    # have to restart terminal here
    sudo reboot
    pip install virtualenv
    virtualenv --python python3 env
    source env/bin/activate
    conda install ipython -y
    cd ~/network-analysis/
    pip install -r requirements.txt
    #pip install --upgrade google-cloud-bigquery google-cloud-storage
    python VMTest.py



# if env already exists can skip to here
source env/bin/activate
cd ~/network-analysis/
python VMTest.py
