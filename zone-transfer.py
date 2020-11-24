###        DNS ZONE TRANSFER SCRIPT        ###
###    AUTHOR: Joseph McCallum-Nattrass    ###
### DESCRIPTION: Inovkes the hosts command ###
### to fetch name servers and attempts DNS ###
###        transfers on each of them       ###

#The subprocess module is needed to run host
import subprocess
#Sys is also needed for specifying the domain
import sys
#Validators enables us to validate the domain
import validators
#Re allows for regex
import re

#Check if the domain is actually valid
if len(sys.argv) > 1:
    if(validators.domain(sys.argv[1]) == False):
            sys.exit("Domain is not valid")
else:
    sys.exit("Domain argument missing")


#Define the command to get the name servers
listNameServers = "host -t ns %s" % sys.argv[1]
hostT = subprocess.Popen(listNameServers.split(), stdout=subprocess.PIPE)
output, error = hostT.communicate()

#Use regex to fetch all of the namesevers
regexedDomain = sys.argv[1].replace(".", "\.")
pattern = "(\w*\.%s)" % regexedDomain
#Return all matches
nameServers = re.findall(pattern, str(output))

#Print the found nameservers
print("Found Name Servers:")
for ns in nameServers:
    print(ns)

#Loop through each name server and attempt a transfer
print("\nAttempting DNS Zone Transfers...\n")
for ns in nameServers:
    print("--- Attempting Transfer On %s ---\n" % ns)
    #Command to perform transfer
    zoneTransfer = "host -l %s %s" % (sys.argv[1], ns)
    hostL = subprocess.Popen(zoneTransfer.split(), stdout=subprocess.PIPE)
    output, error = hostL.communicate()
    print(output.decode("utf-8"))
