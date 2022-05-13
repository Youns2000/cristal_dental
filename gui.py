from tkinter import *
from PIL import Image, ImageTk
import mss
import mss.tools
import os

class gui():
    def __init__(self):
        self.curr_img = "./pics.png"
        self.root = Tk()
        self.root.title('Polaris-Implants')
        window_width = 1100
        window_height = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.attributes('-topmost', 1)
        self.root.wm_attributes('-transparentcolor','grey')
        self.root.update_idletasks()
        self.init_mss()
        # root.iconbitmap('./logo.ico')
        # root.attributes('-alpha',0.5)

        self.shot_area_cnv = Canvas(self.root, background="grey")
        self.shot_area_cnv.pack(fill=X, side=TOP)
        self.buttons_cnv = Canvas(self.root)
        self.buttons_cnv.pack(fill=X, side=BOTTOM)

        self.shot_button = Button(self.buttons_cnv, width=int(self.buttons_cnv.winfo_height()//2), text ="Take a shot", font=("Consolas", 17), command =self.shot)
        self.shot_button.pack(side=LEFT, expand=True)
        icon = PhotoImage(file="./final/refresh.png")
        self.retake_button = Button(self.buttons_cnv, image=icon, width=int(self.buttons_cnv.winfo_height()//2), text ="Retake a shot", command = self.refresh_cnv)
        self.retake_button.pack(side=RIGHT, expand=True)

    def init_mss(self):
        with mss.mss() as sct:
            sct.shot(mon=-1, output=self.curr_img)
        if os.path.exists(self.curr_img):
            os.remove(self.curr_img)

    def shot(self, e = None):
        with mss.mss() as sct:
            monitor = {
                "top": self.root.winfo_y() + 35,
                "left": self.root.winfo_x() + 11,
                "width": self.root.winfo_width(), 
                "height": int(self.root.winfo_height()*0.9)
            }
            sct_img = sct.grab(monitor)
            # mss.tools.to_png(sct_img.rgb, sct_img.size, output=CURR_IMG)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            image = ImageTk.PhotoImage(img)

            img.save(self.curr_img)

            panel = Label(self.shot_area_cnv, image=image)
            panel.pack(side=TOP, fill=BOTH)
            self.root.update_idletasks()
    
    def manage_size(self, event):
        self.shot_area_cnv.config(height=int(self.root.winfo_height()*0.9))
        self.buttons_cnv.config(width=int(self.root.winfo_height()*0.1))

    def refresh_cnv(self):
        self.shot_area_cnv.delete('all')

    def on_closing(self):
        if os.path.exists(self.curr_img):
            os.remove(self.curr_img)
        self.root.destroy()

    def gui_main(self):    
        


        self.shot_area_cnv.bind("<Configure>", self.manage_size)
        self.root.bind('<KeyPress>', self.shot)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()