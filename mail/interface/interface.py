import sys

from ..core.connect import GMailConnect
from ..core.excel_proc import ContactsExcelProc
from ..core.parser import ContentParser


def load_contacts(_filename):
    p = ContactsExcelProc(_filename)
    return p.get_contacts()

def generate_values():
    pass

def put_values(_template, _val):
    p = ContentParser(_template, _val)
    return p.get_content()
    
def connect_mail_server():
    return GMailConnect()

def send_mails(conn, to, _subject, _template, _val):
    conn.work(to, _subject, put_values(_template, _val))










def main():
    # load excel and extract contacts
    file = "../tmp/Book1.xlsx"
    contacts = load_contacts(file)

    # load, parse templates, and put values
    template = "/Users/junss/tech/backend/mail/data/templates/spe_invi_ko.json"
    
    # send mails through gmail
    conn = GMailConnect()
    for to in contacts:
        my_val = {"name": "Bongjun", "age": "21", "target": "마이클 루덴"}
        send_mails(conn, to, "Hello", template, my_val)


if __name__ == "__main__":
    main()