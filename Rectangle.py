import numpy as np

class Rectangle(object):

    # Initiate a class from x,y,l,w, information
    def __init__(self, x, y, l, w, theta = 0):
        # load the variables
        self.x = x
        self.y = y
        self.l = l
        self.w = w
        self.theta = theta
        # calculate the points from the x,y,l,w,theta information
        self.pts = np.array([[x + w / 2, y + l / 2], [x + w / 2, y - l / 2],
                            [x - w / 2, y - l / 2], [x - w / 2, y + l / 2]])
        # rotate the points to the given the    ta
        self.rotate_to(theta)

    # returns the points
    def get_pts(self):
        return self.pts

    # moves the rectangle by given values
    def move_by(self, delta_x, delta_y):
        delta = np.array([delta_x, delta_y])
        self.x += delta_x
        self.y += delta_y
        self.pts += delta

    # moves the rectangle to given coordinates
    def move_to(self, x, y):
        self.x = x
        self.y = y
        self.pts = self.pts - np.apply_along_axis(np.mean, 0, self.pts) + np.array([x, y])

    # moves the rectangle a certain amount in the direction of heading
    def move_forwards(self, amt):
        amt_vec = np.array([0, amt])
        mv_vec = self.rotate_internal(amt_vec, self.theta, 0, 0)
        self.move_by(mv_vec[0], mv_vec[1])

    # rotate the rectangle to a given theta
    def rotate_to(self, theta):
        self.pts = self.rotate_internal(self.pts, theta=theta - self.theta, x=self.x, y=self.y)
        self.theta = theta % 360

    # rotate the rectanlge by a given theta
    def rotate_by(self, theta):
        self.pts = self.rotate_internal(self.pts, theta=theta, x=self.x, y=self.y)
        self.theta = (self.theta + theta) % 360

    # rotate the rectangle around a given set of coordinates
    def rotate_around(self, theta, x, y):
        self.theta += theta
        self.pts = self.rotate_internal(self.pts, theta, x, y)
        mid = np.apply_along_axis(np.mean, 0, self.pts)
        self.x = mid[0]
        self.y = mid[1]

    # internal method that actually rotates the points etc. is used by the other rotate_x functions
    @staticmethod
    def rotate_internal(pts, theta, x, y):
        theta_rad = theta * np.pi / 180
        # get the average values
        middle = np.array([x, y])
        # shift to rotation point
        pts_0 = pts - middle
        # rotate by matrix
        rot_matrix = np.array([[np.cos(theta_rad), -np.sin(theta_rad)], [np.sin(theta_rad), np.cos(theta_rad)]])
        # actually rotate the pts
        pts_0_rotated = np.dot(pts_0, rot_matrix)
        # shift back to original area
        pts_rotated = pts_0_rotated + middle
        return pts_rotated

    # returns true if the current rectangle intersects with a second, given rectangle
    def intersect(self, other):
        # first check if the rectangles are close to each other, to approximate the process
        self_center = np.array([self.x, self.y])
        other_center = np.array([other.x, other.y])
        guess_dist = np.sqrt(sum((self_center - other_center)**2))
        if (guess_dist > 1.5*(self.l + other.l + self.w + other.w)):
            return False
        else:
            # using the two-axis theorem, calculate the axis
            def intersectAxis(ptsA, ptsB):
                ptsAx = ptsA[:,0]
                ptsBx = ptsB[:,0]
                ptsAy = ptsA[:,1]
                ptsBy = ptsB[:,1]

                isectx = min(ptsAx) < max(ptsBx) and max(ptsAx) > min(ptsBx)
                isecty = min(ptsAy) < max(ptsBy) and max(ptsAy) > min(ptsBy)
                return isectx and isecty

            # first rotate around p1 from self
            a = self.rotate_internal(self.pts, self.theta, self.pts[0][0], self.pts[0][1])
            b = self.rotate_internal(other.pts, self.theta, self.pts[0][0], self.pts[0][1])

            axis1 = intersectAxis(a, b)

            # then rotate around p1 from other
            a = self.rotate_internal(self.pts, other.theta, other.pts[0][0], other.pts[0][1])
            b = self.rotate_internal(other.pts, other.theta, other.pts[0][0], other.pts[0][1])

            axis2 = intersectAxis(a, b)

            return axis1 and axis2

