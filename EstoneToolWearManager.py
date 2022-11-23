from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
from tkinter import filedialog

"""
Because we have raw_data_filepath set to a global variable in the 'open_raw_data_file' function, we initialize it here as a string so that other files can call it once it's
mutilated in the 'open_raw_data_file' function.
"""
raw_data_filepath = str()

"""
Imports the important functions from the ImportData script, so that we can call those functions in the 'perform_executed_distance_traveled_calculation' function.
"""
from ImportData import datacleaning, distance_calculation

"""
Defines the function for calculating the executed_distance_traveled based on a program executed on the m600f.
"""
def perform_executed_distance_traveled_calculation(raw_data_filepath):
    try:
        open(raw_data_filepath)
        clean_data = datacleaning(raw_data_filepath)
        distance = distance_calculation(clean_data)
        print(distance)
    except Exception as e:
        messagebox.showerror('Calculate Executed Distance Traveled', 'Invalid or no file selected to use for calculation!')
        print(e)

"""
The message box for clearing a tool's executed distance traveled for an individual tool when the operator changed the tool.
"""
def executed_tool_change(choose_tool):
    if choose_tool.get() == 'Select tool...':
        messagebox.showerror('Executed Tool Change', 'No tool selected!')
    else:
        response = messagebox.askokcancel("Executed Tool Change", "Was " + str(choose_tool.get()) + " replaced with new parts?")
        if response == 1:
            messagebox.showinfo("Executed Tool Change", str(choose_tool.get()) + "\'s Executed Distance Traveled was updated to 0.0 ft.")
        else:
            pass
"""
The message box for updating executed distance traveled based on a program that was executed.
"""
def update_executed_distance_traveled(raw_data_file):
    response = messagebox.askokcancel("Update Executed Distance Traveled", "Are you sure you want to update the Execute Distance Traveled according to the program currently being cut on the m600f?")
    if response == 1:
        perform_executed_distance_traveled_calculation(raw_data_file)


"""
The message box for updating lifetime distance traveled for an individual tool.
"""
def update_lifetime_distance_traveled(choose_tool):
    if choose_tool.get() == "Select tool...":
        messagebox.showerror('Update Lifetime Distance Traveled', "No tool selected!")
    else:
        response = messagebox.askokcancel('Update Lifetime Distance Traveled', "Are you sure you want to update the Lifetime Distance Traveled for tool " + str(choose_tool.get()) + ' ?')
        lifetime_distance_traveled_manager(response, choose_tool)

"""
Opens a new window if the user wishes to update the lifetime distance traveled for an individual tool.
"""
def lifetime_distance_traveled_manager(response, choose_tool):
    if response == 1:
        lifetime_distance_traveled_manager_window = Toplevel(root)
        lifetime_distance_traveled_manager_window.title('Update Lifetime Distance Traveled for tool ' + str(choose_tool.get()))
        info_label = Label(lifetime_distance_traveled_manager_window, text="Enter New Lifetime Distance Traveled for tool " + str(choose_tool.get()) + " in feet (ft)", bd=3, anchor=CENTER)
        info_label.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky=W+E)
        new_lifetime_distance_traveled_entry_field = Entry(lifetime_distance_traveled_manager_window, width=50, relief=SUNKEN, bd=3)
        new_lifetime_distance_traveled_entry_field.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky=W+E)
        close_button = Button(lifetime_distance_traveled_manager_window, text='Cancel', command=lifetime_distance_traveled_manager_window.destroy)
        update_button = Button(lifetime_distance_traveled_manager_window, text='Update', command=lambda: change_lifetime_distance_traveled(new_lifetime_distance_traveled_entry_field, choose_tool, response, lifetime_distance_traveled_manager_window))
        close_button.grid(row=2, column=1, padx=5, pady=5)
        update_button.grid(row=2, column=4, padx=5, pady=5)
"""
Performs the change of the dictionary of lifetime_distance_traveled.
"""
def change_lifetime_distance_traveled(new_lifetime_distance_traveled_entry_field, choose_tool, response, lifetime_distance_traveled_manager_window):
    compare_data_type_of_new_lifetime_distance_traveled_entry_field = StringVar()
    compare_data_type_of_new_lifetime_distance_traveled_entry_field.set(new_lifetime_distance_traveled_entry_field.get())
    try:
        print(int(compare_data_type_of_new_lifetime_distance_traveled_entry_field.get()) + 10)
        lifetime_distance_traveled_manager_window.destroy()
    except Exception as e:
        messagebox.showerror('Update Lifetime Distance Traveled', "The entry " + str(new_lifetime_distance_traveled_entry_field.get()) + " is not a valid input!")
        lifetime_distance_traveled_manager_window.destroy()
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
The dropdown menu for selecting tools. This will be used for any operations regarding indivdual tools.
"""
def choose_tool_dropdown_menu():
    return

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
"""
Trying to fit a new frame inside of the tool_wear_manager frame. Getting some grid manager errors when doing it. Got the new frame commented out for now.
"""
# tool_wear_manager_display_frame = LabelFrame(tool_wear_manager_frame, padx=5, pady=5)
# tool_wear_manager_display_frame.grid(row=1, column=0, sticky=N+S+E+W)
# tool_wear_manager_display_frame.columnconfigure(0, weight=1, pad=10)
# tool_wear_manager_display_frame.rowconfigure(0, weight=1, pad=10)

"""
Defines and inserts the button to clear the executed_distance_traveled when the operator changes the selected tool in the tool selection drop down menu.
"""
button_that_clears_executed_distance_traveled = Button(tool_wear_manager_frame, text="Executed Tool Change", command=lambda: executed_tool_change(choose_tool), padx=5, pady=5)
button_that_clears_executed_distance_traveled.pack()

"""
Defines the button that actually calculates the executed_distance_traveled for a given file chosen in the import_data file dialogue box.
"""
button_that_updates_executed_distance_traveled = Button(calculate_executed_distance_traveled_frame, text="Calculate Executed Distance Traveled", command=lambda: update_executed_distance_traveled(raw_data_filepath), padx=5, pady=5)
button_that_updates_executed_distance_traveled.pack()

"""
Defines the button that will allow the operator to set a new Lifetime Distance Traveled for an individual tool.
"""
button_that_updates_lifetime_distance_traveled = Button(tool_wear_manager_frame, text='Update Lifetime Distance Traveled', command=lambda: update_lifetime_distance_traveled(choose_tool), padx=5, pady=5)
button_that_updates_lifetime_distance_traveled.pack()

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
# tool_selection_list = executed_distance_traveled.keys()  #Insert this into the text portion of the tool_selection OptionMenu.
tool_selection = OptionMenu(tool_wear_manager_frame, choose_tool, 'E001', 'E002', 'E003', 'E004', 'E005', 'E006', 'E007', 'E008', 'E009', 'E010', 'E011', 'E012', 'E013', 'E014', 'E015', 'E016', 'E017', 'E018')
tool_selection.pack()




"""
The function that loops the program until an operator exits the program.
"""
root.mainloop()
