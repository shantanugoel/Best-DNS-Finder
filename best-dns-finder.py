#!/usr/bin/python
#By Shantanu Goel http://tech.shantanugoel.com/
import subprocess
import re

dnsfile   = 'dns-servers.txt'
sitesfile = 'sites.txt'
total_latency = []
total_lookup_errors = []
total_reach_errors = []
debug = 1

def main():
  servers = [line.strip() for line in open(dnsfile)]
  sites = [line.strip() for line in open(sitesfile)]
  i = 0
  for server in servers:
    if debug:
      print "SERVER: " + server
    total_latency.append(0)
    total_reach_errors.append(0)
    total_lookup_errors.append(0)
    for site in sites:
      error = ''
      lookup = subprocess.Popen(["nslookup", site, server], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
      ip, error = lookup.communicate()
      if (len(error) != 0):
        total_lookup_errors[i] = total_lookup_errors[i] + 1
      else:
        ip = [line.strip().split(':') for line in ip.split('\n') if line.strip()]
        ip = ip[len(ip) - 1][len(ip[len(ip) - 1]) - 1]
      if debug:
        print site + ": " + ip
        ping = subprocess.Popen("ping -c 4" + ip, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
        ping_out, error = ping.communicate()
        if (len(error) != 0):
          if debug:
            print error
          total_reach_errors[i] = total_reach_errors[i] + 1
        else:
          matcher = re.compile("rtt min/avg/max/mdev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)")
          latency = matcher.search(ping_out)
          if (latency == None):
            if debug:
              print "Cannot ping"
            total_reach_errors[i] = total_reach_errors[i] + 1
          else:
            latency = latency.groups()
            if debug:
              print latency
            total_latency[i] = total_latency[i] + float(latency[1])
    i=i + 1
  i = 0
  for server in servers:
    print "Server:" + server + " Lookup Errors: %d Reach Errors: %d Avg latency: %d" % (total_lookup_errors[i], total_reach_errors[i], total_latency[i]/(len(sites) - total_reach_errors[i]))
    i = i + 1

main()
