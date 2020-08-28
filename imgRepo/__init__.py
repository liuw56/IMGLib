import boto3
import yaml

with open("./auth_credentials.yaml") as f:
    cred = yaml.load(f, Loader=yaml.FullLoader)

s3 = boto3.resource('s3')
bucket = s3.Bucket('image-repository-grace-2020')
data = open("../portrait.jpg", 'r')
bucket.put_object(Key="portrait.jpg", Body=data)
obj = s3.Object('image-repository-grace-2020', 'portrait.jpg')
print(obj.get())
