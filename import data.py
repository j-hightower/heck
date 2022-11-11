toolpathdata = []
executed_distance_traveled = {}
too_being_cut_with = str()

with open('Test Data.txt') as raw_data:
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

for data_line_index, data_in_data_line in enumerate(toolpathdata):
    def segment(data_line_index, data_in_data_line, new_cut_index_number, tool_being_cut_with):
        if data_line_index >= new_cut_index_number + 2 and "Segment" in data_in_data_line[0]:
            x1 = float(data_in_data_line[1])
            y1 = float(data_in_data_line[2])
            z1 = float(data_in_data_line[3])
            xo = float(toolpathdata[data_line_index - 1][1])
            yo = float(toolpathdata[data_line_index - 1][2])
            zo = float(toolpathdata[data_line_index - 1][3])
            segment_return = (((xo - x1) ** 2) + ((yo - y1) ** 2) + ((zo - z1) ** 2)) ** 0.5
            executed_distance_traveled[tool_being_cut_with] += segment_return
    def arc(data_line_index, data_in_data_line, new_cut_index_number, tool_being_cut_with):
        if data_line_index >= new_cut_index_number + 2 and "Arc" in data_in_data_line[0]:
            xend = float(data_in_data_line[1])
            yend = float(data_in_data_line[2])
            xcent = float(data_in_data_line[4])
            ycent = float(data_in_data_line[5])
            arc_radius = (((xend - xcent) ** 2) + ((yend - ycent) ** 2)) ** 0.5
            arc_length = (3.141592 * arc_radius) / 2
            executed_distance_traveled[tool_being_cut_with] += arc_length
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
print(executed_distance_traveled)
