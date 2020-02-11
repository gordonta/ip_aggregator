import os
from itertools import groupby, cycle

def stringToBinary(ip):
    temp = '.'.join([bin(int(x)+256)[3:] for x in ip.split('.')])
    final = ''.join(i for i in temp if not i == '.')
    return final

def numToBinary(num):
    return format(num, '032b')

#stolen from https://www.geeksforgeeks.org/python-find-groups-of-strictly-increasing-numbers-in-a-list/
def groupSequence(l): 
    temp_list = cycle(l) 
  
    next(temp_list) 
    groups = groupby(l, key = lambda j: j + 1 == next(temp_list)) 
    for k, v in groups: 
        if k: 
            yield tuple(v) + (next((next(groups)[1])), )

#this takes a 32bit binary string and chunks it into 4 bytes separated by a .
def makeBinaryNetwork(ip):
    return str(int(ip[0:8],2))+"."+str(int(ip[8:16],2))+"."+str(int(ip[16:24],2))+"."+str(int(ip[24:32],2))

def groupIPs(grouped_ips):
    for group in grouped_ips:
        #print("========================")
        first = numToBinary(group[0])
        last = numToBinary(group[-1])
        #print("First IP: {} {} {}".format(first, makeBinaryNetwork(first), group[0]))
        #print("Last IP:  {} {} {}".format(last, makeBinaryNetwork(last), group[-1]))
        xor = numToBinary(int(first, 2) ^ int(last, 2))
        #print("XORd IP:  {}".format(xor))
        cidr = str(xor).index('1')
        network_bits = "0" * cidr
        host_bits = "1" * (32-cidr)
        netmask = network_bits + host_bits
        #print("CIDR Bits: {}".format(cidr))
        #print("Netmask:  {}".format(netmask))
        ip_range = makeBinaryNetwork(first)+"/"+str(cidr)
        print(ip_range)

filepath = 'sample_ips.txt'
ips = []
with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
        #print("INPUT Line {}: {}".format(cnt, line.strip()))
        if line == "" or line[0] == "#": #if its a blank line or a comment
            break
        #print(line)
        ip, cidr = line.split("/")
        #print(ip)
        binary = stringToBinary(ip)#error with stringToBinary, adding 1
        int_binary = int(binary, 2)
        ips.append(int_binary)
        #print("Binary: {} INT: {}".format(binary, int_binary))
        #print("OUTPUT Line {}".format(makeBinaryNetwork(binary)))
        line = fp.readline()
        cnt += 1

#print(str(ips))
#print()
sorted_ips = sorted(ips)
#print(str(sorted_ips))
#print()
grouped_ips = list(groupSequence(sorted_ips))
#print(grouped_ips)
#print(grouped_ips[-1])

#takes the list of tuples that reflect ip groupings (ips that increment by 1) and processes that into good data to display
groupIPs(grouped_ips)

    
