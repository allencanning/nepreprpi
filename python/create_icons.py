#!/usr/local/bin/python3

import png
import pprint

pp = pprint.PrettyPrinter(indent=4)

infile="../data/icons/sprite-team-prep-hockey-boys.png"

# Set default icon height and width
ih = 25

# Open the png file
p = png.Reader(filename=infile)

# Read in the png file
pngdata = p.read()

pp.pprint(pngdata)

width = pngdata[0]
height = pngdata[1]

numfiles = int(height / ih)

rowcount = 0
imgcnt = 0
imagerows = []

for row in pngdata[2]:
#  pp.pprint(row)
  mod = rowcount % ih
#  print("Mod = "+str(mod))
  if rowcount == 0:
    # first file, open it
    ofile = "../data/icons/team-"+str(imgcnt)+".png"
    f = open(ofile,'wb')
    op = png.Writer(width,ih)
  if rowcount != 0 and mod == 0: 
    op.write(f,imagerows)
    imagerows = []
    # close existing file
    f.close()
    # open new file
    ofile = "team-"+str(imgcnt)+".png"
    f = open(ofile,'wb')
    op = png.Writer(width=width,height=ih,alpha=True,greyscale=False,interlace=0,planes=4)
    imgcnt += 1
  imagerows.append(row)
  rowcount += 1

