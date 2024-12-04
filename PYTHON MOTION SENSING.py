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
window.configure(bg='dark slate gray')
image=Image.open("psg.jpg")
resized=image.resize((250,250),Image.LANCZOS)
new_pic=ImageTk.PhotoImage(resized)

# Importing the Pandas libraries  
import pandas as panda

# Importing the OpenCV libraries  
import cv2  

# Importing the time module  
import time  

# Importing the datetime function of the datetime module  
from datetime import datetime 

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import csv

def csv_to_pdf(csv_file, pdf_file):
    # Create a PDF document
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)

    # Read the CSV file
    with open(csv_file, 'r') as file:
        data = list(csv.reader(file))

    # Create a table from the CSV data
    table = Table(data)

    # Apply styles to the table
    
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header bottom padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Table background color
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Table text color
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Table font
        ('FONTSIZE', (0, 1), (-1, -1), 10),  # Table font size
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Middle alignment for all cells
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),  # Line above the header
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),  # Line below the header
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Gridlines for all cells
    ])
    table.setStyle(style)

    # Build the PDF document and save it
    elements = [table]
    doc.build(elements)
def start():
    window.destroy()
# Assigning our initial state in the form of variable initialState as None for initial frames  
    initialState = None  

    # List of all the tracks when there is any detected of motion in the frames  
    motionTrackList= [ None, None ]  

    # A new list 'time' for storing the time when movement detected  
    motionTime = []  

    # Initialising DataFrame variable 'dataFrame' using pandas libraries panda with Initial and Final column  
    dataFrame = panda.DataFrame(columns = ["Initial", "Final"])

    # starting the webCam to capture the video using cv2 module  
    video = cv2.VideoCapture(0)  

    # using infinite loop to capture the frames from the video 
    while True:  

        # Reading each image or frame from the video using read function 

        check, cur_frame = video.read()  

   

        # Defining 'motion' variable equal to zero as initial frame 

        var_motion = 0  

   

        # From colour images creating a gray frame 

        gray_image = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY)  

   

   # To find the changes creating a GaussianBlur from the gray scale image  

        gray_frame = cv2.GaussianBlur(gray_image, (21, 21), 0)  

   

   # For the first iteration checking the condition

   # we will assign grayFrame to initalState if is none  

        if initialState is None:  

            initialState = gray_frame  

            continue  

       

   # Calculation of difference between static or initial and gray frame we created  

        differ_frame = cv2.absdiff(initialState, gray_frame)  

   

   # the change between static or initial background and current gray frame are highlighted 

   

        thresh_frame = cv2.threshold(differ_frame, 30, 255, cv2.THRESH_BINARY)[1]  

        thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)  

   

   # For the moving object in the frame finding the coutours 

        cont,_ = cv2.findContours(thresh_frame.copy(),   

                            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  

   

        for cur in cont:  

            if cv2.contourArea(cur) < 10000:  

                continue  

            var_motion = 1  

            (cur_x, cur_y,cur_w, cur_h) = cv2.boundingRect(cur)  

       

       # To create a rectangle of green color around the moving object  

            cv2.rectangle(cur_frame, (cur_x, cur_y), (cur_x + cur_w, cur_y + cur_h), (0, 255, 0), 3)  

       

  # from the frame adding the motion status   

        motionTrackList.append(var_motion)  

        motionTrackList = motionTrackList[-2:]  

   

   # Adding the Start time of the motion 

        if motionTrackList[-1] == 1 and motionTrackList[-2] == 0:  

            motionTime.append(datetime.now())  

       

  # Adding the End time of the motion 

        if motionTrackList[-1] == 0 and motionTrackList[-2] == 1:  

            motionTime.append(datetime.now())  

       

  # In the gray scale displaying the captured image 
        cv2.namedWindow("The image captured in the Gray Frame is shown below: ",cv2.WINDOW_NORMAL)
        cv2.resizeWindow("The image captured in the Gray Frame is shown below: ",300,300)
        cv2.imshow("The image captured in the Gray Frame is shown below: ", gray_frame)  
        
   

   # To display the difference between inital static frame and the current frame 
        cv2.namedWindow("Difference between the  inital static frame and the current frame: ",cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Difference between the  inital static frame and the current frame: ",300,300)
        cv2.imshow("Difference between the  inital static frame and the current frame: ", differ_frame)  

   

   # To display on the frame screen the black and white images from the video 
        cv2.namedWindow("Threshold Frame created from the PC or Laptop Webcam is: ",cv2.WINDOW_NORMAL) 
        cv2.resizeWindow("Threshold Frame created from the PC or Laptop Webcam is: ",300,300)
        cv2.imshow("Threshold Frame created from the PC or Laptop Webcam is: ", thresh_frame)  

   

   # Through the colour frame displaying the contour of the object
        cv2.namedWindow("From the PC or Laptop webcam, this is one example of the Colour Frame:",cv2.WINDOW_NORMAL) 
        cv2.resizeWindow("From the PC or Laptop webcam, this is one example of the Colour Frame:",300,300)
        cv2.imshow("From the PC or Laptop webcam, this is one example of the Colour Frame:", cur_frame)  

   

   # Creating a key to wait  

        wait_key = cv2.waitKey(1)  

   

   # With the help of the 'm' key ending the whole process of our system   

        if wait_key == ord('m'):  

       # adding the motion variable value to motiontime list when something is moving on the screen  

            if var_motion == 1:  

                motionTime.append(datetime.now())  

            break 

    # At last we are adding the time of motion or var_motion inside the data frame  
    for a in range(0, len(motionTime), 2):  

        dataFrame = panda.concat([dataFrame, panda.DataFrame({"Initial": [motionTime[a]], "Final": [motionTime[a + 1]]})], ignore_index=True)
  

 # Get the file paths from the user
    csv_file_path = filedialog.asksaveasfilename(filetypes = [('CSV','*.csv')], title='Save File')
    pdf_file_path = filedialog.asksaveasfilename(filetypes = [('PDF','*.pdf')], title='Save File') 

    # To record all the movements, creating a CSV file  
    dataFrame.to_csv(csv_file_path)  

    # Convert CSV to PDF
    csv_to_pdf(csv_file_path, pdf_file_path)

    # Releasing the video   
    video.release()  

    # Now, Closing or destroying all the open windows with the help of openCV  
    cv2.destroyAllWindows()

l1=Label(window,text="PSG Institute of Technology and Applied Research",font=("Angsana New",20,"bold"),bg="#97FFFF").place(relx=0.5,rely=0.12,anchor="n")
l2=Label(window,image=new_pic).place(relx=0.5,rely=0.4,anchor="center")
button=Button(window,text="Continue",font=("Georgia",20),bg="black",fg="white",activebackground="#97FFFF",command=start).place(relx=0.5,rely=0.80,anchor="s")
window.mainloop()