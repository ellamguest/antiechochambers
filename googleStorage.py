import google.auth
from google.cloud import storage

""" GOOGLE STORAGE FUNCTIONS """

def get_storage_client():
    credentials, project = google.auth.default() # why returning empty project name?
    project = 'aerobic-datum-126519'
    return storage.Client(project=project,
                             credentials=credentials)
def list_buckets():
    storage_client = get_storage_client()
    buckets = list(storage_client.list_buckets())
    print(buckets)
    
def create_bucket(bucket_name):
    storage_client = get_storage_client()
    bucket = storage_client.create_bucket(bucket_name)
    print('Bucket {} created.'.format(bucket.name))
    
def upload_blob(bucket_name, file_name):
    """Uploads a file to the bucket."""
    storage_client = get_storage_client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)

    blob.upload_from_filename(file_name)

    print(f'File {file_name} uploaded.')   