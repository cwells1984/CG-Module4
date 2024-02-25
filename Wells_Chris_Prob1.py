# To run, use the following command. The input file should be in the same directory as the python file:
# python Wells_Chris_Prob1.py <input file name, ex. PS1_TEST_3.csv>
# The output will go to std out
import random
import sys
import utilities


class TreeNode:
    def __init__(self, type, data, left, right):
        self.type = type
        self.data = data
        self.left = left
        self.right = right


class Trapezoid:
    def __init__(self, left_point, right_point, top_segment, bottom_segment, search_node):
        self.left_point = left_point
        self.right_point = right_point
        self.top_segment = top_segment
        self.bottom_segment = bottom_segment
        self.search_node = search_node
        self.lr_neighbor = None
        self.ur_neighbor = None

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


# Search the tree for a particular point, returning a trapezoid
def search_for_point(search_tree, point):

    # If we have reached an outer node, return it
    if search_tree.type == "outer":
        return search_tree.data

    # If we have reached an inner x node, go left if the point is left of the node's endpoint
    if search_tree.type == "innerx":
        if utilities.is_left(point, search_tree.data):
            return search_for_point(search_tree.left, point)
        else:
            return search_for_point(search_tree.right, point)

    # if we have reached an inner y node, go left if the point is above the node's segment
    if search_tree.type == "innery":
        if utilities.is_above(search_tree.data, point):
            return search_for_point(search_tree.left, point)
        else:
            return search_for_point(search_tree.right, point)


# Find a sequence of trapezoids intersected by an input segment
def follow_segment(search_tree, segment):
    p = segment[1]
    q = segment[2]
    int_trapezoids = [search_for_point(search_tree, p)]
    j = 0

    prev_trapezoid = int_trapezoids[0]
    while utilities.is_right(q, prev_trapezoid.right_point) is True:
        if utilities.is_above(segment, prev_trapezoid.right_point):
            new_trapezoid = Trapezoid(prev_trapezoid.right_point, q, None, segment, None)
            prev_trapezoid.lr_neighbor = new_trapezoid
            int_trapezoids.append(new_trapezoid)
            prev_trapezoid = new_trapezoid
        else:
            new_trapezoid = Trapezoid(prev_trapezoid.right_point, q, segment, None, None)
            prev_trapezoid.ur_neighbor = new_trapezoid
            int_trapezoids.append(new_trapezoid)
            prev_trapezoid = new_trapezoid
        j += 1

    return int_trapezoids


# Creates the trapezoidal map and search structure for a list of segments
def trapezoidal_map(segments):

    # create the initial search structure and a random permutation of the segments list
    initial_bounding_box = utilities.create_bounding_box(segments)
    search_root = TreeNode("outer", initial_bounding_box, None, None)
    initial_bounding_box.search_node = search_root
    #random.shuffle(segments)

    for segment in segments:

        int_trapezoids = follow_segment(search_root, segment)

        # If there is only one trapezoid it is simple
        if len(int_trapezoids) == 1:
            new_root = utilities.update_one_trapezoid(int_trapezoids[0], segment)
            search_root = new_root

        if len(int_trapezoids) > 1:
            print("Intersected multiple trapezoids")

    # return the top node of the search structure
    return search_root


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # The input file name is the argument
    input_filename = sys.argv[1]

    # Read the edges and create a set of points, sorted by x value
    print("Reading " + input_filename + "...")
    read_input_segments = read_input_csv(input_filename)

    # Now search for point 6,4
    search_tree_root = trapezoidal_map(read_input_segments)
    t = search_for_point(search_tree_root, (2,2))
    print("Point (2,2) is located in the trapezoid at:")
    print(t)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
