import json
import sys
from wunderapi import WunderApi
import tasks_endpoint
import notes_endpoint

from imapclient import IMAPClient

import email

def create_inbox_task(subject, note):
    wunder_api = WunderApi()
    client = wunder_api.get_client(config['wunderlist']['access_token'],config['wunderlist']['client_id'] )
    task = tasks_endpoint.create_task(client, 141201128, subject)

    notes_endpoint.create_note(client, task["id"], note)

with open(sys.argv[1]) as json_data_file:
    config = json.load(json_data_file)

server = IMAPClient(config['email']['host'], use_uid=True, ssl=False)
server.login(config['email']['user'], config['email']['password'])

select_info = server.select_folder('INBOX')
messages = server.search(['NOT', 'DELETED'])

message_id = "<"+sys.argv[2]+">"

response = server.fetch(messages, ['RFC822'])
for msgid, data in response.items():
    msg = email.message_from_string(data[b'RFC822'].decode("utf-8"))
    if (msg['Message-ID'] == message_id):

        from io import StringIO
        from email.generator import Generator
        fp = StringIO()
        g = Generator(fp, mangle_from_=True, maxheaderlen=60)
        g.flatten(msg)
        text = fp.getvalue()

        start_index = text.find('Content-Type: text/plain;')
        stop_index = text.find("Content-Transfer", start_index)
        html = text[start_index:stop_index]
        create_inbox_task(msg['subject'], html)
