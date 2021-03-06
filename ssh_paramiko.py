import paramiko
import time
import getpass
import sys


def addnewvip(ip,username,password,output_buffer):

    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # initiate SSH connection
    remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
    print "SSH connection established to %s" % ip+"\n"

    # Use invoke_shell to establish an 'interactive session'
    remote_conn = remote_conn_pre.invoke_shell()
    print "Interactive SSH session established\n"

    # Strip the initial router prompt
    output = remote_conn.recv(output_buffer)

    # See what we have
    print output

    # Now let's try to send the NS a command
    ##### add new config #####
    remote_conn.send("\n"
    +"add server prdtestlb001 192.168.1.1\n"
    +"add service svc-8080-prdtestlb001 prdtestlb001 HTTP 8080\n"
    +"add cs vserver cs-80-testlb HTTP 1.1.1.1 80 -stateupdate ENABLED -caseSensitive OFF\n"
    +"add cs vserver cs-443-testlb SSL 1.1.1.1 443 -stateupdate ENABLED -caseSensitive OFF\n"
    +"add lb vserver lb-80-testlb.default HTTP\n"
    +"bind lb vserver  lb-80-testlb.default svc-8080-prdtestlb001\n"
    +"bind cs vserver cs-80-testlb -lbvserver lb-80-testlb.default\n"
    +"bind cs vserver cs-443-testlb -lbvserver lb-80-testlb.default\n")

    # Wait for the command to complete
    time.sleep(2)

    output = remote_conn.recv(output_buffer)
    # See what we have
    print output

def rmvip(ip,username,password,output_buffer):

    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # initiate SSH connection
    remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
    print "SSH connection established to %s" % ip+"\n"

    # Use invoke_shell to establish an 'interactive session'
    remote_conn = remote_conn_pre.invoke_shell()
    print "Interactive SSH session established\n"

    # Strip the initial router prompt
    output = remote_conn.recv(output_buffer0)

    # See what we have
    print output

    # Now let's try to send the NS a command
    ##### Remove config #####
    remote_conn.send("\n"
    +"rm cs vserver cs-80-testlb\n"
    +"rm cs vserver cs-443-testlb\n"
    +"rm lb vserver lb-80-testlb.default\n"
    +"rm server prdtestlb001\n")

    # Wait for the command to complete
    time.sleep(2)

    output = remote_conn.recv(output_buffer)
    # See what we have
    print output

def checkconfig(ip,username,password,output_buffer):
    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # initiate SSH connection
    remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
    print "SSH connection established to %s" % ip+"\n"

    # Use invoke_shell to establish an 'interactive session'
    remote_conn = remote_conn_pre.invoke_shell()
    print "Interactive SSH session established - to Check config on NS\n"

    # Strip the initial router prompt
    output = remote_conn.recv(output_buffer)

    # See what we have
    print output

    # Turn off paging
    #disable_paging(remote_conn)

    # Now let's try to send the router a command
    remote_conn.send("\n"
    +"\n"
    +"show run | g testlb\n")

    # Wait for the command to complete
    time.sleep(2)

    output = remote_conn.recv(output_buffer)
    # See what we have
    print output

if __name__ == '__main__':

    # VARIABLES
    ip = 'xx.xx.xx.xx'
    output_buffer = 1000000
    option = raw_input("\n"
    +"##################### NETSCALER #####################\n"
    +"\n"
    +"\n"
    +"Please choose one of the otpions below:\n"
    +"\n"
    +"[1] - Add new VIP \n\n"
    +"[2] - Check the configuration on Netscaler \n\n"
    +"[3] - Remove VIP on Netscaler \n\n"
    +"[option]:")

    print "\n\n##################### TACACS Login #####################\n"
    username = raw_input('\ninsert your username:')
    password = getpass.getpass("Enter your password:")


    if (option == '1'):
        print "\n###### NEW VIP ########\n"
        addnewvip(ip,username,password,output_buffer)
        sys.exit(0)

    if (option == '2'):

        print "\n\n\nNow Checking the configuration you made on Netscaler\n"
        checkconfig(ip,username,password,output_buffer)
        sys.exit(0)

    if (option == '3'):
        print "\n###### RM VIP ########\n"
        rmvip(ip,username,password,output_buffer)
        sys.exit(0)

    sys.exit(0)
