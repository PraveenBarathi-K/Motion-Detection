from PIL import ImageTk, Image
from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk
from tkinter.filedialog import askopenfile
from ttkbootstrap.constants import *
import pandas as panda
import cv2   
from datetime import datetime 
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import csv
import customtkinter

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")
window=customtkinter.CTk()
window.geometry("1920x1080")
window.title('MOTION DECTECTION')
image=Image.open("psg.jpg")
resized=image.resize((250,250),Image.LANCZOS)
new_pic=ImageTk.PhotoImage(resized) 
img1=ImageTk.PhotoImage(Image.open("bg5.jpg"))

def open():
    top= Toplevel()
    top.tilte("MOTION SENSING")
    top.geometry("800x800")
    my_img= ImageTk.PhotoImage(Image.open("D:/codes/psg.jpg"))
    my_label=Label(top, image=my_img)
    my_label.pack()


def csv_to_pdf(csv_file, pdf_file):
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    with open(csv_file, 'r') as file:
        data = list(csv.reader(file))
    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  
        ('FONTSIZE', (0, 0), (-1, 0), 12),  
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige), 
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'), 
        ('FONTSIZE', (0, 1), (-1, -1), 10),  
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black), 
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black), 
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  
    ])
    table.setStyle(style)
    elements = [table]
    doc.build(elements)
def start():
    window.destroy()  
    initialState = None  
    motionTrackList= [ None, None ]   
    motionTime = []  
    dataFrame = panda.DataFrame(columns = ["Initial", "Final"])
    video = cv2.VideoCapture(0)  
 
    while True:   
        check, cur_frame = video.read()  
        var_motion = 0   
        gray_image = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY)  
        gray_frame = cv2.GaussianBlur(gray_image, (21, 21), 0)    
        if initialState is None:  
            initialState = gray_frame  
            continue    
        differ_frame = cv2.absdiff(initialState, gray_frame)  
        thresh_frame = cv2.threshold(differ_frame, 30, 255, cv2.THRESH_BINARY)[1]  
        thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)   
        cont,_ = cv2.findContours(thresh_frame.copy(),   

                            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  
        for cur in cont:  
            if cv2.contourArea(cur) < 10000:  
                continue  
            var_motion = 1  
            (cur_x, cur_y,cur_w, cur_h) = cv2.boundingRect(cur)  
            cv2.rectangle(cur_frame, (cur_x, cur_y), (cur_x + cur_w, cur_y + cur_h), (0, 255, 0), 3)    
        motionTrackList.append(var_motion)  
        motionTrackList = motionTrackList[-2:]  
        if motionTrackList[-1] == 1 and motionTrackList[-2] == 0:  
            motionTime.append(datetime.now())  
        if motionTrackList[-1] == 0 and motionTrackList[-2] == 1:  
            motionTime.append(datetime.now())

        cv2.namedWindow("The image captured in the Gray Frame is shown below: ",cv2.WINDOW_NORMAL)
        cv2.resizeWindow("The image captured in the Gray Frame is shown below: ",300,300)
        cv2.imshow("The image captured in the Gray Frame is shown below: ", gray_frame)  

        cv2.namedWindow("Difference between the  inital static frame and the current frame: ",cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Difference between the  inital static frame and the current frame: ",300,300)
        cv2.imshow("Difference between the  inital static frame and the current frame: ", differ_frame)  

        cv2.namedWindow("Threshold Frame created from the PC or Laptop Webcam is: ",cv2.WINDOW_NORMAL) 
        cv2.resizeWindow("Threshold Frame created from the PC or Laptop Webcam is: ",300,300)
        cv2.imshow("Threshold Frame created from the PC or Laptop Webcam is: ", thresh_frame)  

        cv2.namedWindow("From the PC or Laptop webcam, this is one example of the Colour Frame:",cv2.WINDOW_NORMAL) 
        cv2.resizeWindow("From the PC or Laptop webcam, this is one example of the Colour Frame:",300,300)
        cv2.imshow("From the PC or Laptop webcam, this is one example of the Colour Frame:", cur_frame)   

        wait_key = cv2.waitKey(1)     

        if wait_key == ord('m'):  
            if var_motion == 1:  
                motionTime.append(datetime.now())  
            break 

    for a in range(0, len(motionTime), 2):  

        dataFrame = panda.concat([dataFrame, panda.DataFrame({"Initial": [motionTime[a]], "Final": [motionTime[a + 1]]})], ignore_index=True)
    csv_file_path =filedialog.asksaveasfilename(defaultextension="*.csv",filetypes = [('CSV','*.csv')],title='csv file')
    pdf_file_path = filedialog.asksaveasfilename(defaultextension="*.pdf",filetypes = [('PDF','*.pdf')],title='pdf file') 

    dataFrame.to_csv(csv_file_path)  
    csv_to_pdf(csv_file_path, pdf_file_path)
    video.release()   
    cv2.destroyAllWindows()

def exitout():
    window.destroy()

l=customtkinter.CTkLabel(master=window,image=img1)
l.pack()
l1=Label(window,text="PSG Institute of Technology and Applied Research",font=("Angsana New",20,"bold"),bg="#97FFFF").place(relx=0.5,rely=0.12,anchor="n")
l2=Label(window,image=new_pic).place(relx=0.5,rely=0.4,anchor="center")
button=customtkinter.CTkButton(master=window,width=220,height=50,text='NEXT',corner_radius=6,command=open,compound="right")
button.place(x=1100,y=700)
button2=customtkinter.CTkButton(master=window,width=220,height=50,text='EXIT',corner_radius=6,command=exit,compound="left")
button2.place(x=200,y=700)
window.mainloop()
