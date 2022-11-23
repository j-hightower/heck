"""
Initializes variables that are mutilated inside of different functions.
"""
toolpathdata = []
executed_distance_traveled = {}
too_being_cut_with = str()

"""
Defines the function that calculates linear distance along all straight line paths in the raw data file.
"""
def segment(data_line_index, data_in_data_line, new_cut_index_number, tool_being_cut_with):
    if data_line_index >= new_cut_index_number + 2 and "Segment" in data_in_data_line[0]:
        x1 = float(data_in_data_line[1])
        y1 = float(data_in_data_line[2])
        z1 = float(data_in_data_line[3])
        xo = float(toolpathdata[data_line_index - 1][1])
        yo = float(toolpathdata[data_line_index - 1][2])
        zo = float(toolpathdata[data_line_index - 1][3])
        if z1 != zo:
            pass_in_or_out_of_material(xo, yo, zo, x1, y1, z1, tool_being_cut_with)
        elif z1 > 0 and zo > 0:
            pass
        else:
            segment_return = (((xo - x1) ** 2) + ((yo - y1) ** 2) + ((zo - z1) ** 2)) ** 0.5
            executed_distance_traveled[tool_being_cut_with] += segment_return

"""
Defines the function that will calculate the linear distance the tool travels across an arc. As far as I know, the "AddArc2PointToToolPath" function in Maestro will only
ever draw quarter circles. this math is only applicable for quarter circles. If new types of arcs are added, either this math will need to be changed, or a new function
for the new type of arc will have to be added.
"""
def arc(data_line_index, data_in_data_line, new_cut_index_number, tool_being_cut_with):
    if data_line_index >= new_cut_index_number + 2 and "Arc" in data_in_data_line[0]:
        xend = float(data_in_data_line[1])
        yend = float(data_in_data_line[2])
        xcent = float(data_in_data_line[4])
        ycent = float(data_in_data_line[5])
        arc_radius = (((xend - xcent) ** 2) + ((yend - ycent) ** 2)) ** 0.5
        arc_length = (3.141592 * arc_radius) / 2
        executed_distance_traveled[tool_being_cut_with] += arc_length

"""
Defines the function that will calculate the linear distance when the tool physically rises into, or out of the surface of the material. If the tool is above the surface of
the material, we don't want that distance to be included in the executed_distance_traveled dictionary. This function will calculate the exact point that it reaches a
cut_depth of 0, and use the X and Y of that point to find the new distance traveled. It also excludes any tool paths in the raw data file that are entirely above the surface
of the material.
"""
def pass_in_or_out_of_material(xo, yo, zo, x1, y1, z1, tool_being_cut_with):
    start_coordinates = [xo, yo, zo]
    end_coordinates = [x1, y1, z1]
    coordinate_list_of_point_below_surface_of_material = [xo, yo, zo]
    if xo <= x1 and yo <= y1 and zo <= z1:
        start_coordinates = [x1, y1, z1]
        end_coordinates = [xo, yo, zo]
    elif z1 < 0.0:
        coordinate_list_of_point_below_surface_of_material = [x1, y1, z1]
    l = start_coordinates[0] - end_coordinates[0]
    m = start_coordinates[1] - end_coordinates[1]
    n = start_coordinates[2] - end_coordinates[2]
    z = 0.0
    x = ((l * z) - (l * start_coordinates[2]) + (n * start_coordinates[0])) / n
    y = ((m * z) - (m * start_coordinates[2]) + (n * start_coordinates[1])) / n
    segment_return = (((x - coordinate_list_of_point_below_surface_of_material[0]) ** 2) + ((y - coordinate_list_of_point_below_surface_of_material[1]) ** 2) + ((z - coordinate_list_of_point_below_surface_of_material[2]) ** 2)) ** 0.5
    executed_distance_traveled[tool_being_cut_with] += segment_return

"""
Defines the datacleaning function which cleans the raw data from a .XCS file. This file is spit out by ROUTER-CIM and is a scripting language containing instructions that Maestro than uses to generate a program.
We can use this script file to calculate executed_distance_traveled, for use in tool wear.
"""
def datacleaning(raw_data_filepath):
    with open(raw_data_filepath) as raw_data:
        for line in raw_data:
            if line.startswith("CreateRoughFinish"):
                data_clean = line.split("\"")
                data_clean_1 = [data_clean[5]]
                data_clean_1.insert(0, "Tool")
                toolpathdata.append(data_clean_1)
            elif line.startswith("AddSegment"):
                data_clean = line.split("(")
                data_clean_1 = data_clean[1].split(",")
                data_clean_2 = data_clean_1[2].split(")")
                data_clean_3 = data_clean_1[0:2]
                data_clean_3.append(data_clean_2[0])
                data_clean_3.insert(0, "Segment")
                toolpathdata.append(data_clean_3)
            elif line.startswith("AddArc"):
                data_clean = line.split("(")
                data_clean_1 = data_clean[1].split(",")
                data_clean_2 = data_clean_1[0:5]
                data_clean_2.insert(0, "Arc")
                toolpathdata.append(data_clean_2)
    return toolpathdata

"""
Performs simple logic to detect whether the program should add a new tool to the executed_distance_traveled dictionary and calculate it's distance, or simply calculate the
distance and add it to an existing tool in the executed_distance_traveled dictionary. The function blocks define linear distance calculations for a straight line and an arc.
For the straight lines, there is a seperate arithmetic function for an occurance of the tool passing into or out of the material. The distance to when cut_depth = 0 is the
only distance added to the tool's executed_distance_traveled.
"""
def distance_calculation(clean_data):
    for data_line_index, data_in_data_line in enumerate(toolpathdata):
        if data_in_data_line[0] == "Tool":
            new_cut_index_number = data_line_index
            if data_in_data_line[1] not in executed_distance_traveled.keys():
                executed_distance_traveled.setdefault(data_in_data_line[1], 0.0)
                tool_being_cut_with = data_in_data_line[1]
            elif data_in_data_line[1] in executed_distance_traveled.keys():
                tool_being_cut_with = data_in_data_line[1]
        else:
            segment(data_line_index, data_in_data_line, new_cut_index_number, tool_being_cut_with)
            arc(data_line_index, data_in_data_line, new_cut_index_number, tool_being_cut_with)
    return executed_distance_traveled
