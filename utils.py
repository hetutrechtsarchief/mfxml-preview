def getTitel(ahd):
  # print(ahd)
  if ahd["AET"]=="NOTAKT":
    return getFlexVeld(ahd,["AKTENUMMER"]) + " " + getFlexVeld(ahd,["SOORTAKTE"])
  elif ahd["AET"]=="PNNA" or ahd["AET"]=="PSN":
    return " ".join([
      getFlexVeld(ahd,["VOORNAAM"]),
      getFlexVeld(ahd,["TUSSENVOEGSEL"]),
      getFlexVeld(ahd,["NAAM"])
     ])
  elif ahd["AET"]=="OBJA":
    return " ".join([
      getFlexVeld(ahd,["PLAATS"])
     ])
  else:
    return getFlexVeld(ahd,["TITEL","BESCHRIJVING","INHOUD"])


def getFlexVeld(ahd, names):
  if not "AWE" in ahd:
    return ""

  for awe in ahd["AWE"]:

    for name in names:
      if awe["NAAM"]==name:
        if awe["WAARDE"]:
          return awe["WAARDE"]
        else:
          return ""

  return ""


def getLabel(item):
  if not "NUMMER" in item or not item["NUMMER"]:
    item["NUMMER"] = ""

  if not "CODE" in item or not item["CODE"]:
    item["CODE"] = ""

  # for field in ["NUMMER","CODE"]:
  #   if not field in item:
  #     item[field] = item[field] or ""

  label = "".join([item["NUMMER"],item["CODE"]])

  if label and label[-1]!=".":
    label += "."

  # if "CODE" in item and item["CODE"]:
  #   label = item["CODE"]
  # elif "NUMMER" in item and item["NUMMER"]:
  #   label = item["NUMMER"]

  titel = getTitel(item)
  if label and titel:
    label = label + " "

  # print("xxx",label,type(label),type(titel),titel)
  label = label + titel #[0:100]

  return label


def tree(ahd): 
  ahd["icon"] = "https://word2mais.hualab.nl/img/" + ahd["AET"].lower() + ".png"
  ahd["text"] = getLabel(ahd)

  for item in ahd["children"]:
    tree(item) 
