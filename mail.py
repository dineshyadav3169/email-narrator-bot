from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import gtts
import os
from playsound import playsound
import time

SCOPES = 'https://www.googleapis.com/auth/gmail.addons.current.message.readonly'

def greets():
    hours = int(time.ctime().split()[3].split(':')[0])
    if hours<=12:
        greet = 'Good ,Morning'
    elif hours>12 and hours<16:
        greet = 'Good ,Afternoon'
    else:
        greet = 'Good ,Evening'

    return greet
    
def main():
    
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))


    # Call the Gmail API to fetch INBOX
    try:
        results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
    except errors.HttpError:
        pass

    
    messages = results.get('messages', [])
    check_id = [messages[0]][0]['id']
    
    
    while(1):
        
        try:
            results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
        except errors.HttpError:
            pass
        
        messages = results.get('messages', [])

        messagess = [messages[0]]
        
        if check_id!=[messages[0]][0]['id']:
            for message in messagess:
                
                try:
                    msg = service.users().messages().get(userId='me', id=message['id']).execute()
                except errors.HttpError:
                    pass
                start_mail_from = msg['payload']['headers'][17]['value'].find('<') - 1
                from_mail = msg['payload']['headers'][17]['value'][0:start_mail_from]

                mail_subject = msg['payload']['headers'][20]['value']

            tts = gtts.gTTS(greets() + ',You have an,new Email , from' + from_mail + '.' + ',' + '.' + mail_subject, lang='en')        
            tts.save("hello.mp3")
            playsound("hello.mp3")
            os.remove("hello.mp3")
        else:
            print('waiting..sync..')

        time.sleep(60)
    
main()
#Done.
