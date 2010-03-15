#!/usr/bin/python

import numpy as np
import numpy.linalg as la
import pylab as py

np.set_printoptions(precision=2,threshold=2000,edgeitems=5, linewidth=150, suppress=True)

tdata = ((1,1),(1,1)),((1,2),(1,2)),((0,0),(0,0)),((4,0),(4,0))

def getHomography(pts):
    m = getA( pts )
    u,s,v = la.svd(m)
    h = v[8,:].reshape((3,3))
    
    return h/h[2,2], m, v, s, u


def getA(pts):
    m2 = None

    for pair in pts:
        ((x1,y1),(X1,Y1)) = pair

        m = np.matrix([[x1,y1,1,0,0,0,-x1*X1,-y1*X1,-X1],
                       [0,0,0,x1,y1,1,-x1*Y1,-y1*Y1,-Y1]
                       ])
        if m2 is None:
            m2 = m
        else:
            m2 = np.vstack((m2,m))

    return m2




def disp(pts):
    py.figure(1)
    m = np.array(pts)
    
    py.hold('on')
    py.subplot(211)
    py.plot(m[:,0,0],m[:,0,1],'o')
    py.subplot(212)
    py.plot(m[:,1,0],m[:,1,1],'o')

if __name__ == "__main__":

    maxx = 512
    maxy = 256

    p0 = ((0,0),(0,0))
    p1 = ((maxx,0),(256,0))
    p2 = ((0,maxy),(100,256))
    p3 = ((maxx,maxy),(156,256))
    
    pts = (p0,p1,p2,p3)
    h = getHomography(pts)
    h=h[0]
    
    dmap = np.zeros((maxy,maxx,4))
    ym, xm, dm = dmap.shape
    for x in range(xm):
        for y in range(ym):
            dest = h*np.matrix([[x,y,1]]).T
            dest = dest.T.tolist()[0]
            dmap[y,x] = np.array([dest[0]/dest[2], dest[1]/dest[2], 0, 255.0]) / 255.0
    
    py.imshow(dmap)



