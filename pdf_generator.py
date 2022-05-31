try:
    import tkinter as tk
    from tkinter import messagebox
    from tkinter import filedialog
except ImportError:
    import Tkinter as tk
    from Tkinter import messagebox
    from Tkinter import filedialog

# from tkPDFViewer import tkPDFViewer as pdf
# from fpdf import FPDF

from tkinter.scrolledtext import ScrolledText
import fitz
import os
from reportlab.pdfgen import canvas
from reportlab.lib import utils
from PyPDF2 import PdfFileWriter, PdfFileReader
from PIL import Image, ImageTk
import img


class PDFViewer(ScrolledText):
    def show(self, pdf_file):
        self.delete('1.0', 'end')
        pdf = fitz.open(pdf_file)
        self.images = []
        for page in pdf:
            pix = page.get_pixmap()
            pix1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
            photo = tk.PhotoImage(data=pix1.tobytes('ppm'))
            self.image_create('end', image=photo)
            self.insert('end', '\n')
            self.images.append(photo)


class MyPDF:
    def pdf_generate(self, e=None):
        self.x = self.scale_x.get()
        self.y = self.scale_y.get()
        self.size = self.scale_size.get()
        self.rotate = self.scale_rotate.get()

        img = utils.ImageReader('./pics.png')
        img_width, img_height = img.getSize()
        aspect = img_height / float(img_width)

        c = canvas.Canvas(self.curr_pdf)
        if self.bg_image_path:
            try:
                c.drawImage(self.bg_image_path, 0, 0)
            except OSError:
                tk.messagebox.showerror(
                    "Erreur image", "Le chemin pour l'image de font n'existe pas. Veillez reconfigurez l'image de font.")
        c.saveState()
        c.rotate(self.rotate)
        c.drawImage('./pics.png', self.x, self.y,
                    self.size, preserveAspectRatio=True)
        c.restoreState()
        c.save()
        self.pdf.show(self.curr_pdf)
        # self.c
        # self.c.showPage()
        # self.c.save()
        # pdf = FPDF()
        # pdf.add_page()

        # if self.bg_image_path:
        #     pdf.image(self.bg_image_path, 0, 0)
        # pdf.image('./pics.png', self.x, self.y, self.size)
        # pdf.output(self.curr_pdf, 'F')
        # self.pdf.show(self.curr_pdf)

    def on_closing(self):
        self.set_config()
        if os.path.exists(self.curr_pdf):
            os.remove(self.curr_pdf)
        self.pdfwin.destroy()

    def get_config(self):
        with open('config_pdf.txt', 'r') as file:
            lines = file.readlines()
            if len(lines) >= 3:
                self.size = float(lines[0])
                self.x = float(lines[1])
                self.y = float(lines[2])
                if len(lines) >= 4:
                    self.bg_image_path = lines[3][:-1]

    def set_config(self):
        with open('config_pdf.txt', 'w') as file:
            file.write(str(self.size)+"\n")
            file.write(str(self.x)+"\n")
            file.write(str(self.y)+"\n")
            file.write(str(self.bg_image_path)+"\n")

    def folder_selection(self):
        self.curr_pdf = filedialog.asksaveasfilename(
            title='Enregistrer sous ...', initialfile='fichier.pdf', defaultextension=".pdf", filetypes=[("PDF", "*.pdf"), ("All Files", "*.*")])
        if self.curr_pdf == None:
            self.curr_pdf = "./tmp.pdf"
            pass
        self.pdf_generate()
        self.pdfwin.destroy()

    def onConfig(self):
        self.bg_image_path = filedialog.askopenfilename(initialdir=self.bg_image_path, title="Open file", filetypes=(
            ("Images", "*.png;*.jpg;*.gif"), ("All files", "*.*")))

        self.set_config()
        self.pdf_generate()

    def rotate_(self, e=None):
        img.rotate_img('./pics.png', self.rotate, './pics.png')
        self.pdf_generate()

    def show_pdf(self):
        if not os.path.exists('pics.png'):
            tk.messagebox.showerror(
                "Erreur image", "Vous n'avez pris de photo!")
            return

        ################ SET CONFIG VARS ####################
        self.x = 10
        self.y = 10
        self.size = 10
        self.rotate = 0
        self.bg_image_path = ""
        self.curr_pdf = "./tmp.pdf"
        self.finalfolder = ""
        self.get_config()

        self.pdfwin = tk.Toplevel()
        self.pdfwin.attributes('-topmost', 1)
        self.pdfwin.title('Polaris-Implants - PDF')
        tk.Grid.rowconfigure(self.pdfwin, 0, weight=1)
        tk.Grid.columnconfigure(self.pdfwin, 0, weight=1)
        self.frame = tk.Frame(self.pdfwin)
        self.frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        self.menubar = tk.Menu(self.pdfwin)
        self.filemenu = tk.Menu(self.menubar)
        self.filemenu.add_command(label="Config", command=self.onConfig)
        self.filemenu.add_command(label="Exit")
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.pdfwin.config(menu=self.menubar)

        tk.Grid.rowconfigure(self.frame, 0, weight=1)
        tk.Grid.columnconfigure(self.frame, 0, weight=1)
        self.pdf = PDFViewer(self.pdfwin, width=75,
                             height=41, spacing3=5, bg='grey')
        self.pdf.grid(row=0, column=0, sticky='nsew')

        tk.Grid.columnconfigure(self.frame, 0, weight=1)
        tk.Grid.rowconfigure(self.frame, 1, weight=1)
        self.scale_x = tk.ttk.Scale(self.pdfwin, value=self.x, from_=0, to=300,
                                    orient="horizontal", command=self.pdf_generate,
                                    takefocus=False)
        self.scale_x.grid(row=1, column=0)

        tk.Grid.columnconfigure(self.frame, 1, weight=1)
        self.scale_y = tk.ttk.Scale(self.pdfwin, value=self.y, from_=800, to=-250,
                                    orient="vertical", command=self.pdf_generate,
                                    takefocus=False)
        self.scale_y.grid(row=0, column=1, rowspan=2)

        tk.Grid.rowconfigure(self.frame, 2, weight=1)
        tk.Grid.columnconfigure(self.frame, 0, weight=1)
        self.scale_size = tk.ttk.Scale(self.pdfwin, value=self.size, from_=50, to=600, variable=self.size,
                                       orient="horizontal", command=self.pdf_generate,
                                       takefocus=False)
        self.scale_size.grid(row=2, column=0)

        tk.Grid.rowconfigure(self.frame, 3, weight=1)
        tk.Grid.columnconfigure(self.frame, 0, weight=1)
        self.scale_rotate = tk.ttk.Scale(self.pdfwin, value=self.rotate, from_=0, to=360, variable=self.rotate,
                                         orient="horizontal", command=self.rotate_,
                                         takefocus=False)
        self.scale_rotate.grid(row=3, column=0)

        tk.Grid.rowconfigure(self.frame, 4, weight=1)
        self.retake_button = tk.ttk.Button(
            self.pdfwin, text="Enregistrer", command=self.folder_selection)
        self.retake_button.grid(
            row=4, column=0, columnspan=2, sticky=tk.S+tk.E+tk.W)

        self.pdf_generate()

        self.pdfwin.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.pdfwin.mainloop()
