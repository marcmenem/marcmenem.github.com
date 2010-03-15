#!/usr/bin/python
import numpy as np
import numpy.linalg as la
import pylab as py
import Image

import homography as ho
import scipy.misc as mi



np.set_printoptions(precision=2,threshold=2000,edgeitems=5, linewidth=150, suppress=True)

#feImage
if True:
    # psMap = py.imread('../pspmap.png')

    maxx = 512
    maxy = 256

    top = 40
    width = 256
    height = 250
    base = 20

    p0 = ((0,0),(0,top))
    p1 = ((maxx,0),(width,top))
    p2 = ((0,maxy),(int(width/2-base),height))
    p3 = ((maxx,maxy),(int(width/2+base),height))
    
    pts = (p0,p1,p2,p3)
    h = ho.getHomography(pts)
    h=h[0]
    
    psMap = np.zeros((maxy,maxx,4))
    ym, xm, dm = psMap.shape
    for x in range(xm):
        for y in range(ym):
            dest = h*np.matrix([[x,y,1]]).T
            dest = dest.T.tolist()[0]
            psMap[y,x] = np.array([dest[0]/dest[2], dest[1]/dest[2], 0, 255.0]) / 255.0
    
    py.imshow( psMap )
    
    ym, xm, dm = psMap.shape
    for x in range(xm):
        for y in range(ym):
            psMap[y,x,0]=( (psMap[y,x,0]*255 - x + 65536) % 256 )/255.0
            psMap[y,x,1]=( (psMap[y,x,1]*255 - y + 65536) % 256 )/255.0
            
    dMap = psMap

    mi.imsave( "../fdisplacement512-marc.png", psMap)
else:
    dMap = py.imread('../fdisplacement512.png')


"""

dMap2 = np.zeros((dMap.shape[0]+256, dMap.shape[1]+256, 4))
dMap2[128:dMap.shape[0]+128, 128:dMap.shape[1]+128, :] = dMap

out = np.ones((dMap.shape[0]+128, dMap.shape[1]+128, 4))


# input
im = Image.open('../fmap-relief.png')
im = im.rotate(135)
sc = np.reshape( np.array(im.convert('RGBA').getdata()), ( im.size[1], im.size[0],4) )/256.0
#sc = py.imread('../fmap.png')

# feOffset
dx = 100
dy = 200
tile = sc[dx:dx+256, dy:dy+256, :]
# feTile
tile2 = tile.copy()

while dMap2.shape[0] > tile2.shape[0]:
    tile2=np.vstack(( tile2, tile2 ))

while dMap2.shape[1] > tile2.shape[1]:
    tile2=np.hstack((tile2,tile2))

tile2 = tile2[0:dMap2.shape[0], 0:dMap2.shape[1], :]

#feDisplacementMap
ym, xm, dp = out.shape
for x in range(xm):
    for y in range(ym):
        crd = dMap2[y,x]
        if (crd[3] == 1):
            origX = (crd[0] - 0.5) * 255 + x
            origY = (crd[1] - 0.5) * 255 + y
            
            if (origX > 0 and origY > 0 and origX < tile2.shape[1] and origY < tile2.shape[0]):
                out[y,x] = tile2[ int(origY), int(origX) ]
#                tile2[ int(origY), int(origX) ] = 0.5 * tile2[int(origY), int(origX)]
            else:
                out[y,x] = np.array([1,0,0,1])
        else:
            out[y,x] = np.array([1,1,1,1])
                
out = out[128:,128:]

tile2[256,:] = np.matrix(np.ones(768)).T*np.matrix([1,0,0,1])
tile2[:,256] = np.matrix(np.ones(512)).T*np.matrix([1,0,0,1])
tile2[:,512] = np.matrix(np.ones(512)).T*np.matrix([1,0,0,1])
py.figure(2)
py.imshow(tile2)
py.plot( np.array(pts)[:,1,0]+256, np.array(pts)[:,1,1], 'o')

py.figure(3)
py.imshow(out)

"""


def feDisplacementMap(dMap, im, rot, dx, dy):
    dMap2 = np.zeros((dMap.shape[0]+256, dMap.shape[1]+256, 4))
    dMap2[128:dMap.shape[0]+128, 128:dMap.shape[1]+128, :] = dMap

    out = np.ones((dMap.shape[0]+128, dMap.shape[1]+128, 4))

    # input
#    im = Image.open('../fmap-relief.png')
    im = im.rotate(rot)
    sc = np.reshape( np.array(im.convert('RGBA').getdata()), ( im.size[1], im.size[0],4) )/256.0

    # feOffset
    tile = sc[dx:dx+256, dy:dy+256, :]
    # feTile
    tile2 = tile.copy()
    while dMap2.shape[0] > tile2.shape[0]:
        tile2=np.vstack(( tile2, tile2 ))

    while dMap2.shape[1] > tile2.shape[1]:
        tile2=np.hstack((tile2,tile2))

    tile2 = tile2[0:dMap2.shape[0], 0:dMap2.shape[1], :]

    #feDisplacementMap
    ym, xm, dp = out.shape
    for x in range(xm):
        for y in range(ym):
            crd = dMap2[y,x]
            if (crd[3] == 1):
                origX = (crd[0] - 0.5) * 255 + x
                origY = (crd[1] - 0.5) * 255 + y
            
                if (origX > 0 and origY > 0 and origX < tile2.shape[1] and origY < tile2.shape[0]):
                    out[y,x] = tile2[ int(origY), int(origX) ]
                else:
                    out[y,x] = np.array([1,0,0,1])
            else:
                out[y,x] = np.array([1,1,1,1])
                
    out = out[128:,128:]

    return out



out = feDisplacementMap( dMap, Image.open('../fmap.png'), 145, 100, 100)
py.figure()
py.imshow( out )

relief = feDisplacementMap( dMap, Image.open('../fmap-relief.png'), 145, 100, 100)
py.figure()
py.imshow( relief )


