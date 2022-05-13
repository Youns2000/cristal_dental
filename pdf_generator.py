from tkinter import *
from tkPDFViewer import tkPDFViewer as pdf
import fpdf


root = Tk()
root.title('Polaris-Implants')
v1 = pdf.ShowPdf()

# Adding pdf location and width and height.
v2 = v1.pdf_view(root,
                pdf_location = r"cdc.pdf",  
                width = 80, height = 100)
v2.pack()



root.mainloop()