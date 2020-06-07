#!/bin/python3
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import argparse, platform

_appname_="mailr"
_version_="0.1"
_description_="A simple fake mailer"
_author_="blackc8"

ncol   ="\033[0m"
bold   ="\033[1m"
dim    ="\033[2m"
uline  ="\033[4m"
reverse="\033[7m"
red    ="\033[31m"
green  ="\033[32m"
yellow ="\033[33m"
blue   ="\033[34m"
purple ="\033[35m"
cyan   ="\033[36m"
white  ="\033[37m"

if platform.system == "Windows":
    ncol=bold=dim=uline=red=green=yellow=blue=purple=cyan=white=''

def inf(msg,enD="\n"):
   print(dim+blue+"[i] "+ncol+bold+blue+msg+ncol,end=enD)

def scs(msg,enD="\n"):
    print(dim+green+"[+] "+ncol+bold+green+msg+ncol,end=enD)

def err(msg,enD="\n"):
    print(dim+red+"[-] "+ncol+bold+red+msg+ncol,end=enD)

def wrn(msg):
    print(dim+red+"[!] "+ncol+bold+red+msg+ncol)

def ask(msg):
    inp=input(purple+dim+"[?] "+ncol+bold+purple+msg+white)
    print(ncol,end='')
    return inp

def inp(msg):
    inp=input(bold+green+msg+white)
    print(ncol,end='')
    return inp

default_from="blackc8@no-reply.com"
mailr_url="http://blackc8-1.000webhostapp.com/upload/mailr.php"

big_banner=bold+green+"""
\t                 _ _
\t _ __ ___   __ _(_) |_ __
\t| '_ ` _ \ / _` | | | '__|
\t| | | | | | (_| | | | |
\t|_| |_| |_|\__,_|_|_|_| """+"("+white+_version_+green+")"+red+"\n\n\t [ "+_description_+" ]"+white+"\n\t © Copyright 2020 blackc8"+white+"\n      GitHub: "+uline+purple+"github.com/blackc8/mailr"+ncol

min_banner=bold+green+"mailr ("+white+_version_+green+") ["+blue+"blackc8"+green+"]("+uline+purple+"github.com/blackc8/mailr"+green+")"+ncol


def send_mail(Mto,Mfrom,Msubject,Mbody):
    form = { "to": Mto, "from": Mfrom, "subject": Msubject, "body": Mbody }
    request = Request(mailr_url, urlencode(form).encode())
    response= urlopen(request).read().decode()
    return bool(response)


def mailr_interactive():
    print("")
    print(bold+green+reverse+"Send a new mail"+ncol)

    inf("use comma to separate reciptanats")
    mailTos=inp("to: ").split(',')
    while len(mailTos) == 0:
        err("Reviptants can't empty. Try again.")
        mailTos=inp("to: ").split(',')

    mailFm=inp("from: ")
    if mailFm == "":
        inf("Sender not given. Set to default("+default_from+")")
        mailFm=default_from

    mailSb=inp("subject: ")
    inf("Enter 'EOF' when done")
    print(bold+blue+"body: "+white)
    mailBd=""
    while True:
        line=input("")
        if line == "EOF": break
        mailBd+=line+"\n"
    mailCn=int(inp("count: "))

    for mailTo in mailTos:
        for count in range(1,mailCn+1):
            scs("Sending mail to "+mailTo+" count: "+str(count)+"  ...",enD='')
            try:
                if send_mail(mailTo,mailFm,mailSb,mailBd):
                    print(bold+green+"success"+ncol)
                else: print(bold+red+"failed"+ncol)

            except:
               print(bold+red+"error")
    if(ask("Do you want to send more mail(y/N)? ").upper() == "Y"):
        mailr_interactive()
    else: exit()


parser = argparse.ArgumentParser(description=_description_,epilog="Author: "+_author_)
parser.add_argument("-i","--interactive",help="launch the interactive mode",action="store_true")
parser.add_argument("-t","--mail_to",help="email address of the reciptants")
parser.add_argument("-f","--mail_from",help="email address of the sender")
parser.add_argument("-s","--subject",help="subject of the email",default='')
parser.add_argument("-b","--body",help="body of the email",default='')
parser.add_argument("-c","--count",help="number of times email to be sent",default=1)

args = parser.parse_args()

if args.interactive:
    print(big_banner)
    print("")
    wrn(bold+"Warning: "+ncol+dim+red+"This is application is only for educational purpose.\n    I am not responsible for any of your mischievous attempts")
    try:
        mailr_interactive()
    except:
        print(bold+red+"Exting.."+ncol)
    exit()

print(min_banner)
print("")
wrn(bold+"Warning: "+ncol+dim+red+"This is application is only for educational purpose.\n    I am not responsible for any of your mischievous attempts")
print("")
if not args.mail_to:
    err("Email reciptant no given!")
    exit()

if not args.mail_from:
    inf("Sender not given. Set to default("+default_from+")")
    mailFm=default_from
else:
    mailFm=args.mail_from

for mailTo in args.mail_to.split(','):
    for count in range(1,int(args.count)+1):
        scs("Sending mail to "+mailTo+" count: "+str(count)+"  ...",enD='')
        try:
            if send_mail(mailTo,mailFm,args.subject,args.body):
                print(bold+green+"success"+ncol)
            else: print(bold+red+"failed"+ncol)

        except:
            print(bold+red+"error"+ncol)
