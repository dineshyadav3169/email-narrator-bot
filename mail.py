from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import gtts
import os
from playsound import playsound
import time

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

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
    results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
    messages = results.get('messages', [])

    messagess = [messages[1]]
    check_id = messagess[0]['id']

    print('check 1')
    while (1):
        
        if [messages[0]][0]['id']==check_id:
            print('waiting..sync..')
        else:
            check_id = messagess[0]['id']
            for message in messagess:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                my_text = msg['snippet']
        
            print(my_text)
            tts = gtts.gTTS(greets() + ',You have an,new Email ,' + my_text, lang='en')        
            tts.save("hello.mp3")
            playsound("hello.mp3")
            os.remove("hello.mp3")
        messagess = [messages[0]] 
        time.sleep(60)

main()
#Done.
