import datetime
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    method_arn = event['methodArn']
    auth_token = event['authorizationToken']
    # method_arn = arn:aws:execute-api:us-east-1:12345668:abcd1234/ESTestInvoke-stage/GET/
    # print("="*20)
    # print(auth_token)
    # print("="*20)
    # get "us-east-1" from method_arn
    region = method_arn.split(':')[3]
    # get "12345668" from method_arn
    account_id = method_arn.split(':')[4]
    # get "abcd1234" from method_arn
    api_id = method_arn.split(':')[5].split('/')[0]
    
    return {
        "principalId": "user",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow" if validate_request(auth_token) else "Deny",
                    "Resource": f"arn:aws:execute-api:{region}:{account_id}:{api_id}/*/*"
                }
            ]
        },
        "context": {
            "cur_user": "steve"
        }
    }

def validate_request(token:str):
    # split the token into 2 parts based on "-"
    parts = token.split("-")
    if len(parts) != 2:
        return False
    
    # if the first part is not acd, return False
    if parts[0] != "acd":
        return False
    
    # if the second part is not the last date of the current month, return False
    # get the last date of the current month
    today = datetime.date.today()
    last_day_of_month = datetime.date(today.year, today.month, 1) + datetime.timedelta(days=32)
    last_day_of_month = last_day_of_month.replace(day=1) - datetime.timedelta(days=1)
    if parts[1] != last_day_of_month.strftime("%Y%m%d"):
        return False
    
    return True