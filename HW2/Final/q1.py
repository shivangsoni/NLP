import re
s="""
    qwertyuiop
    asdfghjkl

    zxcvbnm
    token qwerty
    token hi
"""


items=re.findall("token.*$",s,re.MULTILINE)
for a in items:
  print(a)
