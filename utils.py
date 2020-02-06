from common import message_responses
import random as rand


def get_random_message(key):
    message = rand.choice(message_responses[key]["messages"])
    resp = {**message_responses[key], "messages": message, }
    return resp


def get_message_by_id(m_id):
    for key, message in message_responses.items():
        if message["id"] == m_id:
            return key, message
    return None
