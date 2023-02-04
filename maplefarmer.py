from tkinter import *

#Create window
win = Tk()
# set size
win.geometry("700x700")
#Set title
win.title("Maple Farmer")

#Entire font 
win.option_add("*Font","Timesnewroman 25")

# Create button
btn = Button(win, text="Button")
btn.pack()

# change bg color
win.configure(bg='light blue')

#Execute 
win.mainloop()