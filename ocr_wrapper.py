import cv2
import pytesseract
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

from reading import parse_tesseract_data

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Application")
        
        self.canvas = Canvas(root, cursor="cross")
        self.canvas.pack(fill=BOTH, expand=True)
        
        self.menu = Menu(root)
        root.config(menu=self.menu)
        file_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.load_image)
        
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.rect = None
        self.start_x = None
        self.start_y = None
        self.im = None
        self.ocr_result = None
        
    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.im = cv2.imread(file_path)
            self.ocr_result = pytesseract.image_to_string(self.im, config='--oem 3 --psm 3', lang='jpn_vert')
            print(self.ocr_result)
            data = pytesseract.image_to_data(self.im, output_type=pytesseract.Output.DICT, lang='jpn_vert')
            out = parse_tesseract_data(data)
            from pprint import pprint
            pprint(out)
            self.display_image(self.im)
    
    def display_image(self, image):
        self.imtk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
        self.canvas.create_image(0, 0, anchor=NW, image=self.imtk)
        self.root.geometry(f"{self.imtk.width()}x{self.imtk.height()}")
        
    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red')
    
    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)
    
    def on_button_release(self, event):
        self.extract_text(self.start_x, self.start_y, event.x, event.y)
    
    def extract_text(self, x1, y1, x2, y2):
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])
        
        # ensure coordinates are within image boundaries
        height, width, _ = self.im.shape
        x1 = max(0, min(x1, width))
        x2 = max(0, min(x2, width))
        y1 = max(0, min(y1, height))
        y2 = max(0, min(y2, height))

        selected_region = self.im[y1:y2, x1:x2]
        text = pytesseract.image_to_string(selected_region, lang='jpn_vert')  # or 'jpn', 'jpn_vert'
        
        self.display_text(text)

    def display_text(self, text):
        text_window = Toplevel(self.root)
        text_window.title("Extracted Text")
        text_area = Text(text_window)
        text_area.pack(fill=BOTH, expand=True)
        text_area.insert(1.0, text)
