import openpyxl
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
        check if the input excel file has valid e-mail form
        '''
        for line in self._sheet:
            addressToVerify = line[self.MAIL_COL].value
            regex_mail = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
            match = re.match(regex_mail, addressToVerify)
            if match == None:
                return False

        return True