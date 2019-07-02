import imaplib
import email
import sys
from emailparser import EmailParser

# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------
ORG_EMAIL   = "@gbills.com"
FROM_EMAIL  = "manask" + ORG_EMAIL
FROM_PWD    = "Hyd3r@b@d"
SMTP_SERVER = "mail.gbills.com"
SMTP_PORT   = 25

def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)

        try:
            mail.login(FROM_EMAIL,FROM_PWD)
        except imaplib.IMAP4.error:
            print "LOGIN FAILED!!! "
            sys.exit(1)

        mail.select('Purchases')

        type, data = mail.search(None, 'ALL')
        print  data, type
        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

       # instantiate the parser
        for i in range(latest_email_id, first_email_id, -1):
            typ, data = mail.fetch(i, '(RFC822)' )
            print i, typ
            if i == latest_email_id:
               for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print 'From : ' + email_from + '\n'
                    print 'Subject : ' + email_subject + '\n'
                    for part in msg.walk():
                        if part.get_content_type() == "text/html":
                         print 'Extracted Details :' + EmailParser(html = '<body>'+str(part.get_payload(decode=True))+'</body>').parse() + '\n'
                        else:
                         continue
               break


    except Exception, e:
        print str(e)


def main():
    read_email_from_gmail()

if __name__ == "__main__":
        main()