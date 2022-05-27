try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pdf_generator import MyPDF
import mss
import os

class gui(tk.Tk):
    def __init__(self):
        self.curr_img = "./pics.png"
        
        self.root = tk.Tk()

        self.mypdf = MyPDF()
        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 0, weight=1)
        self.root.minsize(300, 200)
        self.root.title('Polaris-Implants')
        self.root.wm_attributes('-transparentcolor','red')
        self.root.attributes('-topmost', 1)

        self.frame=tk.Frame(self.root)
        self.frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Grid.rowconfigure(self.frame, 0, weight=1)
        tk.Grid.columnconfigure(self.frame, 0, weight=1)
        self.shot_area_cnv = tk.Canvas(self.frame, background="red")
        self.shot_area_cnv.grid(row=0, column=0, columnspan=3, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Grid.columnconfigure(self.frame, 0, weight=1)
        self.shot_button = tk.Button(self.frame, text ="Take a shot", command =self.shot)
        self.shot_button.grid(row=1, column=0, sticky=tk.S+tk.E+tk.W)  

        tk.Grid.columnconfigure(self.frame, 1, weight=1)
        self.retake_button = tk.Button(self.frame, text ="Retake a shot", command = self.refresh_cnv)
        self.retake_button.grid(row=1, column=1, sticky=tk.S+tk.E+tk.W)  

        tk.Grid.columnconfigure(self.frame, 2, weight=1)
        self.retake_button = tk.Button(self.frame, text ="PDF", command = self.mypdf.show_pdf)
        self.retake_button.grid(row=1, column=2, sticky=tk.S+tk.E+tk.W)  

        self.init_mss()

    def init_mss(self):
        with mss.mss() as sct:
            sct.shot(mon=-1, output=self.curr_img)
        if os.path.exists(self.curr_img):
            os.remove(self.curr_img)
    
    def refresh_cnv(self):
        self.shot_area_cnv.delete('all')
        if os.path.exists(self.curr_img):
            os.remove(self.curr_img)

    def shot(self):
        with mss.mss() as sct:
            monitor = {
                "top": self.root.winfo_y() + 35,
                "left": self.root.winfo_x() + 11,
                "width": self.root.winfo_width(), 
                "height": int(self.root.winfo_height()*0.9)
            }
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            image = ImageTk.PhotoImage(img)

            img.save(self.curr_img)

            self.shot_area_cnv.create_image(0,0, anchor = tk.NW, image=image)
            self.shot_area_cnv.image = image

    def on_closing(self):
        if os.path.exists(self.curr_img):
            os.remove(self.curr_img)
        if os.path.exists('./fpdf.pdf'):
            os.remove('./fpdf.pdf')
        self.root.destroy()

    def start(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()