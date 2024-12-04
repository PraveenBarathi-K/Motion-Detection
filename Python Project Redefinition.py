from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk
import pytesseract as py
from tkinter.filedialog import askopenfile
import tkinter.messagebox as messagebox

window=Tk()
window.geometry("1920x1080")
window.configure(bg='#97FFFF')
image=Image.open("D:\Python programs\psgitech.png")
resized=image.resize((250,250),Image.LANCZOS)
new_pic=ImageTk.PhotoImage(resized)

def new_window1():
    window.destroy()
    window1=Tk()
    window1.geometry("1920x1000")
    window1.configure(bg='#97FFFF')
    l1=Label(window1,text="Optical Character Recognition",font=("Angsana New",40,"bold"),bg="#97FFFF").place(relx=0.5,rely=0.15,anchor="n")
    image1=Image.open("D:\Python programs\snapedit_1683127590217.jpg")
    resized1=image1.resize((300,250),Image.LANCZOS)
    new_pic1=ImageTk.PhotoImage(resized1)
    l2=Label(window1,image=new_pic1).place(relx=0.5,rely=0.45,anchor="center")
    button1=Button(window1,text="Open File",font=("Georgia",20),bg="black",fg="white",activebackground="#97FFFF",command=img_to_text_converter).place(relx=0.5,rely=0.75,anchor="s")
    window1.mainloop()
    

data=""

def img_to_text_converter():
        global data,window2
        py.pytesseract.tesseract_cmd="D:\\Tesseract_OCR\\tesseract.exe"
        path=filedialog.askopenfilename()
        img=Image.open(path)
        data=py.image_to_string(img)
        messagebox.showinfo("Information",data)
            

#place function here is used to place the label at the required place.

l1=Label(window,text="PSG Institute of Technology and Applied Research",font=("Angsana New",40,"bold"),bg="#97FFFF").place(relx=0.5,rely=0.15,anchor="n")
l2=Label(window,image=new_pic).place(relx=0.5,rely=0.5,anchor="center")

button=Button(window,text="Continue",font=("Georgia",20),bg="black",fg="white",activebackground="#97FFFF",command=new_window1).place(relx=0.5,rely=0.80,anchor="s")


window.mainloop()