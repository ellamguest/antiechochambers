

```python
%autoreload 2

from network_stats import *
```

### dropping weak ties


```python
def get_subset(data, n=10, defaults=None):
    sub_counts = data.subreddit.value_counts()
    author_counts = data.author.value_counts()

    keep_subs = sub_counts[sub_counts>=n].index
    keep_authors = author_counts[author_counts>=n].index
    
    subset = data.copy()
    
    subset=subset[(subset['subreddit'].isin(keep_subs))&
              (subset['author'].isin(keep_authors))&
              (subset['weight']>=n)]
    
    if defaults:
        subset=subset[~subset.isin(defaults)]
    
    return subset
```

### removing defaults


```python
defaults = """
/r/announcements/
/r/Art/
/r/AskReddit/
/r/askscience/
/r/aww/
/r/blog/
/r/books/
/r/creepy/
/r/dataisbeautiful/
/r/DIY/
/r/Documentaries/
/r/EarthPorn/
/r/explainlikeimfive/
/r/food/
/r/funny/
/r/Futurology/
/r/gadgets/
/r/gaming/
/r/GetMotivated/
/r/gifs/
/r/history/
/r/IAmA/
/r/InternetIsBeautiful/
/r/Jokes/
/r/LifeProTips/
/r/listentothis/
/r/mildlyinteresting/
/r/movies/
/r/Music/
/r/news/
/r/nosleep/
/r/nottheonion/
/r/OldSchoolCool/
/r/personalfinance/
/r/philosophy/
/r/photoshopbattles/
/r/pics/
/r/science/
/r/Showerthoughts/
/r/space/
/r/sports/
/r/television/
/r/tifu/
/r/todayilearned/
/r/UpliftingNews/
/r/videos/
/r/worldnews/
"""

defaults_list = [x.strip('/\n') for x in defaults.split('/r/')]
```

### compiling scripts


```python
%run network_stats.py
```

    1
    done with likeus!
    2
    done with newjersey!
    File network_stats.db uploaded.



```python
bucket_name = 'network-analysis'
files = ["requirements.txt","antiechochambers-1ba7f7f4c68e.json","network_stats.py", "googleCloud.py"]

for file_name in files:
    upload_blob(bucket_name, file_name)
```

    File requirements.txt uploaded.
    File antiechochambers-1ba7f7f4c68e.json uploaded.
    File network_stats.py uploaded.
    File googleCloud.py uploaded.


### google cloud compute 


```python
! pipreqs . --force
```

    INFO: Successfully saved requirements file in ./requirements.txt



```python
import argparse

import googleapiclient.discovery


def create_service():
    # Construct the service object for interacting with the Cloud Storage API -
    # the 'storage' service, at version 'v1'.
    # Authentication is provided by application default credentials.
    # When running locally, these are available after running
    # `gcloud auth application-default login`. When running on Compute
    # Engine, these are available from the environment.
    return googleapiclient.discovery.build('storage', 'v1')

def list_buckets(service, project_id):
    buckets = service.buckets().list(project=project_id).execute()
    return buckets


def main(project_id):
    service = create_service()
    buckets = list_buckets(service, project_id)
    print(buckets)


main('aerobic-datum-126519')
```

    {'kind': 'storage#buckets', 'items': [{'kind': 'storage#bucket', 'id': 'network-analysis', 'selfLink': 'https://www.googleapis.com/storage/v1/b/network-analysis', 'projectNumber': '472724286010', 'name': 'network-analysis', 'timeCreated': '2018-05-22T10:52:59.950Z', 'updated': '2018-05-22T10:52:59.950Z', 'metageneration': '1', 'location': 'US', 'storageClass': 'STANDARD', 'etag': 'CAE='}, {'kind': 'storage#bucket', 'id': 'td-all-comments', 'selfLink': 'https://www.googleapis.com/storage/v1/b/td-all-comments', 'projectNumber': '472724286010', 'name': 'td-all-comments', 'timeCreated': '2017-10-11T16:36:48.440Z', 'updated': '2017-10-11T16:36:48.440Z', 'metageneration': '1', 'location': 'EUROPE-WEST1', 'storageClass': 'REGIONAL', 'etag': 'CAE='}, {'kind': 'storage#bucket', 'id': 'tuned-aviary-8376', 'selfLink': 'https://www.googleapis.com/storage/v1/b/tuned-aviary-8376', 'projectNumber': '472724286010', 'name': 'tuned-aviary-8376', 'timeCreated': '2017-07-12T14:41:21.461Z', 'updated': '2017-07-12T14:41:21.461Z', 'metageneration': '1', 'location': 'US', 'storageClass': 'MULTI_REGIONAL', 'etag': 'CAE='}]}



```python
import googleapiclient.discovery

def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items']

def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result

        time.sleep(1)
```


```python
compute = googleapiclient.discovery.build('compute', 'v1')
project = 'aerobic-datum-126519'
zone = 'europe-west4-a'

list_instances(compute, project, zone)
```




    [{'canIpForward': False,
      'cpuPlatform': 'Intel Skylake',
      'creationTimestamp': '2018-05-22T05:26:11.165-07:00',
      'deletionProtection': False,
      'description': '',
      'disks': [{'autoDelete': True,
        'boot': True,
        'deviceName': 'instance-1',
        'guestOsFeatures': [{'type': 'VIRTIO_SCSI_MULTIQUEUE'}],
        'index': 0,
        'interface': 'SCSI',
        'kind': 'compute#attachedDisk',
        'licenses': ['https://www.googleapis.com/compute/v1/projects/debian-cloud/global/licenses/debian-9-stretch'],
        'mode': 'READ_WRITE',
        'source': 'https://www.googleapis.com/compute/v1/projects/aerobic-datum-126519/zones/europe-west4-a/disks/instance-1',
        'type': 'PERSISTENT'}],
      'id': '8213703190054023821',
      'kind': 'compute#instance',
      'labelFingerprint': '42WmSpB8rSM=',
      'machineType': 'https://www.googleapis.com/compute/v1/projects/aerobic-datum-126519/zones/europe-west4-a/machineTypes/n1-standard-1',
      'metadata': {'fingerprint': 'wELp6O-Bl8s=', 'kind': 'compute#metadata'},
      'name': 'instance-1',
      'networkInterfaces': [{'accessConfigs': [{'kind': 'compute#accessConfig',
          'name': 'External NAT',
          'natIP': '35.204.44.76',
          'type': 'ONE_TO_ONE_NAT'}],
        'fingerprint': 'Snvpfi5Wm6U=',
        'kind': 'compute#networkInterface',
        'name': 'nic0',
        'network': 'https://www.googleapis.com/compute/v1/projects/aerobic-datum-126519/global/networks/default',
        'networkIP': '10.164.0.2',
        'subnetwork': 'https://www.googleapis.com/compute/v1/projects/aerobic-datum-126519/regions/europe-west4/subnetworks/default'}],
      'scheduling': {'automaticRestart': True,
       'onHostMaintenance': 'MIGRATE',
       'preemptible': False},
      'selfLink': 'https://www.googleapis.com/compute/v1/projects/aerobic-datum-126519/zones/europe-west4-a/instances/instance-1',
      'serviceAccounts': [{'email': '472724286010-compute@developer.gserviceaccount.com',
        'scopes': ['https://www.googleapis.com/auth/cloud-platform']}],
      'startRestricted': False,
      'status': 'RUNNING',
      'tags': {'fingerprint': '42WmSpB8rSM='},
      'zone': 'https://www.googleapis.com/compute/v1/projects/aerobic-datum-126519/zones/europe-west4-a'}]




```python
import sqlalchemy

sqlalchemy.__version__
```




    '1.1.13'


