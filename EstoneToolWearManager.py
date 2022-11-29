from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
from tkinter import filedialog
import json

"""
Imports the important function from the ImportData script, so that we can call those functions in the 'perform_executed_distance_traveled_calculation' function.
"""
from ImportData import datacleaning

"""
To make this program not crash if it's opened on a computer for the first time, these lines of code generate the ToolDistanceDB.json file, if it doesn't exist. If it does exist,
it simply closes it right after opening. This way we won't have to import the dictionary of lifetime_distance_traveled anywhere else than right here. It also initializes the
dictionary lifetime_distance_traveled so that the program doesn't error out when it is called in the lifetime_distance_traveled_filehandling_and_calculation function.
"""
def boot():
    try:
        database_file_object = open('ToolDistanceDB.json')
        database_file_object.close()
    except:
        database_file_object = open('ToolDistanceDB.json', 'w')
        database_file_object.write('''
{
  "ideal_distance_traveled": {
    "E001": 10000.0,
    "E002": 10000.0,
    "E003": 10000.0,
    "E004": 10000.0,
    "E005": 10000.0,
    "E006": 10000.0,
    "E007": 10000.0,
    "E008": 10000.0,
    "E009": 10000.0,
    "E010": 10000.0,
    "E011": 10000.0,
    "E012": 10000.0,
    "E013": 10000.0,
    "E014": 10000.0,
    "E015": 10000.0,
    "E016": 10000.0,
    "E017": 10000.0,
    "E018": 10000.0,
    "E019": 10000.0
  },
  "lifetime_distance_traveled": {},
  "tool_wear": {}
}
        ''')
        database_file_object.close()

boot()

"""
Because we have raw_data_filepath set to a global variable in the 'open_raw_data_file' function, we initialize it here as a string so that other files can call it once it's
mutilated in the 'open_raw_data_file' function.
"""
raw_data_filepath = str()

"""
Defines a function that can be called to create the combined dictionaries from ToolDistanceDB.json without passing any arguments into or out of the function.
"""
def create_combined_dictionaries():
    with open('ToolDistanceDB.json') as json_file_object:
        combined_dictionaries = json.load(json_file_object)
    return combined_dictionaries

"""
Defines the function to handle updating the database anytime a function alters one of the three dictionaries in the ToolDistanceDB.json database.
"""
def update_database(dictionary, update_type):
    combined_dictionaries = create_combined_dictionaries()
    if update_type == 'lifetime':
        lifetime_distance_traveled = combined_dictionaries.get('lifetime_distance_traveled')
        lifetime_distance_traveled.update(dictionary)
        ideal_distance_traveled = combined_dictionaries.get('ideal_distance_traveled')
        tool_wear_dictionary = combined_dictionaries.get('tool_wear')
        combined_dictionaries = {'lifetime_distance_traveled': lifetime_distance_traveled, 'ideal_distance_traveled': ideal_distance_traveled, 'tool_wear': tool_wear_dictionary}
        with open('ToolDistanceDB.json', 'w') as json_file_object:
            json.dump(combined_dictionaries, json_file_object, indent=2, sort_keys=True)
    elif update_type == 'ideal':
        ideal_distance_traveled = combined_dictionaries.get('ideal_distance_traveled')
        ideal_distance_traveled.update(dictionary)
        lifetime_distance_traveled = combined_dictionaries.get('lifetime_distance_traveled')
        tool_wear_dictionary = combined_dictionaries.get('tool_wear')
        combined_dictionaries = {'lifetime_distance_traveled': lifetime_distance_traveled, 'ideal_distance_traveled': ideal_distance_traveled, 'tool_wear': tool_wear_dictionary}
        with open('ToolDistanceDB.json', 'w') as json_file_object:
            json.dump(combined_dictionaries, json_file_object, indent=2, sort_keys=True)
    elif update_type == 'tool wear':
        tool_wear_dictionary = combined_dictionaries.get('tool_wear')
        tool_wear_dictionary.update(dictionary)
        lifetime_distance_traveled = combined_dictionaries.get('lifetime_distance_traveled')
        ideal_distance_traveled = combined_dictionaries.get('ideal_distance_traveled')
        combined_dictionaries = {'lifetime_distance_traveled': lifetime_distance_traveled, 'ideal_distance_traveled': ideal_distance_traveled, 'tool_wear': tool_wear_dictionary}
        with open('ToolDistanceDB.json', 'w') as json_file_object:
            json.dump(combined_dictionaries, json_file_object, indent=2, sort_keys=True)

"""
Defines the function for handling the ToolDistanceDB file. My plan for this function is to create a ToolDistanceDB.estone file for referencing lifetime_distance_traveled, and
ideal_distance_traveled. It should also create a window to show the user what the calculated executed_distance_traveled is, according to the distance calculation they ran on
the selected raw data file. It should also append the dictionary of lifetime_distance_traveled. We will have to figure out how to overwrite the existing
lifetime_distance_traveled dictionary without using the 'w' method, because this file will also store the dictionary for ideal distance traveled. In this blocks current state,
it will delete all of the contents of ToolDistanceDB.py, and then write ONLY the lifetime_distance_traveled dictionary to it.
"""
def lifetime_distance_traveled_calculation(executed_distance_traveled):
    combined_dictionaries = create_combined_dictionaries()
    lifetime_distance_traveled = combined_dictionaries.get('lifetime_distance_traveled')
    for tool in executed_distance_traveled:
        if tool not in lifetime_distance_traveled.keys():
            lifetime_distance_traveled.setdefault(tool, executed_distance_traveled.get(tool))
        else:
            tool_distance_from_raw_data = executed_distance_traveled.get(tool)
            tool_distance_from_database = lifetime_distance_traveled.get(tool)
            new_incremented_tool_distance = tool_distance_from_raw_data + tool_distance_from_database
            temporary_iterable_dictionary = {tool:new_incremented_tool_distance}
            lifetime_distance_traveled.update(temporary_iterable_dictionary)
    tool_wear_calculation(lifetime_distance_traveled)
    acknowledge_window_for_running_importdata_script(executed_distance_traveled, lifetime_distance_traveled)

"""
Defines the function that calculates tool_wear as a ratio between lifetime_distance_traveled and ideal_distance_traveled
"""
def tool_wear_calculation(dictionary):
    combined_dictionaries = create_combined_dictionaries()
    ideal_distance_traveled = combined_dictionaries.get('ideal_distance_traveled')
    tool_wear_dictionary = combined_dictionaries.get('tool_wear')
    update_type = 'tool wear'
    for tool in dictionary:
        tool_wear_ratio = dictionary.get(tool) / ideal_distance_traveled.get(tool)
        temporary_iterable_dictionary = {tool:tool_wear_ratio}
        tool_wear_dictionary.update(temporary_iterable_dictionary)
    update_database(tool_wear_dictionary, update_type)
    return tool_wear_dictionary

"""
The message box for clearing a tool's lifetime distance traveled for an individual tool when the operator changed the tool.
"""
def executed_tool_change(choose_tool):
    if choose_tool.get() == 'Select tool...':
        messagebox.showerror('Executed Tool Change', 'No tool selected!')
    else:
        response = messagebox.askokcancel("Executed Tool Change", "Was " + str(choose_tool.get()) + " replaced with new parts?")
        if response == 1:
            messagebox.showinfo("Executed Tool Change", str(choose_tool.get()) + "\'s Lifetime Distance Traveled was updated to 0.0 ft.")
            combined_dictionaries = create_combined_dictionaries()
            lifetime_distance_traveled = combined_dictionaries.get('lifetime_distance_traveled')
            temporary_iterable_dictionary = {choose_tool.get():0.0}
            lifetime_distance_traveled.update(temporary_iterable_dictionary)
            update_type = 'lifetime'
            update_database(lifetime_distance_traveled, update_type)
            tool_wear_calculation(lifetime_distance_traveled)
            choose_tool_dropdown_menu(choose_tool)
        else:
            pass

"""
The message box for calculating executed_distance_traveled and updating lifetime distance traveled based on a program that was executed when the operator clicks the "Calculate
Executed Distance Traveled button".
"""
def calculate_executed_distance_traveled(raw_data_filepath):
    response = messagebox.askokcancel("Calculate Lifetime Distance Traveled", "Are you sure you want to update the Lifetime Distance Traveled according to the program currently being cut on the m600f?")
    if response == 1:
        try:
            raw_data_file = open(raw_data_filepath)
            raw_data_file.close()
            executed_distance_traveled = (datacleaning(raw_data_filepath))
            lifetime_distance_traveled_calculation(executed_distance_traveled)
        except Exception as e:
            messagebox.showerror('Calculate Executed Distance Traveled', 'Invalid or no file selected to use for calculation!')
            print(e)

"""
The message box for updating ideal distance traveled for an individual tool.
"""
def update_ideal_distance_traveled(choose_tool):
    if choose_tool.get() == "Select tool...":
        messagebox.showerror('Update Ideal Distance Traveled', "No tool selected!")
    else:
        response = messagebox.askokcancel('Update Ideal Distance Traveled', "Are you sure you want to update the Ideal Distance Traveled for tool " + str(choose_tool.get()) + ' ?')
        ideal_distance_traveled_manager(response, choose_tool)

"""
Opens a new window if the user wishes to update the Ideal distance traveled for an individual tool.
"""
def ideal_distance_traveled_manager(response, choose_tool):
    if response == 1:
        ideal_distance_traveled_manager_window = Toplevel(root)
        ideal_distance_traveled_manager_window.title('Update Ideal Distance Traveled for tool ' + str(choose_tool.get()))
        info_label = Label(ideal_distance_traveled_manager_window, text="Enter New Ideal Distance Traveled for tool " + str(choose_tool.get()) + " in feet (ft)", bd=3, anchor=CENTER)
        info_label.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky=W+E)
        new_ideal_distance_traveled_entry_field = Entry(ideal_distance_traveled_manager_window, width=50, relief=SUNKEN, bd=3)
        new_ideal_distance_traveled_entry_field.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky=W+E)
        close_button = Button(ideal_distance_traveled_manager_window, text='Cancel', command=ideal_distance_traveled_manager_window.destroy)
        update_button = Button(ideal_distance_traveled_manager_window, text='Update', command=lambda: change_ideal_distance_traveled(new_ideal_distance_traveled_entry_field, choose_tool, response, ideal_distance_traveled_manager_window))
        close_button.grid(row=2, column=0, padx=5, pady=5)
        update_button.grid(row=2, column=4, padx=5, pady=5)

"""
Performs the change of the dictionary of ideal_distance_traveled.
"""
def change_ideal_distance_traveled(new_ideal_distance_traveled_entry_field, choose_tool, response, ideal_distance_traveled_manager_window):
    combined_dictionaries = create_combined_dictionaries()
    lifetime_distance_traveled = combined_dictionaries.get('lifetime_distance_traveled')
    ideal_distance_traveled = combined_dictionaries.get('ideal_distance_traveled')
    compare_data_type_of_new_ideal_distance_traveled_entry_field = StringVar()
    compare_data_type_of_new_ideal_distance_traveled_entry_field.set(new_ideal_distance_traveled_entry_field.get())
    try:
        new_ideal_distance_traveled_for_selected_tool = float(compare_data_type_of_new_ideal_distance_traveled_entry_field.get())
        temporary_iterable_dictionary = {choose_tool.get():new_ideal_distance_traveled_for_selected_tool}
        ideal_distance_traveled.update(temporary_iterable_dictionary)
        update_type = 'ideal'
        update_database(ideal_distance_traveled, update_type)
        tool_wear_calculation(lifetime_distance_traveled)
        choose_tool_dropdown_menu(choose_tool)
        ideal_distance_traveled_manager_window.destroy()
    except Exception as e:
        messagebox.showerror('Update Ideal Distance Traveled', "The entry " + str(new_ideal_distance_traveled_entry_field.get()) + " is not a valid input!")
        ideal_distance_traveled_manager_window.destroy()
        print(e)

"""
The place where the user picks the raw data to use for calculating executed_distance_traveled. This function also updates the label label_for_the_selected_raw_data_file_directory with the file directory that was selected.
"""
def open_raw_data_file(label_for_the_selected_raw_data_file_directory):
    root.filename = filedialog.askopenfilename(initialdir='C:/Users', title='Select a file... ', filetypes=(("XCS files", "*.xcs"),("All file types", "*.*")))
    global raw_data_filepath
    raw_data_filepath = root.filename
    label_for_the_selected_raw_data_file_directory.destroy
    label_for_the_selected_raw_data_file_directory = Label(import_data_frame, text=root.filename, padx=5, pady=5, bd=3, relief=SUNKEN, anchor=E, width=50, height=2)
    label_for_the_selected_raw_data_file_directory.grid(row=0, column=1)

"""
The 'acknowledge_window' function is the operator's visual queue of the output taken from ImportData.py. It includes that output, the current distance in the database, and the distance
that will be entered into the database if the operator clicks 'acknowledge'. The 'update_destroy' function simply calls the update_database function and destroys the acknowledge window.
This function exists simply so that the 'update_database' function will never need more than two positional arguements.
"""
def acknowledge_window_for_running_importdata_script(executed_distance_traveled, lifetime_distance_traveled):
    combined_dictionaries = create_combined_dictionaries()
    acknowledgement_window_for_running_importdata_script = Toplevel(root)
    acknowledgement_window_for_running_importdata_script.title('Estone CNC Tool Wear Manager')
    database_lifetime_distance_traveled = combined_dictionaries.get('lifetime_distance_traveled')
    database_lifetime_distance_traveled_frame = LabelFrame(acknowledgement_window_for_running_importdata_script, text='Distance from Database', padx=10, pady=10, bd=5)
    database_lifetime_distance_traveled_frame.grid(row=0, column=1)
    updated_lifetime_distance_traveled = lifetime_distance_traveled
    updated_lifetime_distance_traveled_frame = LabelFrame(acknowledgement_window_for_running_importdata_script, text='New Distance after Update, and Tool Wear.', padx=10, pady=10, bd=5)
    updated_lifetime_distance_traveled_frame.grid(row=0, column=2)
    executed_distance_traveled_frame = LabelFrame(acknowledgement_window_for_running_importdata_script, text='Executed Distance from Raw Data', padx=10, pady=10, bd=5)
    executed_distance_traveled_frame.grid(row=0, column=0)
    tool_wear_dictionary = combined_dictionaries.get('tool_wear')
    row_number = {}
    xiter = 0
    update_type = 'lifetime'
    for tool in updated_lifetime_distance_traveled:
        xiter += 1
        temporary_iterable_dictionary = {tool:xiter}
        row_number.update(temporary_iterable_dictionary)
    for tool in executed_distance_traveled:
        string = str(executed_distance_traveled.get(tool))
        truncated_string = string[:string.find('.') + 3]
        label = Label(executed_distance_traveled_frame, text=str(tool) + ' : ' + truncated_string + ' ft.', padx=2, pady=2, bd=1, anchor=CENTER, height=2, width=30)
        label.grid(row=row_number.get(tool), column=0)
    if len(database_lifetime_distance_traveled) == 0:
        for tool in updated_lifetime_distance_traveled:
            label = Label(database_lifetime_distance_traveled_frame, text=str(tool) + ' : ' + '0.00 ft.', padx=2, pady=2, bd=1, anchor=CENTER, height=2, width=30)
            label.grid(row=row_number.get(tool), column=1)
    elif len(database_lifetime_distance_traveled) >= 1:
        for tool in database_lifetime_distance_traveled:
            string = str(database_lifetime_distance_traveled.get(tool))
            truncated_string = string[:string.find('.') + 3]
            label = Label(database_lifetime_distance_traveled_frame, text=str(tool) + ' : ' + truncated_string + ' ft.', padx=2, pady=2, bd=1, anchor=CENTER, height=2, width=30)
            label.grid(row=row_number.get(tool), column=1)
    for tool in updated_lifetime_distance_traveled:
        string = str(updated_lifetime_distance_traveled.get(tool))
        truncated_string = string[:string.find('.') + 3]
        percentage = tool_wear_dictionary.get(tool) * 100
        string2 = str(percentage)
        truncated_string2 = str(string2[:3])
        label = Label(updated_lifetime_distance_traveled_frame, text=str(tool) + ' : ' + truncated_string + ' ft. : ' + truncated_string2 + ' %', padx=2, pady=2, bd=1, anchor=CENTER, height=2, width=40)
        label.grid(row=row_number.get(tool), column=2)
    final_row_number = len(row_number) + 1
    cancel_button = Button(acknowledgement_window_for_running_importdata_script, text='Cancel', padx=5, pady=5, bd=2, command=acknowledgement_window_for_running_importdata_script.destroy)
    cancel_button.grid(column=0, row=final_row_number)
    acknowledge_button = Button(acknowledgement_window_for_running_importdata_script, text='Acknowledge', padx=5, pady=5, bd=2, command=lambda: update_and_destroy(updated_lifetime_distance_traveled, update_type, acknowledgement_window_for_running_importdata_script))
    acknowledge_button.grid(column=2, row=final_row_number)
    acknowledgement_window_for_running_importdata_script.mainloop()

def update_and_destroy(updated_lifetime_distance_traveled, update_type, acknowledgement_window_for_running_importdata_script):
    acknowledgement_window_for_running_importdata_script.destroy()
    update_database(updated_lifetime_distance_traveled, update_type)

"""
'choose_tool_dropdown_menu' and 'create_text_for_label' are the two functions that populate the labels shown in the tool_wear_manager_display_frame. The purpose of the
'choose_tool_dropdown_menu' function is to define the labels, and place them on the screen. 'choose_tool_dropdown_menu' is only called when the operator selects a choice in the OptionMenu
'select_tool'. The 'create_text_for_label' function defines the text that will be populated in each label. Currently, do to the restraints with tkinter's label widgets, loops, or a mix of
both of those factors and a lack of knowledge on my part, the labels are simply laid on top of one another. There could be an instance when an operator populates too many of these widgets
and the program could crash, but because of how often the program updates the database, it shouldn't be too big of an issue if this ever does happen. Unfortunately, because functions in
this GUI are either vanilla python functions or tkinter "Callbacks," the data type of 'choose_tool' changes between a 'str' clas and a 'tkinter.string'. When 'choose_tool' is a
'tkinter.string' class object, it must be fetched with the .get() method, which is not applicable to the python 'str' class. Thus, an if statement is called to check the data type of
'choose_tool,' and points the function to handle the string manipulation and concatonation accordingly.
"""
def choose_tool_dropdown_menu(choose_tool):
    label_text = create_text_for_label(choose_tool)
    tool_info_label_tool = Label(tool_wear_manager_display_frame, text=label_text[0], padx=5, pady=5, anchor=CENTER)
    tool_info_label_lifetime_distance = Label(tool_wear_manager_display_frame, text=label_text[1], padx=5, pady=5, anchor=CENTER, width=30)
    tool_info_label_ideal_distance = Label(tool_wear_manager_display_frame, text=label_text[2], padx=5, pady=5, anchor=CENTER, width=30)
    tool_info_label_tool_wear = Label(tool_wear_manager_display_frame, text=label_text[3], padx=5, pady=5, anchor=CENTER, width=30)
    tool_info_label_tool.grid(row=0, column=0, columnspan=3, ipady=2)
    tool_info_label_lifetime_distance.grid(row=1, column=0, padx=5, pady=2, ipadx=10, ipady=2)
    tool_info_label_ideal_distance.grid(row=1, column=1, padx=5, pady=2, ipadx=10, ipady=2)
    tool_info_label_tool_wear.grid(row=1, column=2, padx=5, pady=2, ipadx=10, ipady=2)

def create_text_for_label(choose_tool):
    string_comparator = str()
    tkinter_string_comparator = StringVar()
    label_text = []
    combined_dictionaries = create_combined_dictionaries()
    lifetime_distance_traveled = combined_dictionaries.get('lifetime_distance_traveled')
    ideal_distance_traveled = combined_dictionaries.get('ideal_distance_traveled')
    tool_wear_dictionary = combined_dictionaries.get('tool_wear')
    if type(choose_tool) == type(string_comparator):
        label_text.append(choose_tool)
        if choose_tool not in lifetime_distance_traveled.keys():
            label_text.append(' ')
        else:
            lifetime_distance_for_tool = str(lifetime_distance_traveled.get(choose_tool)) + ' ft.'
            lifetime_distance_for_tool_truncated = lifetime_distance_for_tool[:lifetime_distance_for_tool.find('.') + 3]
            label_text.append('Lifetime Distance Traveled for ' + choose_tool + ' : ' + lifetime_distance_for_tool_truncated)
        if choose_tool not in ideal_distance_traveled.keys():
            label_text.append(' ')
        else:
            ideal_distance_for_tool = str(ideal_distance_traveled.get(choose_tool)) + ' ft.'
            label_text.append('Ideal Distance Traveled for ' + choose_tool + ' : ' + ideal_distance_for_tool)
        if choose_tool not in tool_wear_dictionary.keys():
            label_text.append(' ')
        else:
            tool_wear_percentage = tool_wear_dictionary.get(choose_tool) * 100
            tool_wear_percentage_string = str(tool_wear_percentage)
            tool_wear_percentage_truncated_string = tool_wear_percentage_string[:3]  + ' %'
            label_text.append('Tool Wear percentage for' + choose_tool + ' : ' + tool_wear_percentage_truncated_string)
        return label_text
    else:
        label_text.append(choose_tool.get())
        if choose_tool.get() not in lifetime_distance_traveled.keys():
            label_text.append(' ')
        else:
            lifetime_distance_for_tool = str(lifetime_distance_traveled.get(choose_tool.get())) + ' ft.'
            lifetime_distance_for_tool_truncated = lifetime_distance_for_tool[:lifetime_distance_for_tool.find('.') + 3]
            label_text.append('Lifetime Distance Traveled for ' + choose_tool.get() + ' : ' + lifetime_distance_for_tool_truncated)
        if choose_tool.get() not in ideal_distance_traveled.keys():
            label_text.append(' ')
        else:
            ideal_distance_for_tool = str(ideal_distance_traveled.get(choose_tool.get())) + ' ft.'
            label_text.append('Ideal Distance Traveled for ' + choose_tool.get() + ' : ' + ideal_distance_for_tool)
        if choose_tool.get() not in tool_wear_dictionary.keys():
            label_text.append(' ')
        else:
            tool_wear_percentage = tool_wear_dictionary.get(choose_tool.get()) * 100
            tool_wear_percentage_string = str(tool_wear_percentage)
            tool_wear_percentage_truncated_string = tool_wear_percentage_string[:3]  + ' %'
            label_text.append('Tool Wear percentage for' + choose_tool.get() + ' : ' + tool_wear_percentage_truncated_string)
        return label_text

"""
Defines the major window that the program will run in.
"""
root = Tk()

"""
Trying to set a default window size for the tool manager program, but it's giving me gruff while dealing with the grid method of displaying all of the widgets assosciated
with the GUI. It's commented out for now.
"""
# root.geometry("900x600")

"""
Gives a title to the program
"""
root.title('Estone CNC Tool Wear Manager')

"""
Gives the program an Icon. Right now it will be commented out because I haven't made an Icon for it.
"""
# root.iconbitmap('Insert directory for icon here')

"""
Initializes the tkinter variable for our choose_tool dropdown menu.
"""
choose_tool = StringVar()
choose_tool.set("Select tool...")
"""
Eventually, we'll set the options for this dropdown equal to the keys of the executed_distance_traveled dictionary as follows. Make sure there's an asterisk (*) after the list
name.
"""

"""
This is the visual layout of the GUI. We want four frames. The import data frame, The calculate executed_distance_traveled frame, the tool wear manager frame, and the frame
that will display the actual tool wear (As a ratio of executed_distance_traveled and lifetime_distance_traveled).
"""
import_data_frame = LabelFrame(root, text="Import Data", padx=10, pady=10, bd=3)
import_data_frame.grid(row=0, column=0, sticky=N+S+E+W)
import_data_frame.columnconfigure(0, weight=1, pad=10)
import_data_frame.rowconfigure(0, weight=1, pad=10)
calculate_executed_distance_traveled_frame = LabelFrame(root, text="Calculate Executed Distance Traveled", padx=10, pady=10, bd=3)
calculate_executed_distance_traveled_frame.grid(row=1, column=0, sticky=N+S+E+W)
calculate_executed_distance_traveled_frame.columnconfigure(0, weight=1, pad=10)
calculate_executed_distance_traveled_frame.rowconfigure(0, weight=1, pad=10)
tool_wear_manager_frame = LabelFrame(root, text="Tool Wear Manager", padx=5, pady=5, bd=3)
tool_wear_manager_frame.grid(row=0, column=1, rowspan=2, sticky=N+S+E+W)
tool_wear_manager_frame.columnconfigure(0, weight=1, pad=10)
tool_wear_manager_frame.rowconfigure(0, weight=1, pad=10)
tool_wear_manager_display_frame = LabelFrame(tool_wear_manager_frame, padx=5, pady=5)
tool_wear_manager_display_frame.grid(row=0, column=0, columnspan=3, sticky=N+S+E+W)
tool_wear_manager_display_frame.columnconfigure(0, weight=1, pad=10)
tool_wear_manager_display_frame.rowconfigure(0, weight=1, pad=10)

"""
Defines and inserts the button to clear the executed_distance_traveled when the operator changes the selected tool in the tool selection drop down menu.
"""
button_that_clears_lifetime_distance_traveled = Button(tool_wear_manager_frame, text="Executed Tool Change", command=lambda: executed_tool_change(choose_tool), padx=5, pady=5)
button_that_clears_lifetime_distance_traveled.grid(row=1, column=1, padx=5, pady=5)

"""
Defines the button that actually calculates the executed_distance_traveled for a given file chosen in the import_data file dialogue box.
"""
button_that_calculates_executed_distance_traveled = Button(calculate_executed_distance_traveled_frame, text="Calculate Executed Distance Traveled", command=lambda: calculate_executed_distance_traveled(raw_data_filepath), padx=5, pady=5)
button_that_calculates_executed_distance_traveled.pack()

"""
Defines the button that will allow the operator to set a new Lifetime Distance Traveled for an individual tool.
"""
button_that_updates_ideal_distance_traveled = Button(tool_wear_manager_frame, text='Update Ideal Distance Traveled', command=lambda: update_ideal_distance_traveled(choose_tool), padx=5, pady=5)
button_that_updates_ideal_distance_traveled.grid(row=1, column=2, padx=5, pady=5)

"""
Allows the operator to select the raw data file that will be used for calculating executed distance traveled. Also provides a label to show the operator what the filepath
that was selected is.
"""
button_that_opens_file_explorer_for_raw_data = Button(import_data_frame, text='Import Raw Data... ', command=lambda: open_raw_data_file(label_for_the_selected_raw_data_file_directory), padx=5, pady=5)
button_that_opens_file_explorer_for_raw_data.grid(row=0, column=0)
label_for_the_selected_raw_data_file_directory = Label(import_data_frame, padx=5, pady=5, bd=3, relief=SUNKEN, anchor=E, width=50, height=2)
label_for_the_selected_raw_data_file_directory.grid(row=0, column=1)

"""
Defines the tool selection drop down menu.
"""
tool_selection = OptionMenu(tool_wear_manager_frame, choose_tool, 'E001', 'E002', 'E003', 'E004', 'E005', 'E006', 'E007', 'E008', 'E009', 'E010', 'E011', 'E012', 'E013', 'E014', 'E015', 'E016', 'E017', 'E018', command=choose_tool_dropdown_menu)
tool_selection.grid(row=1, column=0, padx=5, pady=5, ipady=3, ipadx=20, sticky=N+S+E+W)

"""
The function that loops the program until an operator exits the program.
"""
root.mainloop()
