import cImage as image

fg = image.Image('secret.gif')
newIm = image.EmptyImage(fg.getWidth(),fg.getHeight())

for row in range(fg.getHeight()):
    for col in range(fg.getWidth()):
        fgpix = fg.getPixel(col,row)
        fgr = fgpix.getRed()

        if fgr % 2 == 0:
            newPix = image.Pixel(255,255,255)
        else:
            newPix = image.Pixel(0,0,0)
        newIm.setPixel(col,row,newPix)

win = image.ImageWin(500,400)
newIm.draw(win)
win.exitonclick()
