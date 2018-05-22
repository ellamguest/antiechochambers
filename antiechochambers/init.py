from network_stats import *
import subprocess

def exportFiles():
    bucket_name = 'network-analysis'
    files = ["requirements.txt","antiechochambers-1ba7f7f4c68e.json","network_stats.py", "setup.sh"]

    for file_name in files:
        upload_blob(bucket_name, file_name)

if __name__ == "__main__":
    exportFiles()
    subprocess.call(['./launchInstance.sh'])
