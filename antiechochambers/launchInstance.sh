gcloud compute --project "aerobic-datum-126519" ssh --zone "us-central1-b" "instance-3"
gsutil cp -r gs://network-analysis .
cd ~/network-analysis/
chmod u+x setup.sh
./setup.sh
