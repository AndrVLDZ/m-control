import telnetlib

def print_logo(logo=''):
    LOGO_DAFAULT = """\033[93m

   /\                 /\\
  / \\'._   (\_/)   _.'/ \\
 /_.''._'--('.')--'_.''._\\
 | \_ / `;=/ " \=;` \ _/ |
  \/ `\__|`\___/`|__/`  \/
   `      \(/|\)/        `
           " ` "
     DAW_Start_By_VLDZ
\033[0m
"""
    if logo != '':
        print(logo)
    else:
        print(LOGO_DAFAULT)

print_logo()

port = int(input('\n PORT: '))
hosts_number = int(input(' Number of hosts: '))
i = 0
ip = []
while i != hosts_number:
    addr = str(input(' Host_' + str(i) + ' IP: '))
    ip.append(addr)
    i+=1
print(len(ip))

while True:
    symbol = str(input('==> '))
    if symbol == 's':
        for i in range(len(ip)):
            node = telnetlib.Telnet(ip[i], port)
            node.write(b's\r\n')
    elif symbol == 'n':
        for i in range(len(ip)):
            node = telnetlib.Telnet(ip[i], port)
            node.write(b'n\r\n')
    elif symbol == 'b':
        for i in range(len(ip)):
            node = telnetlib.Telnet(ip[i], port)
            node.write(b'b\r\n')
    else:
        for i in range(len(ip)):
            node = telnetlib.Telnet(ip[i], port)
            node.write(bytes(str.encode(symbol)))