from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import tkinter as tk
from my_package.model import ImageCaptioningModel
from my_package.model import ImageClassificationModel
from functools import partial
import os


def fileClick():
    # Define the function you want to call when the filebrowser button (Open) is clicked.
    # This function should pop-up a dialog for the user to select an input image file.
    global file_path
    file_path = filedialog.askopenfilename()
    image = Image.open(file_path)
    image = image.resize((500, 300))
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo


# Function for image captioning
def image_captioning():
    output_label.config(text="Running image captioning on: " + file_path)

# Function for image classification
def image_classification():
    output_label.config(text="Running image classification on: " + file_path)

def process(option_variable, captioner, classifier):
    # This function will produce the required output when 'Process' button is clicked.
    if 'file_path' not in globals():
        output_label.config(text="Error: No image selected.")#handle the case if the user clicks on the `Process` button without selecting any image file.
        return

    selected_option = option_variable.get()
    if selected_option == "Image Captioning":
        t=Text(root,height=10,width=60,font="Arial")
        t.insert(END,"\t\tTOP #3 Captions generated\n\n")
        y = captioner.__call__(file_path,3)
        for i in range(len(y)):
            t.insert(END,str(i)+". ")
            t.insert(END,y[i])
            t.insert(END,"\n")
        t.grid(row=2,column=4)    
    elif selected_option == "Image Classification":
        #Image classification model is called and displayed
            t=Text(root,height=10,width=60,font="Arial")
            t.insert(END,"\t\tTOP #3 classes\n\n")
            y= classifier.__call__(file_path)
            for i in range(len(y)):
                t.insert(END,str(i)+". ")
                t.insert(END,y[i])
                t.insert(END,"\n")
            t.grid(row=2,column=4) 


if __name__ == '__main__':
    # Instantiate the root window.
    root = tk.Tk()
    root.title("Image Processing")
    # Provide a title to the root window.
    select_button = tk.Button(root, text="Open", command=fileClick)#button for open
    select_button.grid(row=1,column=0)
    # Label to display selected image
    image_label = tk.Label(root)
    image_label.grid(row=2,column=0)

    # Declare the drop-down button.
    option_label = tk.Label(root, text="Select an image processing option:")
    option_label.grid(row=0)

    captioner=ImageCaptioningModel()
    classifier=ImageClassificationModel()
 
    option_variable = tk.StringVar(root)
    option_variable.set("Image Captioning")

    option_menu = tk.OptionMenu(root, option_variable, "Image Captioning", "Image Classification")
    option_menu.grid(row=1,column=1)

    # Declare the process button.
    process_button = tk.Button(root, text="Process", command=lambda:process(option_variable,captioner,classifier))
    process_button.grid(row=1,column=2)

    # Declare the output label.
    output_label = tk.Label(root, text="")
    output_label.grid(row=2,column=1)

    root.mainloop()
