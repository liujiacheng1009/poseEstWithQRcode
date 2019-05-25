import math
import operator
import numpy as np
import cv2

import utilities as ut
from settings import *

thresh = 80
thresh_max_value = 255
canny_thresh1 = 50
canny_thresh2 = 150

class MarkerNumError(RuntimeError):
    def __init__(self, arg):
        self.args = arg

def getVertices(contour, marker_center):
    minRect = cv2.minAreaRect(contour)
    rectVertices = cv2.boxPoints(minRect)

    dists_to_marker_center = np.zeros((4, 1))
    vertices = np.array([None] * 4)

    for P in contour:
        P = P[0]

        dists_to_rect_vertices = []
        for rectVertex in rectVertices:
            rectVertex = np.array(rectVertex)
            dists_to_rect_vertices.append(ut.distanceP2P(P, rectVertex))

        section_idx = np.argmin(dists_to_rect_vertices)

        dist_to_marker_center = ut.distanceP2P(P, marker_center)

        if dist_to_marker_center > dists_to_marker_center[section_idx]:
            dists_to_marker_center[section_idx] = dist_to_marker_center
            vertices[section_idx] = P

    return vertices


def updateVerticesOrder(vertices, marker_center, pattern_center):
    dists = []
    for i in range(len(vertices)):
        dists.append((i, abs(ut.distanceP2L(marker_center, pattern_center, vertices[i]))))

    dists = sorted(dists, key=operator.itemgetter(1))

    corner_idx = dists[0][0] if ut.distanceP2P(vertices[dists[0][0]], pattern_center) \
        > ut.distanceP2P(vertices[dists[1][0]], pattern_center) else dists[1][0]

    return np.append(vertices[corner_idx:], vertices[:corner_idx])

def detectQRcode(src):
    gray_img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.GaussianBlur(gray_img,(3,3),0)
    th, thresh_img = cv2.threshold(gray_img, thresh, thresh_max_value, cv2.THRESH_BINARY)
    canny_img = cv2.Canny(thresh_img,canny_thresh1,canny_thresh2)
    # cv2.imshow("canny",canny_img)
    # cv2.waitKey(0)
    contours, hierarchy = cv2.findContours(canny_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hierarchy = hierarchy[0]

    marker_candidate = []
    for i in range(len(hierarchy)):
        j, count=i,0
        while hierarchy[j][2] !=-1:
            j = hierarchy[j][2]
            count += 1
        if count == 5:
            marker_candidate.append(i)
    
    if len(marker_candidate)<3:
        raise MarkerNumError('Number of detected markers is less than 3')
    else:
        marker_candidate = marker_candidate[-3:]

    mass_centers = []
    for contour in contours:
        M = cv2.moments(contour)
        if M['m00'] == 0:
            mass_centers.append((0, 0))
        else:
            mass_centers.append(np.array((int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))))
    
    

    A = marker_candidate[0]
    B = marker_candidate[1]
    C = marker_candidate[2]


    # cv2.circle(src, tuple(mass_centers[A]), 15, (255,0,0), 4)
    # cv2.circle(src, tuple(mass_centers[B]), 15, (255,0,0), 4)
    # cv2.circle(src, tuple(mass_centers[C]), 15, (255,0,0), 4)
    # cv2.imshow("xx",src)
    # cv2.waitKey(0)


    AB = ut.distanceP2P(mass_centers[A], mass_centers[B])
    BC = ut.distanceP2P(mass_centers[B], mass_centers[C])
    AC = ut.distanceP2P(mass_centers[A], mass_centers[C])

#确定三个定位图案的位置
    top_left, top_right, bot_left = None, None, None
    P, Q = None, None

    if AB > BC and AB > AC:
        top_left, P, Q = C, A, B
    elif BC > AB and BC > AC:
        top_left, P, Q = A, B, C
    elif AC > AB and AC > BC:
        top_left, P, Q = B, A, C

    if np.cross(mass_centers[P]-mass_centers[top_left],mass_centers[Q]-mass_centers[top_left])<0:
        bot_left,top_right = P,Q
    else:
        bot_left,top_right = Q,P
    
#确定四个角点
    pattern_center = None
    top_left_vertices, top_right_vertices, bot_left_vertices = None, None, None

    pattern_center = np.array(((mass_centers[P][0] + mass_centers[Q][0]) // 2, \
        (mass_centers[P][1] + mass_centers[Q][1]) // 2))

    top_left_vertices = getVertices(contours[top_left], mass_centers[top_left])
    top_right_vertices = getVertices(contours[top_right], mass_centers[top_right])
    bot_left_vertices = getVertices(contours[bot_left], mass_centers[bot_left])

    top_left_vertices = updateVerticesOrder(top_left_vertices, mass_centers[top_left], pattern_center)
    top_right_vertices = updateVerticesOrder(top_right_vertices, mass_centers[top_right], pattern_center)
    bot_left_vertices = updateVerticesOrder(bot_left_vertices, mass_centers[bot_left], pattern_center)


    M1, M2 = None, None
    bot_right_corner = None

    M1 = top_right_vertices[1] if ut.distanceP2P(top_right_vertices[1], mass_centers[top_left]) \
        > ut.distanceP2P(top_right_vertices[-1], mass_centers[top_left]) else top_right_vertices[-1]
    M2 = bot_left_vertices[1] if ut.distanceP2P(bot_left_vertices[1], mass_centers[top_left]) \
        > ut.distanceP2P(bot_left_vertices[-1], mass_centers[top_left]) else bot_left_vertices[-1]

    bot_right_corner = ut.intersection(top_right_vertices[0], M1, bot_left_vertices[0], M2)

    return np.array([top_left_vertices[0], top_right_vertices[0], bot_right_corner, bot_left_vertices[0]])

