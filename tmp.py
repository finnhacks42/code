def extract_key(name):
    if name.startswith("TAB"):
        name = name[3:].split("X")
        key = name[0].zfill(3)+name[1].zfill(3)
        return key
    else:
        return name

l = ["TAB1X22","TAB103X1","TAB1X1","STATE"]
l.sort()
print l
l.sort(key=extract_key)

print l
