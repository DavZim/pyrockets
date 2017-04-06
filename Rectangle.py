import numpy as np

class Rectangle(object):

    # Initiate a class from x,y,l,w, information
    def __init__(self, x, y, l, w, theta = 0):
        # load the variables
        self.x = x
        self.y = y
        self.l = l
        self.w = w
        # calculate the points from the x,y,l,w,theta information
        self.pts = np.array([[x + w / 2, y + l / 2], [x + w / 2, y - l / 2],
                            [x - w / 2, y - l / 2], [x - w / 2, y + l / 2]])
        # rotate the points to the given the    ta
        # self.rotate_to(theta)

    # returns the points
    def get_pts(self):
        return self.pts
