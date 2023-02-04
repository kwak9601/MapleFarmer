from tkinter import *

#Create window
win = Tk()
# set size
win.geometry("700x700")
#Set title
win.title("Maple Farmer")

#Entire font 
win.option_add("*Font","Timesnewroman 25")

# Buttons
btn = Button(win, text="Button")
btn.pack()
btn.config(width=20, height=10)
btn.config(text = 'PRESS')
def alert():
    print('button is pressed')
btn.config(command=alert)

# change bg color
win.configure(bg='light blue')

#Execute 
win.mainloop()