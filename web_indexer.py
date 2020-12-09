#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ipaddress
import socket
import mysql.connector
import requests
import re
from bs4 import BeautifulSoup
import argparse

__author__ = "undefined objects"

def connect_mysql():
  return mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="web_indexes"
  )

def main():
  mydb = connect_mysql()

  parser = argparse.ArgumentParser(description="Web Indexer")
  
  parser.add_argument("-s", "--start", dest="start", type=str, help="Start IP", required=True)
  parser.add_argument("-e", "--end", dest="end", type=str, help="End IP", required=True)

  args = parser.parse_args()


  if mydb.is_connected():
    for ip in range(int(ipaddress.IPv4Address(args.start)), int(ipaddress.IPv4Address(args.end))):
      try:
        webSiteInfo = [ str(ipaddress.IPv4Address(ip)) ]
        webPage = requests.get("http://" + webSiteInfo[0], timeout=(1, 2))
      except:
        print(*webSiteInfo)
        continue

      webSiteName = webPage.url.encode("utf-8")
      webSiteInfo.append(webSiteName)

      soup = BeautifulSoup(webPage.text)

      webTitle = ""
      webDescription = ""
      webKeywords = ""

      try:
          webTitle = soup.find("title").text.encode("utf-8")
      except:
          pass

      webSiteInfo.append(webTitle)

      try:
        allDescription = soup.findAll(attrs={"name": re.compile(r"description", re.I)}) 
        webDescription = allDescription[0]["content"].encode("utf-8")
      except:
        pass

      webSiteInfo.append(webDescription)

      try:
        allKeywords = soup.findAll(attrs={"name": re.compile(r"keywords", re.I)}) 
        webKeywords = allKeywords[0]["content"].encode("utf-8")
      except:
        pass

      webSiteInfo.append(webKeywords)

      mycursor = mydb.cursor()

      sql = "INSERT INTO sites (ip, name, title, description, keywords) VALUES (%s, %s, %s, %s, %s)"
      values = list(webSiteInfo)
      mycursor.execute(sql, values)
      mydb.commit()

      print(*webSiteInfo, sep=" - ")
  else:
    print("Database is Not Connected")

if __name__ == '__main__':
	main()
