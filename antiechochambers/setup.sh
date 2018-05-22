sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y build-essential
sudo apt-get install bzip2
cd /tmp
curl -O https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc
conda install ipython -y
cd ~/network-analysis/
pip install -r requirements.txt
pip install --upgrade google-cloud-bigquery
pip install --upgrade google-cloud-storage
ipython
%run network_stats.py
