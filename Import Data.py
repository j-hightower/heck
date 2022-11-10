# Variables
toolpathdata = []
executed_distance_traveled = []
tool = []
executed_distance_traveled_for_existing_tool_calc = []

# increment through each line of the data and concatonate all required data into toolpathdata.
with open('Test Data') as main:
    for line in main:
        if line.startswith("CreateRoughFinish"):
            toollist = line.split("\"")
            tool = [toollist[5]]
            tool.insert(0, "Tool")
            toolpathdata.append(tool)
            # print(tool)
        elif line.startswith("AddSegment"):
            dcl = line.split("(")
            dcl1 = dcl[1].split(",")
            dcl2 = dcl1[2].split(")")
            dcl3 = dcl1[0:2]
            dcl3.append(dcl2[0])
            dcl3.insert(0, "Segment")
            toolpathdata.append(dcl3)
            # print(dcl3)
        elif line.startswith("AddArc"):
            dcl = line.split("(")
            dcl1 = dcl[1].split(",")
            dcl2 = dcl1[0:5]
            dcl2.insert(0, "Arc")
            toolpathdata.append(dcl2)
            # print(dcl2)

for x, value in enumerate(toolpathdata):
    if value[0] in executed_distance_traveled:
        existing_tool_index_number = executed_distance_traveled.index(value[0])
        if x >= 2:
            if "Segment" in value[0]:
                x1 = float(value[1])
                y1 = float(value[2])
                z1 = float(value[3])
                xo = float(toolpathdata[x - 1][1])
                yo = float(toolpathdata[x - 1][2])
                zo = float(toolpathdata[x - 1][3])
                segment_return = (((xo - x1) ** 2) + ((yo - y1) ** 2) + ((zo - z1) ** 2)) ** 0.5
                executed_distance_traveled[existing_tool_index_number + 1] += segment_return
            elif "Arc" in value[0]:
                xend = float(value[1])
                yend = float(value[2])
                xcent = float(value[3])
                ycent = float(value[4])
                arc_radius = (((xend - xcent) ** 2) + ((yend - ycent) ** 2)) ** 0.5
                arc_length = (3.141592 * arc_radius) / 2
                executed_distance_traveled[existing_tool_index_number + 1] += arc_length
    elif value[0] not in executed_distance_traveled:
        executed_distance_traveled_for_new_tool_calc = [value[0], 0.0]
        if x >=2:
            if "Segment" in value[0]:
                x1 = float(value[1])
                y1 = float(value[2])
                z1 = float(value[3])
                xo = float(toolpathdata[x - 1][1])
                yo = float(toolpathdata[x - 1][2])
                zo = float(toolpathdata[x - 1][3])
                segment_return = (((xo - x1) ** 2) + ((yo - y1) ** 2) + ((zo - z1) ** 2)) ** 0.5
                executed_distance_traveled_for_new_tool_calc[1] += segment_return
            elif "Arc" in value[0]:
                xend = float(value[1])
                yend = float(value[2])
                xcent = float(value[3])
                ycent = float(value[4])
                arc_radius = (((xend - xcent) ** 2) + ((yend - ycent) ** 2)) ** 0.5
                arc_length = (3.141592 * arc_radius) / 2
                executed_distance_traveled_for_new_tool_calc[1] += arc_length
executed_distance_traveled.append(executed_distance_traveled_for_new_tool_calc)
print(executed_distance_traveled)