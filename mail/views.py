from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
import openpyxl

import smtplib
from email.mime.text import MIMEText
import pickle
import os.path
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import os
import json
from .core.parser import ContentParser


class Invitation():
    def __init__(self, row): 
        self.row = row

        self.LANG = 0
        self.MAIL = 1
        self.NAME = 2
        self.SENDER = 3
        self.FIELD = 4
        self.ONE_SEN = 5
        self.DATE = 6
        self.DESC = 7
        self.DONE = 8
        self.ETC = 9
    
    def is_eng(self):
        if self.row[self.LANG].value == '영':
            return True
        return False

    def get_mail(self):
        return self.row[self.MAIL].value

    def get_name(self):
        return self.row[self.NAME].value
    
    def get_sender(self):
        return self.row[self.SENDER].value
    
    def get_field(self):
        return self.row[self.FIELD].value
    
    def get_sentence(self):
        return self.row[self.ONE_SEN].value

    def get_date(self):
        return self.row[self.DATE].value
    
    def is_done(self):
        if self.row[self.DONE].value == 'O':
            return True
        return False
    
    def __str__(self):
        return "{}, {}".format(self.get_name(), self.get_mail())

def index(request):
    if request.method == 'GET':
        return render(request, 'mail/index.html', {})

    # load excel file
    excel_file = request.FILES['excel_file']
    wb = openpyxl.load_workbook(excel_file)
    ws = wb['Sheet1']
    invitations = parse_excel_file(ws)
    # connect to gmail server
    creds = login()
    service = build('gmail', 'v1', credentials=creds)

    # send mails
    for invi in invitations:
        send_mail(invi, service)
    
    return render(request, 'mail/index.html', {'excel_data':invitations})

def parse_excel_file(worksheet, header=True):
    invitations = []
    empty_count = 0
    # gathering excel file data
    for i, row in enumerate(worksheet.iter_rows()):
        # ignore header file
        if header == True:
            if i == 0:
                continue
        # too many Nones.. ignore them
        is_valid_row = True
        for cell in row:
            if cell.value == None:
                empty_count += 1
                is_valid_row = False
                break
            else:
                empty_count = 0
                break
        if empty_count > 3:
            break
        if is_valid_row:
            invitations.append(Invitation(row))
        if empty_count >= 3:
            for _ in range(3):
                invitations.pop()
    return invitations

def send_mail(invi, service, user_id='me'):
    # create message
    if invi.is_eng():
        template = os.path.dirname(os.path.realpath(__file__)) + '/data/eng.json'
    else:
        template = os.path.dirname(os.path.realpath(__file__)) + '/data/kor.json'
    val = {
        'name': invi.get_name(),
        'sender': invi.get_sender(),
        'field': invi.get_field(),
        'date': invi.get_date(),
        'one_sen': invi.get_sentence(),
    }
    p = ContentParser(template = template, values = val)
    subject = p.get_title() 
    print("To: {:30}\nTitle: {:40}\n".format(str(invi), p.get_content()))
    msg_txt = p.get_content()
    message = MIMEText(msg_txt, _charset = 'utf-8')
    message['subject'] = subject
    message['from'] = user_id
    message['to'] = invi.get_mail()
    # send message
    # message = (service.users().messages().send(userId=user_id, body=message).execute())

def login():
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # Check if the crudential is already stored as pickle
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credential = os.path.dirname(os.path.realpath(__file__)) + '/credentials.json'
            flow = InstalledAppFlow.from_client_secrets_file(
                credential, SCOPES)
            creds = flow.run_local_server(port=8000)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds
