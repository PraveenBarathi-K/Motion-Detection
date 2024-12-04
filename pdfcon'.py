import tkinter as tk
from tkinter import Canvas
from PIL import ImageTk, Image
import os
from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk
from tkinter.filedialog import askopenfile
import ttkbootstrap as s
from ttkbootstrap.constants import *


window=Tk()
window.geometry("700x600")
window.configure(bg='#97FFFF')
image=Image.open("psg.jpg")
resized=image.resize((250,250),Image.LANCZOS)
new_pic=ImageTk.PhotoImage(resized)
def window1():
# GUI application window
    window.destroy()
    win = s.Window(themename="solar")
    win.title('Img to Pdf converter application')
    win.iconphoto(False,tk.PhotoImage(file = 'pdfimg.png'))
    win.geometry('700x700')
    win.resizable(0,0)

    def disable(btn):
        btn['state']='disabled'

    def enable(btn):
        btn['state']='active'

    files = {}
    def upload_imgs():
        global files
        files = {}
        files['filename']=filedialog.askopenfilenames(filetypes=[('JPG','*.jpg'),('PNG','*.png'),('JPEG','*.jpeg')],
        initialdir = os.getcwd(), title='Select File/Files')
        if len(files['filename'])!=0:
            enable(download_button)
        
    def saveas():
        try:
            global files
            img_list = []
            for file in files['filename']:
                img_list.append(Image.open(file).convert('RGB'))
            save_file_name = filedialog.asksaveasfilename(filetypes = [('PDF','*.pdf')], initialdir=os.getcwd(), title='Save File')
            img_list[0].save(f'{save_file_name}.pdf', save_all=True, append_images = img_list[1:])
            disable(download_button)
        except:
            return
    # main img of application
    canvas = Canvas(win, bg='white',width = 250, height=250)
    canvas.grid(row =1,column=0, sticky=tk.N, padx=220, pady =25)

    main_img = ImageTk.PhotoImage(Image.open('image1.png'))
    canvas.create_image(125,120, image=main_img)
    # upload button
    upload_button = tk.Button(win, text='UPLOAD IMAGES', width = 20, height =1,font=('arial',14,'bold'), bg='white',fg='green', command=upload_imgs)
    upload_button.grid(row =2, column = 0, padx=200, pady =20)

    # Download button
    download_button = tk.Button(win, text='Download PDF', width = 20, height =1,font=('arial',14,'bold'), bg='white',fg='red', command=saveas)
    download_button.grid(row=3, column=0)
    disable(download_button)
    win.mainloop()
l1=Label(window,text="PSG Institute of Technology and Applied Research",font=("Angsana New",20,"bold"),bg="#97FFFF").place(relx=0.5,rely=0.12,anchor="n")
l2=Label(window,image=new_pic).place(relx=0.5,rely=0.4,anchor="center")
button=Button(window,text="Continue",font=("Georgia",20),bg="black",fg="white",activebackground="#97FFFF",command=window1).place(relx=0.5,rely=0.80,anchor="s")
window.mainloop()