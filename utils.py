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


def getLabel(ahd):
  label = ""
  if "CODE" in ahd and ahd["CODE"]:
    label = label + ahd["CODE"]
  elif "NUMMER" in ahd and ahd["NUMMER"]:
    label = label + ahd["NUMMER"]

  titel = getTitel(ahd)
  if label and titel:
    label = label + ". "

  label = label + titel #[0:100]

  return label


def tree(ahd): 
  ahd["icon"] = "https://word2mais.hualab.nl/img/" + ahd["AET"].lower() + ".png"
  ahd["text"] = getLabel(ahd)

  for item in ahd["children"]:
    tree(item) 
