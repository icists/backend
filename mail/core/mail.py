import openpyxl
import smtplib
from email.mime.text import MIMEText
import re


class MailError(Exception):
    pass

class InvalidContactsError(MailError):
    """
    Anomalous email address detected. Check if all mail address has valid syntax.
    """
    pass

class ContactsExcelProc():
    """
    @functionality
    - read an excel file and parse the contacts
    """
    def __init__(self, filename: str, sheetname="Sheet1", mail_col=2):
        # Constants for management
        self.MAIL_COL = mail_col
        self.CONT_CACHED = False
        
        self._excel_file = openpyxl.load_workbook(filename=filename) # Open excel workbook
        self._sheet = self._excel_file[sheetname] # _sheet containing contacts

        # _contacts contain email address
        self._contacts = []
        if self._is_valid_contacts():
            pass
        else:
            raise InvalidContactsError
    
    def get_contacts(self):
        '''
        @return
        a list of email_address
        '''

        if self.CONT_CACHED:
            return self._contacts

        for line in self._sheet:
            email_address = line[self.MAIL_COL].value
            self._contacts.append(email_address)

        self.CONT_CACHED = True
        return self._contacts

    def _is_valid_contacts(self):
        '''
        @functionality
        check if the input excel file has valid contacts information
        '''
        for line in self._sheet:
            addressToVerify = line[self.MAIL_COL].value
            regex_mail = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
            match = re.match(regex_mail, addressToVerify)
            if match == None:
                return False

        return True

class ContentParser():
    """
    @functionality
    - read content template
    - put args into template
    """
    pass





userID = None
userPW = None

"""
Set name of a file to read
Set User ID, PW -> Security Issue....
"""
excelname= "contents.xlsx"
userid = 'media@icists.org'
userpw = 'icistsmed2005'

#read excel file
contacts_excel = openpyxl.load_workbook(filename= excelname)
excel = contacts_excel.active

sheet = contacts_excel['Sheet1']

google_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
google_server.ehlo()
google_server.login(userid, userpw)






#line[#, txt format number, mail address, subject, argument)
for line in sheet.rows:
    if line[0].value == '#' or line[1].value == None:
        # Skip this line
        continue

    with open('mail%s.txt'%(str(line[1].value)), 'r') as f:
        contents = f.read()

    args = line[4].value.split(',')

    # Check if the number of args do not match the blanks
    if len(args) != contents.count('[]'):
        print("Error with count of argument!! There are %d in txt but there are %d arguments in xlsx\nCheck %s's arguments"%(len(args), contents.count('[]'),line[2].value))
        continue

    for arg in args:
        contents = contents.replace('[]', arg.lstrip(), 1)

    recipients = line[2].value

    msg= MIMEText(contents, _charset = 'UTF-8')
    msg['Subject'] = line[3].value
    msg['To'] = recipients

    print('Email Preview')
    print('Subject : %s'%msg['Subject'])
    print('From: %s'%userid)
    print('To: %s'%recipients)
    print('Contents:\n%s'%contents)

    chk = input("Check and send email! Is it alright?(yes or no)")
    if chk.lower() == 'yes':
    	google_server.sendmail(userid, recipients.split(','), msg.as_string())


'''
    msg = MIMEText(contents, _charset= 'UTF-8')
    #contents -> body of mail
    msg['Subject'] -> title of mail
    msg['From'] -> cannot see in email
    msg['To'] -> seeing in mail

    google_server.sendmail(id, address, msg.as_string()) -> id : not using, address -> get mail , msg -> header of mail)
'''
