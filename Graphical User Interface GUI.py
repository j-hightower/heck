from tkinter import *

root = Tk() # Generates the actual view-window.

#Everything on top of the view-window will be a widget.
#Generates the actual text 'widget'.
myLabel = Label(root, text="Hello World!")
#Shoves/places/puts the text widget onto the view-window.
myLabel.pack()

#This is the 'mainloop'. It basically allows the program to run continuously until the operator closes the program.
root.mainloop()