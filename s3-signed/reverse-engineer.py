import base64
import hmac
from hashlib import sha1
import boto3
import os


def generate_random_secret_key():
    return base64.b64encode(os.urandom(32)).decode()



def create_signed_url(bucket, key, expiration=3600):
    s3 = boto3.client('s3')
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket,
            'Key': key
        },
        ExpiresIn=expiration
    )
    return url

def reverse():
    result = ''
    access_key = 'ASIAWFOD2FP2PNVEYEWT'.encode("UTF-8")
    string_to_sign = 'GET 1706977682 x-amz-security-token:IQoJb3JpZ2luX2VjEKoI= /strata-2024/data2.txt' \
        .encode("UTF-8")

    while ('OxQHlg+H5v1STFpoX/M/40U3Veg=' != result):
        secret_key = generate_random_secret_key().encode("UTF-8")

        signature = base64.b64encode(
            hmac.new(
                secret_key, string_to_sign, sha1
            ).digest()
        ).strip()
        result = signature.decode()
        print(f"AWS {access_key.decode()}:{signature.decode()}")

if __name__ == '__main__':

    url = create_signed_url('strata-2024', 'data.txt', 20)
    print(url)

    url = create_signed_url('strata-2024', 'data2.txt', 20)
    print(url)

    # reverse()



