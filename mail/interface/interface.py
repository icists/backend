import sys

sys.path.append('..')

from core.connect import GMailConnect
from core.excel_proc import ContactsExcelProc
from core.parser import ContentParser

contacts = None
template = None

def load_contacts(_filename):
    p = ContactsExcelProc(_filename)
    contacts = p.get_contacts()
    

def main():
    # load excel and extract contacts
    file = "../tmp/Book1.xlsx"
    excel_process = ContactsExcelProc(file)
    contacts = excel_process.get_contacts()

    print(contacts)
    # load, parse templates, and put values
    template = "/Users/junss/tech/backend/mail/data/templates/spe_invi_ko.json"
    my_val = {"name": "Bongjun", "age": "21", "target": "마이클 루덴"}
    p = ContentParser(template, my_val)

    # send mails through gmail
    conn = GMailConnect()
    for to in contacts:
        conn.work(to, "Hello", p.get_content())


if __name__ == "__main__":
    main()