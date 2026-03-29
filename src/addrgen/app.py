import json
import os
import openai
import time


def lambda_handler(event, context):
    # openai key is in Parameter Store "dev__openai"
    openai_key = os.environ['openai_key']
    sys_mpt = os.environ['sys_mpt']
    usr_mpt = os.environ['usr_mpt']
    body_json = json.loads(event['body'])

    # check if "cur_user" is in event['requestContext']['authorizer'] and authorizer is in event['requestContext']
    if 'requestContext' not in event or 'authorizer' not in event['requestContext'] or 'cur_user' not in event['requestContext']['authorizer']:
        cur_user = 'unknown'
    else:
        cur_user = event['requestContext']['authorizer']['cur_user']

    # replace all "[[key]]" with the value in usr_mpt
    for key, value in body_json.items():
        usr_mpt = usr_mpt.replace(f'[[{key}]]', value)

    addresses_list = gen_address(openai_key, sys_mpt, usr_mpt)
    response = ""
    if body_json["format"].lower() == "json":
        address_dict = {}
        # add a sequence number to each address and put them in a dict, sequence number is key (str), address is value (str)
        for i, address in enumerate(addresses_list):
            address_dict[str(i+1)] = address
            
        response = json.dumps(address_dict, ensure_ascii=False)
    else:
        response = '\n'.join(addresses_list)
    
    return {
        'statusCode': 200,
        'body': response
    }


def gen_address(openai_key: str, sys_mpt: str, usr_mpt: str):
    openai.api_key = openai_key

    # try 5 times if openai is not available
    for i in range(2):
        try:
            chat_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system","content": sys_mpt},
                    {"role": "user", "content": usr_mpt}
                ],
                temperature=0.8
            )

            addresses = chat_completion.choices[0].message.content.strip()
            #print(f"addresses: {addresses}")
            #split the addresses by newline
            addresses_list = addresses.split('\n')
            
            return addresses_list
        except Exception as e:
            try_again_in = 2*(i+1)
            print(f"OpenAI is not available, try again in {try_again_in} seconds, {5-i} times left")
            print(f"Error: {e}")
            time.sleep(2*(i+1))
            continue
