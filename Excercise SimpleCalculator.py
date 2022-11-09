from tkinter import *

root = Tk()
root.title("Simple Calculator")

calculator_entry = Entry(root, width=35, borderwidth=5)
calculator_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# calculator_entry.insert(calculator_entry.get() + calculator_entry_display)

def populate_calculator_entry(number):
    # calculator_entry_display = calculator_entry.get() + text
    current = calculator_entry.get()
    calculator_entry.delete(0, END)
    calculator_entry.insert(0, str(current) + str(number))
def perform_addition_and_clear_calculator_entry():
    first_number = calculator_entry.get()
    global f_num
    global math
    math = "addition"
    f_num = first_number
    calculator_entry.delete(0, END)
    # return
def perform_subtraction_and_clear_calculator_entry():
    first_number = calculator_entry.get()
    global f_num
    global math
    math = "subtraction"
    f_num = first_number
    calculator_entry.delete(0, END)
    #return
def perform_multiplication_and_clear_calculator_entry():
    first_number = calculator_entry.get()
    global f_num
    global math
    math = "multiplication"
    f_num = first_number
    calculator_entry.delete(0, END)
    #return
def perform_division_and_clear_calculator_entry():
    first_number = calculator_entry.get()
    global f_num
    global math
    math = "addition"
    f_num = first_number
    calculator_entry.delete(0, END)
    #return
def clear_calculator_memory():
    calculator_entry.delete(0, END)
    f_num = 0
    # return
def perform_arithmetic():
    if math == "addition":
            calculator_entry_number = int(f_num) + int(calculator_entry.get())
            calculator_entry.delete(0, END)
            calculator_entry.insert(0, str(calculator_entry_number))
    elif math == "subtraction":
        calculator_entry_number = int(f_num) - int(calculator_entry.get())
        calculator_entry.delete(0, END)
        calculator_entry.insert(0, str(calculator_entry_number))
    elif math == "multiplication":
        calculator_entry_number = int(f_num) * int(calculator_entry.get())
        calculator_entry.delete(0, END)
        calculator_entry.insert(0, str(calculator_entry_number))
    else:
        calculator_entry_number = int(f_num) / int(calculator_entry.get())
        calculator_entry.delete(0, END)
        calculator_entry.insert(0, str(calculator_entry_number))

    # calculator_entry_number = int(f_num) + int(calculator_entry.get())
    # calculator_entry.delete(0, END)
    # calculator_entry.insert(0, str(calculator_entry_number))
    # if int(f_num) + int(calculator_entry.get()) == int():
    #     calculator_entry.delete(0, END)
    #     calculator_entry_number = int(f_num) + int(Calculator_entry.get())
    #     calculator_entry.insert(0, str(calculator_entry_number))
    # else:
    #     calculator_entry.delete(0, END)
    #     f_num = 0
    #     calculator_entry.insert(0, str("Error! You didn't add two numbers!"))
    # return


# Define the buttons.
button_1 = Button(root, text="1", padx=40, pady=20, command=lambda: populate_calculator_entry(1))
button_2 = Button(root, text="2", padx=40, pady=20, command=lambda: populate_calculator_entry(2))
button_3 = Button(root, text="3", padx=40, pady=20, command=lambda: populate_calculator_entry(3))
button_4 = Button(root, text="4", padx=40, pady=20, command=lambda: populate_calculator_entry(4))
button_5 = Button(root, text="5", padx=40, pady=20, command=lambda: populate_calculator_entry(5))
button_6 = Button(root, text="6", padx=40, pady=20, command=lambda: populate_calculator_entry(6))
button_7 = Button(root, text="7", padx=40, pady=20, command=lambda: populate_calculator_entry(7))
button_8 = Button(root, text="8", padx=40, pady=20, command=lambda: populate_calculator_entry(8))
button_9 = Button(root, text="9", padx=40, pady=20, command=lambda: populate_calculator_entry(9))
button_0 = Button(root, text="0", padx=40, pady=20, command=lambda: populate_calculator_entry(0))
button_clear = Button(root, text="Clear", padx=76, pady=20, command=clear_calculator_memory)
button_addition = Button(root, text="+", padx=39, pady=20, command=perform_addition_and_clear_calculator_entry)
button_multiplication = Button(root, text="*", padx=40, pady=20, command=perform_multiplication_and_clear_calculator_entry)
button_division = Button(root, text="/", padx=40, pady=20, command=perform_division_and_clear_calculator_entry)
button_subtraction = Button(root, text="-", padx=40, pady=20, command=perform_subtraction_and_clear_calculator_entry)
button_solve = Button(root, text="=", padx=86, pady=20, command=perform_arithmetic)

# Locate the buttons
button_1.grid(row=3, column=0)
button_2.grid(row=3, column=1)
button_3.grid(row=3, column=2)
button_4.grid(row=2, column=0)
button_5.grid(row=2, column=1)
button_6.grid(row=2, column=2)
button_7.grid(row=1, column=0)
button_8.grid(row=1, column=1)
button_9.grid(row=1, column=2)
button_0.grid(row=4, column=0)
button_clear.grid(row=4, column=1, columnspan=3)
button_addition.grid(row=5, column=0)
button_solve.grid(row=5, column=1, columnspan=3)
button_multiplication.grid(row=1, column=3)
button_division.grid(row=2, column=3)
button_subtraction.grid(row=3, column=3)

root.mainloop()
