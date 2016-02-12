import json
import time
import logging

import requests


def gather_data(api_key, username, test_id):
    fetching_time = int(time.time()) - 8000
    logger = logging.getLogger()
    try:
        parameters = {'TestID': test_id, 'Fields': 'performance,time,status,time,location', 'Start': fetching_time}
        headers = {'API': api_key, 'Username': username}
        r = requests.get('https://www.statuscake.com/API/Tests/Checks', params=parameters, headers=headers)
        return json.loads(r.text)
    except:
        logger.warn('no new values from statuscake api')
