# To run, use the following command. The input file should be in the same directory as the python file:
# python Wells_Chris_Prob1.py <input file name, ex. PS1_TEST_3.csv>
# The output will go to std out
import random
import sys


class InnerXNode:
    def __init__(self, endpoint, left, right):
        self.parent = None
        self.endpoint = endpoint
        self.left = left
        self.right = right


class InnerYNode:
    def __init__(self, segment, left, right):
        self.parent = None
        self.segment = segment
        self.left = left
        self.right = right


class OuterNode:
    def __init__(self, trapezoid):
        self.parent = None
        self.trapezoid = trapezoid


class Trapezoid:
    def __init__(self, left_point, right_point, top_segment, bottom_segment):
        self.left_point = left_point
        self.right_point = right_point
        self.top_segment = top_segment
        self.bottom_segment = bottom_segment

    def __str__(self):
        s = ""
        s += "Left Point: " + str(self.left_point) + "\n"
        s += "Right Point: " + str(self.right_point) + "\n"
        s += "Top Segment: " + str(self.top_segment) + "\n"
        s += "Bottom Segment: " + str(self.bottom_segment)
        return s


# Read the list of points
# Returns a list of all unique points, sorted by increasing x-coordinate
def read_input_csv(input_file):

    input_segments = []

    with open(input_file, 'r') as f:

        # a segment is a 3-item tuple including name, coord pair 1, and coord pair 2
        input_lines = f.readlines()
        for input_line in input_lines:
            split = input_line.strip().split(",")

            # create the line segment
            segment_id = split[0]
            p = (int(split[1]), int(split[2]))
            q = (int(split[3]), int(split[4]))

            # add to input segments list
            input_segments.append((segment_id, p, q))

    # Pass back the list of input segments
    return input_segments


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


# Search the tree for a particular point, returning a trapezoid
def search_for_point(search_tree, point):
    if isinstance(search_tree, OuterNode):
        return search_tree
    if isinstance(search_tree, InnerXNode):
        if point[0] < search_tree.endpoint[0]:
            return search_for_point(search_tree.left, point)
        else:
            return search_for_point(search_tree.right, point)
    if isinstance(search_tree, InnerYNode):
        diff = InnerYNode.segment[1] - InnerYNode.segment[0]
        slope = diff[1]/diff[0]
        interp_y = (point[0] - InnerYNode.segment[0][0]) * slope
        if point[1] > interp_y:
            return search_for_point(search_tree.left, point)
        else:
            return search_for_point(search_tree.right, point)


# Find a sequence of trapezoids intersected by an input segment
def follow_segment(search_tree, segment):
    p = segment[1]
    q = segment[2]
    int_trapezoids = [search_for_point(search_tree, p)]
    j = 0

    return int_trapezoids


# Creates the trapezoidal map and search structure for a list of segments
def trapezoidal_map(segments):

    # create the initial search structure and a random permutation of the segments list
    initial_bounding_box = create_bounding_box(segments)
    search_root = OuterNode(initial_bounding_box)
    random.shuffle(segments)

    for segment in segments:
        p = segment[1]
        q = segment[2]
        int_trapezoids = follow_segment(search_root, segment)

        # If there is only one trapezoid it is simple
        if len(int_trapezoids) == 1:
            t_node = int_trapezoids[0]
            t = t_node.trapezoid

            # Create a new subtree with the new trapezoids
            trap_a = OuterNode(Trapezoid(None, p, t.top_segment, t.bottom_segment))
            trap_b = OuterNode(Trapezoid(q, None, t.top_segment, t.bottom_segment))
            trap_c = OuterNode(Trapezoid(p, q, None, segment))
            trap_d = OuterNode(Trapezoid(p, q, segment, None))
            p_node = InnerXNode(p, None, None)
            q_node = InnerXNode(q, None, None)
            s_node = InnerYNode(segment, None, None)
            p_node.left = trap_a
            p_node.right = q_node
            q_node.left = s_node
            q_node.right = trap_b
            s_node.left = trap_c
            s_node.right = trap_d

            # Now replace the node in the tree
            if t_node.parent is None:
                search_root = p_node
            else:
                p = t_node.parent
                if p.left == t_node:
                    p.left = p_node
                    p_node.parent = p
                if p.right == t_node:
                    p.right = p_node
                    p_node.parent = p

        # TEMPORARY return the tree after the first segment
        return search_root


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # The input file name is the argument
    input_filename = sys.argv[1]

    # Read the edges and create a set of points, sorted by x value
    print("Reading " + input_filename + "...")
    read_input_segments = read_input_csv(input_filename)

    # Now search for point 6,4
    search_root = trapezoidal_map(read_input_segments)
    t = search_for_point(search_root, (6,4))
    print(t.trapezoid)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
