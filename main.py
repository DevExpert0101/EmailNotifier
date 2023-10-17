from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from bs4 import BeautifulSoup
import base64
import time
import tkinter as tk
from tkinter import Frame, Text, Scrollbar
import webbrowser
from tkhtmlview import HTMLLabel
from tkinter import *

import threading
from threading import Event

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

root = tk.Tk()
root.geometry("1928x1080")
root.minsize(800, 600)
root.maxsize(1920, 1080)

root.title('Email Notifier')

threads = []

event = Event()

def task(event: Event) -> None:
    for i in range(6):
        print(f'Running #{i+1}')
        
        if event.is_set():
            print('The thread was stopped prematurely.')
            break
    else:
        print('The thread was stopped maturely.')

def stop_threads():
    event.set()  

def on_closing():
    stop_threads()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# f = Frame(root, relief=GROOVE, bd=1)
# f.grid(column=0, row=0,padx=10, pady=10)

from tkinter import ttk

container = ttk.Frame(root)
container.pack(side=LEFT)

canvas = tk.Canvas(container, width=1500, height=800, background='gray75')
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

container.pack()
canvas.pack(side="left", fill="both", expand=True)

scrollbar.pack(side="right", fill="y")




email_widgets = []
widgets = []
def update_email_grid(email_content):
    # Create a new Frame for the email content
    # frame = Frame(f)
    frame = Frame(scrollable_frame)
    frame.grid()

    col = len(email_widgets) % 5
    row = len(email_widgets) // 5

    total_rows = len(email_widgets) // 5
    reversed_row = total_rows - row - 1

    # frame.grid(column=col, row=row, padx=10, pady=10)
    
    

    # Create a Text widget to display the email content
    email_text = Text(frame, wrap='none', height=20, width=30)
    # email_text.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
    email_text.grid()

    # Create a Scrollbar for the Text widget
    scrollbar = Scrollbar(frame, command=email_text.yview)
    # scrollbar.grid(row=0, column=1, padx=5, pady=5, sticky='ns')
    scrollbar.grid()
    email_text['yscrollcommand'] = scrollbar.set

    # Insert the email content into the Text widget
    email_text.insert('1.0', email_content)

    widgets.insert(0, frame)
    # Update the GUI
    # frame.update_idletasks()
    # root.update()

    num_columns = 5
    for i, widget in enumerate(widgets):
        row = i // num_columns
        col = i % num_columns
        widget.grid(row=row, column=col, padx=10, pady=10)

def repeat(service, prev_ids):
    
    while True:
        try:
            result =  service.users().messages().list(userId='me').execute()

            messages = result.get('messages', [])[:10]

            ids = [msg['id'] for msg in messages]

            print(ids)

            if prev_ids != None:
                received_email_num = ids.index(prev_ids[0])
                print('received_email_num: ', received_email_num)

                if received_email_num == 0:
                    for ind in range(10, 0, -1):
                        new_msg = service.users().messages().get(userId='me', id=ids[ind - 1]).execute()
                        
                        print('-'*10)
                        

                        try:
                            payload = new_msg['payload']                  
                            headers = payload['headers']

                            for d in headers:
                                if d['name'] == 'Subject':
                                    subject = d['value']
                                if d['name'] == 'From':
                                    sender = d['value']
                            parts = payload.get('parts')[0]
                            data = parts['body']['data']
                            data = data.replace("-", "+").replace("_", "/")
                            decoded_data = base64.b64decode(data)

                            soup = BeautifulSoup(decoded_data, "lxml")
                            body = soup.body()
                            

                            if sender != 'Central Dispatch <do-not-reply@centraldispatch.com>':
                                print('*')
                                body = str(body)

                                new_email_content = body.split('href="')[1].split(' ')[0]
                                
                                # webbrowser.open_new_tab(new_email_content)


                            else:
                                # body = str(body)
                                new_email_content = body
                                print(body)
                                email_widgets.append(new_email_content)
                                update_email_grid(new_email_content)

                        except Exception as e:
                            print(e)


                    print('\n')

            prev_ids = ids
        except Exception as e:
                print(e)

        time.sleep(1)

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)


        search_result = service.users().messages().list(userId='me').execute()
        messages = search_result.get('messages', [])[:10]

        prev_ids = None

        
        x = threading.Thread(target=repeat, args=(service,prev_ids,))
        x.setDaemon(True)
        x.start()        
                    

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


# if __name__ == '__main__':
#     main()

main()
root.mainloop()