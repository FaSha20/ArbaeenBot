from minio import Minio
from minio.error import S3Error
from io import BytesIO
# import mdf

minio_address = "79.127.71.106:9000"
access_key="grAB47ZriVFQlmXkQGXv"
secret_key="AHsYO5bURE1N8PUXBrtL4lDruHZirUIRyCNDbTzS"

class DAO:
    
    def create_connection():
        client = Minio(
            minio_address,
            access_key=access_key,
            secret_key=secret_key,
            secure=False  # Set to True if using HTTPS
        )
        return client 


    def get_voice_file(client):
        buckets = client.list_buckets()
        print("Connected to MinIO. Here are the buckets:")
        bucket = buckets[0].name
        file_data = BytesIO()
        response = client.get_object(bucket, 'madahi/Karimi/ageBereSaram.mp3')
        file_data.write(response.read())
        file_data.seek(0)  # Move the pointer to the start of the file
        print('ok')
            # objects = client.list_objects(bucket.name, recursive=False)
            #     # for i , obj in enumerate(objects):
            #     #     # mdf.r
            #     #     # print(i , end = ' ')
            #     #     print(obj)

            #     result = client.fget_object(bucket.name, 'madahi/Karimi/ageBereSaram.mp3','savedAudios/test.mp3')
            #     print(result)
        return file_data


