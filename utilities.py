from Wells_Chris_Prob1 import Trapezoid
from Wells_Chris_Prob1 import TreeNode


# Create the initial box encompassing all the line segments
def create_bounding_box(segments):
    left_point = None
    right_point = None
    top_point = None
    bottom_point = None

    for segment in segments:
        p = segment[1]
        q = segment[2]

        # are either points left of the current leftmost point?
        if left_point is None or p[0] < left_point[0]:
            left_point = p
        if left_point is None or q[0] < left_point[0]:
            left_point = q

        # are either points right of the current rightmost point?
        if right_point is None or p[0] > right_point[0]:
            right_point = p
        if right_point is None or q[0] > right_point[0]:
            right_point = q

        # are either points below the current bottommost point?
        if bottom_point is None or p[1] < bottom_point[1]:
            bottom_point = p
        if bottom_point is None or q[1] < bottom_point[1]:
            bottom_point = q

        # are either points above the current topmost point?
        if top_point is None or p[1] > top_point[1]:
            top_point = p
        if top_point is None or q[1] > top_point[1]:
            top_point = q

    # Now create a trapezoid representing the bounding box
    top_segment = ((left_point[0], top_point[1]), (right_point[0], top_point[1]))
    bottom_segment = ((left_point[0], bottom_point[1]), (right_point[0], bottom_point[1]))
    t = Trapezoid(left_point, right_point, top_segment, bottom_segment)
    return t


# Is a point p above or below a segment s
def is_above(s, p):
    x1 = s[1][0]
    x2 = s[2][0]

    # Determine the origin (leftmost) and destination (rightmost) points in s
    if x1 < x2:
        o = s[1]
        d = s[2]
    else:
        o = s[2]
        d = s[1]

    # If determinant of this matrix > 0 p is to the left of the line going from left to right, and so is above
    det = (d[0]*p[1] - d[1]*p[0]) - (o[0]*(p[1] - d[1])) + (o[1]*(p[0] - d[0]))

    if det > 0:
        return True
    else:
        return False


# Determines if the point p1 is left of p2
def is_left(p1, p2):
    if p1[0] < p2[0]:
        return True
    else:
        return False


# Determines if the point p1 is right of p2
def is_right(p1, p2):
    if p1[0] > p2[0]:
        return True
    else:
        return False


# Updates search structure when there is 1 intersecting trapezoid
def update_one_trapezoid(t_node, segment):

    # Get the segment endpoints
    p = segment[1]
    q = segment[2]

    # Get the trapezoid from the node
    t = t_node.data

    # Create the 4 new trapezoids
    trap_a = TreeNode("outer", Trapezoid(None, p, t.top_segment, t.bottom_segment), None, None)
    trap_b = TreeNode("outer", Trapezoid(q, None, t.top_segment, t.bottom_segment), None, None)
    trap_c = TreeNode("outer", Trapezoid(p, q, None, segment), None, None)
    trap_d = TreeNode("outer", Trapezoid(p, q, segment, None), None, None)

    # Create a new subtree with the new trapezoids
    p_node = TreeNode("innerx", p, None, None)
    q_node = TreeNode("innerx", q, None, None)
    s_node = TreeNode("innery", segment, None, None)

    # Set the parent/child relationships
    p_node.left = trap_a
    p_node.right = q_node
    q_node.left = s_node
    q_node.right = trap_b
    q_node.parent = p_node
    s_node.left = trap_c
    s_node.right = trap_d
    s_node.parent = q_node

    # If the node was the root node return the created p x-node as the new root
    if t_node.parent is None:
        return p_node

    # Otherwise, set the new p node as the child of the input node's parent and return None
    else:
        parent_node = t_node.parent
        if parent_node.left == t_node:
            parent_node.left = p_node
            p_node.parent = parent_node
        if parent_node.right == t_node:
            parent_node.right = p_node
            p_node.parent = parent_node
        return None
