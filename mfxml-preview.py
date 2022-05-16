#!/usr/bin/env python3
from sys import argv
import xml.etree.ElementTree as ET 
import lxml.etree as etree
import re,sys
import xml.dom.minidom as md
from bs4 import BeautifulSoup
import xmltodict, json
from utils import *

latestAHD = None

if len(argv)!=3:
  sys.exit("Usage: "+argv[0]+" input.MFXML output.HTML")

with open(argv[1], 'r', encoding="utf-8") as file:
  
  print("reading text file", file=sys.stderr)
  contents = file.read()

  print("string replace", file=sys.stderr)
  # print(contents.find("<MFEXPORT"))
  # sys.exit()

  contents = contents.replace("\ufeff","") # remove BOM

  if contents.find("<MFEXPORT")!=0: # if the string does not start with 
    contents = "<MFEXPORT>\n" +  contents

  contents = contents+"</MFEXPORT>" # add root tag
  contents = contents.replace("&","&amp;") # escape &
  contents = contents.replace("<BCURS","&lt;BCURS") # escape <
  contents = contents.replace("<ECURS","&lt;ECURS") # escape <
  contents = re.sub(r"<(\d+)", r"&lt;\1", contents) # escape <1976 to &lt;1976
  contents = contents.replace("<ZR>","\n") # fix <ZR>  <ZR/>

  # writing tmp.xml for testing
  print("Writing to tmp.xml (should now be valid xml)")
  with open("tmp.xml", 'w') as tmp:
    print(contents, file=tmp)

  # sys.exit()

  print("xml from string", file=sys.stderr)
  xml = ET.fromstring(contents)

  # from here the XML should have a valid syntax
  # now improve the semantics by moving INRICHTING, REL, ABD as child of AHD
  print("processing records", file=sys.stderr)
  ahds = []
  for i in xml:

    if i.tag=='AHD':
      if latestAHD:
        ahds.append(latestAHD)   # don't mutate xml but create a new one

      latestAHD = i
    elif re.match(r'INRICHTING|REL|ABD', i.tag):  # add child to new AHD
      latestAHD.append(i)

    else:
      print("Unkown element: " + i.tag, file=sys.stderr)

  ahds.append(latestAHD) # add the final one

  result = ET.fromstring("<MFEXPORT/>")
  for i in ahds:
    result.append(i)


  # print("print using minidom", file=sys.stderr)
  # xmlstring = ET.tostring(result, encoding="utf8").decode("utf8")
  xmlstr = ET.tostring(result).decode()
  # newxml = md.parseString(xmlstr)
  # print(newxml.toprettyxml(indent='  ',newl=''))


  print("creating preview", file=sys.stderr)
  od = xmltodict.parse(xmlstr) # OrderedDict


  items = json.loads(json.dumps(od)) #convert OrderedDict to Dict
  itemsByID = {} # lookup table by ID

  for item in items["MFEXPORT"]["AHD"]: # AHD=[ {}, {}, {}]
    itemsByID[item["ID"]] = item
    item["children"] = [] # create child array for each item

  for item in items["MFEXPORT"]["AHD"]: # AHD=[ {}, {}, {}]
    # if not "children" in item:
      
    parent = itemsByID[item["AHD_ID"]] if "AHD_ID" in item else None

    if parent:
      parent["children"].append(item)


########################
# code for Preview. creates a nested json file for jstree with 'icon' and 'text' added to each item

  top = itemsByID["1"]

  tree(top) #traverse / recursive function starting at top

  html_file = open(argv[2],'w')

  print('<meta charset="utf-8">',file=html_file)
  print('<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>',file=html_file)
  print('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jstree/3.2.1/themes/default/style.min.css" />',file=html_file)
  print('<script src="https://cdnjs.cloudflare.com/ajax/libs/jstree/3.2.1/jstree.min.js"></script>',file=html_file)

  print('<style>body { font-family:verdana; font-size:11px; background: rgba(212, 230, 232, 0.48); }</style>',file=html_file)
  print(f"<button onclick=\"$('#tree').jstree('open_all');\">open alles</button>",file=html_file)
  print(f"<button onclick=\"$('#tree').jstree('close_all');\">sluit alles</button>",file=html_file)
  print('<div id="tree"></div>',file=html_file)
  s = json.dumps({ "core": { "data": top }}, ensure_ascii=False) #"plugins" : [ "state" ]

  s = s.replace("[BCURS]","<em>")
  s = s.replace("[ECURS]","</em>")

  print(f"<script>$('#tree').jstree({s});</script>",file=html_file)

