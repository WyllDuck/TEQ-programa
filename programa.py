# Tkinter
from tkinter import *
from PIL import ImageTk, Image # pip install Pillow

# Tools:
import pandas as pd
from openpyxl import workbook # pip install openpyxl
from random import shuffle
import os
import time


# Set user sex:
def sex_male ():
    global frame
    global master
    global data

    data["sex"].append("MALE")

    # Set to 0 the UI (Tkinter)
    frame.destroy()
    frame = Frame(master)
    frame.pack()

    next()

def sex_female ():
    global frame
    global master
    global data

    data["sex"].append("FEMALE")

    # Set to 0 the UI (Tkinter)
    frame.destroy()
    frame = Frame(master)
    frame.pack()

    next()


# Save experiment values to CSV:
def save (filename):

    global path
    global data

    path_file = path + "\\results\{}.xlsx".format(filename)
    df = pd.DataFrame(data)
    df.to_excel(path_file, index = False)                           


# Get values experiments:
def get_states():

    data = {"num" : [], "Like / Dislike" : [], "Repercusion previa": [], "Modelo" : [], "Tag Precio" : [], "Sexo ropa" : [], "Description" : []}
    experiment_num = 1

    # Like / Dislike
    for i1 in range(-1,2,2):
        # Repercusion / No repercusion
        for i2 in range(-1,2,2):
            # Modelo / No modelo
            for i3 in range(-1,2,2):
                # Precio / No precio
                for i4 in range(-1,2,2):
                    # Sexo ropa
                    for i5 in range(-1,2,2):
                        # Description / No description
                        for i6 in range(-1,2,2):
                            data["Like / Dislike"].append(i1)
                            data["Repercusion previa"].append(i2)
                            data["Modelo"].append(i3)
                            data["Tag Precio"].append(i4)
                            data["Sexo ropa"].append(i5)
                            data["Description"].append(i6)
                            data["num"].append(experiment_num)

                            experiment_num += 1

    return data


# Go to the next image:
def next ():

    global frame
    global files
    global experiment_counter
    global data
    global path
    global scale
    global master
    global img
    global states
    global filename

    # While we still have images to show to the user we will repopulate the screen
    if experiment_counter < len(files):

        if experiment_counter > 0:
            
            print("exp: {} || num: {}".format(files[experiment_counter - 1], experiment_counter - 1))

            # Add information to "data" and save:
            data["experiment"].append(files[experiment_counter - 1])
            data["values"].append(scale.get())
            data["sex"] = [data["sex"][0] for i in range(len(data["values"]))]
            
            index = states["num"].index(int(files[experiment_counter - 1].replace(".jpg", "")))

            data["Like / Dislike"].append(states["Like / Dislike"][index])
            data["Repercusion previa"].append(states["Repercusion previa"][index])
            data["Modelo"].append(states["Modelo"][index])
            data["Tag Precio"].append(states["Tag Precio"][index])
            data["Sexo ropa"].append(states["Sexo ropa"][index])
            data["Description"].append(states["Description"][index])
            
            save(filename)

            # Set to 0 the UI (Tkinter)
            frame.destroy()
            frame = Frame(master)
            frame.pack()

        # First page (ask user sex)
        elif experiment_counter == -1:

            # Add buttons (male / female):
            button_male = Button(frame, text ="MALE", command = sex_male, height = 3, width = 20)
            button_male.pack()

            button_female = Button(frame, text ="FEMALE", command = sex_female, height = 3, width = 20)
            button_female.pack()

            experiment_counter += 1

            return

        # Add image to UI (Tkinter)
        img = Image.open(path + "\img\{}".format(files[experiment_counter]))
        img = img.resize((300, 505), Image.ANTIALIAS) #The (250, 250) is (width, height)
        img = ImageTk.PhotoImage(img)

        panel = Label(frame, image = img)
        panel.pack(side = "top", fill = "both", expand = "yes")

        # Add slider bar:
        scale = Scale(frame, from_=0, to=100, orient = HORIZONTAL, showvalue = 0, length = 400, resolution=0.1, width = 50)
        scale.pack()

        # Add button:
        button = Button(frame, text ="Next", command = next, height = 3, width = 20)
        button.pack()

        experiment_counter += 1
    
    else:

        # Add information to "data" and save:
        data["experiment"].append(files[experiment_counter - 1])
        data["values"].append(scale.get())
        data["sex"] = [data["sex"][0] for i in range(len(data["values"]))]
        
        index = states["num"].index(int(files[experiment_counter - 1].replace(".jpg", "")))

        data["Like / Dislike"].append(states["Like / Dislike"][index])
        data["Repercusion previa"].append(states["Repercusion previa"][index])
        data["Modelo"].append(states["Modelo"][index])
        data["Tag Precio"].append(states["Tag Precio"][index])
        data["Sexo ropa"].append(states["Sexo ropa"][index])
        data["Description"].append(states["Description"][index])
        
        save(filename)

        # Close Tkinter:
        master.destroy()

        print("The user has finished!")
        quit()


def main ():
    
    global frame
    global files
    global experiment_counter 
    global data
    global path
    global master
    global states
    global filename

    data = {"experiment": [], "values": [], "sex": [], "Like / Dislike" : [], "Repercusion previa": [], "Modelo" : [], "Tag Precio" : [], "Sexo ropa" : [], "Description" : []}
    experiment_counter = -1

    # Init Tkinter:
    master = Tk()
    frame = Frame(master)
    frame.pack()

    # Get all the images:
    path = os.path.dirname(os.path.abspath(__file__))
    files = os.listdir(path + "\img")
    files.sort()

    # Randomize the order of the images:
    shuffle(files)

    # Get states from all the experiments
    states = get_states()

    # Select a sample of X pictures we want to test:
    # files = files[0:16]

    # Set filename to save information:
    filename = "results_{}".format(time.strftime("%H_%M_%S"))

    # get things to appear on the screen:
    next()

    mainloop()

if __name__ == "__main__":
    main()
