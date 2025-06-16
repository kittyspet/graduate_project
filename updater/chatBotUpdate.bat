C:/rtlink/env/Scripts/python.exe c:/rtlink/mainForPng.pyw
pscp -pw 4rAKymAAV4 -r C:/rtlink/attachment/ Kirill.Malkov@192.168.192.40:/home/botTemplate/bot-fix/attachment/
plink -batch -pw 1hyScdIZxw Aleksey.Orachev@192.168.192.40 '/home/botTemplate/bot-fix/script'
plink -batch -pw 1hyScdIZxw Aleksey.Orachev@192.168.192.40 '/home/botTemplate/bot-fix/logscript'

pscp -pw 4rAKymAAV4 -r C:/rtlink/attachment/ Kirill.Malkov@192.168.192.40:/home/botTemplate/test_bot-fix/attachment/
plink -batch -pw 1hyScdIZxw Aleksey.Orachev@192.168.192.40 '/home/botTemplate/test_bot-fix/script'
plink -batch -pw 1hyScdIZxw Aleksey.Orachev@192.168.192.40 '/home/botTemplate/test_bot-fix/logscript'