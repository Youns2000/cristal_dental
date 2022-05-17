from tkinter import *
from tkPDFViewer import tkPDFViewer as pdf
from fpdf import FPDF

# class PDF(FPDF):

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(40, 10, 'Hello World!')
pdf.image('refresh.png', 10, 8, 33)
pdf.output('tuto1.pdf', 'F')




# root = Tk()
# root.title('Polaris-Implants')
# v1 = pdf.ShowPdf()

# # Adding pdf location and width and height.
# v2 = v1.pdf_view(root,
#                 pdf_location = r"cdc.pdf",  
#                 width = 80, height = 100)
# v2.pack()



# root.mainloop()