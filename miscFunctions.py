import os
import json
import boto3
import jwt

APP_NAME = os.getenv('APP_NAME')
ENV_NAME = os.environ["ENV_NAME"]
EMAIL_QUEUE_URL = os.environ["EMAIL_QUEUE_URL"]


KID1 = "L8up7zej5JUDJ17MXAgJKmnG00/+U9KW5UJ36YZR6ow="
PKEY1 = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArsaepG01vGzjRblcynyMgW50gF22jn5DeDzNUrOS7PtzCLgbEkXw0jSRZSUI3byxAgROqY89IbjLcIVQ30mas45y513IUpUHV47zvAVm8qbEqWuUdT0zXX6KijVPO2Dg6SQVWej9A9Wqtewp6qU9XZt9WjL4/1Rc8R7DvYy5AHZl+k7+JpG1MLQ1S6Su7cnS0MeQA7tEYX6fihCxRUSVWFuZEjtX3eb67cAoqXI4TpXBaEp8BZBBkdwZQdyvGnjHZOry8Ehfg3zgnfOBmooAyP19WjtSPVwWinbtRx/Oew03d4Bbe22I+0O/5GwLkA94kxzJKxK4ViH+7Db94KQC+wIDAQAB\n-----END PUBLIC KEY-----"
AUDIENCE = "5ggi6skuunvkei5v0i199l00l1"
KID2 = "w91FdpJFqJi4fI7vkboyrLimF0GreekBys9+RFtp318="
PKEY2 = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwJwnAbpqUAJU5N0Yc+gt+HElEbn4Mjiu3NozHQz+6tT1CpC/ch7tAJIit1ySPMrwGq6sZT59LnWVjcngBE1aVVGHbiz++xgGs/wwiSpcTGCAokNnOOofmTEGxDcou1DXgtKPAp3N1UATLepZ7bpuCqQ/45iGwPCDTibxkmeAG/Z+pC7P+j+XhRRUB+3cdRIuzmNuCV05s1pWtYhXnmCUuefk/JWvxmAyRPwgPRNHQ0G8f1wmmFVKTuo4Tt++QdTWA+u92Dvtjt+vqzm/Zr/0b1n5a1SRNU9+bQ9cW/mhicYH/GZzQw9Ccw5c0dwVBJQa7Cxx4GVjHqA5QhPLwEqabQIDAQAB\n-----END PUBLIC KEY-----"

def authorize_token(token):
    response_message = {}

    kid = jwt.get_unverified_header(token)['kid']
    if kid == KID1:
        pkey = PKEY1
        audience = AUDIENCE
    elif kid == KID2:
        pkey = PKEY2
        audience = AUDIENCE
    else:
        response_message['errorCode'] = 1001
        response_message['errorMessage'] = 'Invalid token. Unknown key id in token!!!'
        return response_message

    try:
        decoded_token = jwt.decode(
            token,
            pkey,
            algorithms=["RS256"],
            options={"verify_signature": True, "verify_aud": True, "verify_exp": True},
            audience=audience
        )
        email = decoded_token['email']
        response_message['errorCode'] = 0
        response_message['developerId'] = email
        return response_message

    except jwt.exceptions.ExpiredSignatureError:
        response_message['errorCode'] = 1002
        response_message['errorMessage'] = 'Invalid token. Token is expired!!!'
        return response_message

    except jwt.exceptions.InvalidSignatureError:
        response_message['errorCode'] = 1003
        response_message['errorMessage'] = 'Invalid token. Token signature fail!!!'
        return response_message

    except jwt.exceptions.InvalidAudienceError:
        response_message['errorCode'] = 1004
        response_message['errorMessage'] = 'Invalid token. Invalid audience claim in token'
        return response_message

    except Exception as e:
        response_message['errorCode'] = 1005
        response_message['errorMessage'] = str(e)
        return response_message
