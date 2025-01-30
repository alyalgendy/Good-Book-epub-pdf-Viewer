from customtkinter import *
import tika
from tika import parser
from customtkinter import filedialog
from langdetect import detect
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import fitz
from PIL import Image, ImageTk
from tkinter.colorchooser import askcolor

# Initialize Tika
tika.initVM()

app = CTk()
app.title("Good Book epub,pdf Viewer")
app.geometry('700x700')

def process_text(text):
    language = detect(text)  # Detect the language
    if language == "ar":  # If the text is Arabic
        reshaped_text = reshape(text)  # Reshape Arabic letters
        bidi_text = get_display(reshaped_text)  # Correct the text direction
        return bidi_text, "right"
    else:  # For English or other LTR languages
        return text, "left"

def begin():
    for widget in app.winfo_children():
        widget.destroy()

    app.filename = filedialog.askopenfilename(
        initialdir="/",
        title="choose a file",
        filetypes=(("epub files", "*.epub"), ("pdf files", "*.pdf"))
    )

    def read_epub(file_path):
        parsed = parser.from_file(file_path)
        content = parsed["content"]
        return content

    def show_pdf(file_path):
        scrollable_frame = CTkScrollableFrame(app, width=700, height=700)
        scrollable_frame.pack(padx=20, pady=20, fill="both", expand=True)

        doc = fitz.open(file_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_tk = ImageTk.PhotoImage(img)

            label = CTkLabel(scrollable_frame, image=img_tk)
            label.image = img_tk  # Keep a reference to avoid garbage collection
            label.pack(padx=20, pady=20)


    def show_content(content):
        for widget in app.winfo_children():
            widget.destroy()

        text_to_display, alignment = process_text(content)

        textbox = CTkTextbox(app, width=700, height=630, wrap="word")
        textbox.insert("0.0", text_to_display)
        textbox.tag_config("align", justify=alignment)
        textbox.tag_add("align", "1.0", "end")
        textbox.configure(state="disabled")  # Make it read-only
        textbox.place(relx=0.5, rely=0.55, anchor="center")

        def fontchange(value):
            textbox.configure(font=("Arial", value))

        fontsize = CTkLabel(app, text="Font Size", font=("Times New Roman", 18))  
        fontsize.place(relx=0.25, rely=0.01, anchor="center")  

        font_slider = CTkSlider(app,
            from_=10,
            to=100,
            command=fontchange
            )
        font_slider.place(relx=0.25, rely=0.05, anchor="center")
        font_slider.set(10)

        def text_color():
            color_code = askcolor(title="Choose text color")[1]
            if color_code:
                textbox.configure(text_color=color_code)

        color_button = CTkButton(app, text="Choose Text Color", command=text_color)
        color_button.place(relx=0.45, rely=0.03)

        def bg_color():
            color_code = askcolor(title="Choose bg color")[1]
            if color_code:
                textbox.configure(fg_color=color_code)

        color_button = CTkButton(app, text="Choose bg Color", command=bg_color)
        color_button.place(relx=0.7, rely=0.03)

    file_path = app.filename
    if file_path.endswith(".epub"):
        content = read_epub(file_path)
        if content:
            show_content(content)
    elif file_path.endswith(".pdf"):
        show_pdf(file_path)
    else:
        print("Unsupported file type")
        return

lbl = CTkLabel(
    master=app,
    text="Good Book epub,pdf Viewer",
    font=("Times New Roman", 50)
)
lbl.place(relx=0.5, rely=0.3, anchor="center")

btn = CTkButton(
    master=app,
    text="choose your file",
    font=("Arial", 16),
    corner_radius=32,
    command=begin
)
btn.place(relx=0.5, rely=0.5, anchor="center")

app.mainloop()