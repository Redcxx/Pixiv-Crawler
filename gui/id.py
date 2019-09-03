import re
import sys
import time
import tkinter as tk
from threading import Thread

import texts
from common import go_to_next_screen, download
from models import PikaxGuiComponent


class IDDownloadThread(Thread):
    def __init__(self, output_area, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_area = output_area

    def run(self):
        super().run()
        if self.output_area:
            self.output_area.see(0.0)


class IdScreen(PikaxGuiComponent):

    def __init__(self, master, pikax_handler):
        super().__init__(master, pikax_handler)

        self.grid_width = 20
        self.grid_height = 18
        self.id_or_url_text_id = self.add_text(text=texts.ID_SCREEN_ID_OR_URL, row=4, column=9, columnspan=2)

        self.id_or_url_input = self.make_text(height=10)
        self.id_or_url_input_id = self.add_widget(widget=self.id_or_url_input, row=8, column=9, columnspan=2)

        # buttons
        self.download_button = self.make_button(text=texts.ID_SCREEN_DOWNLOAD)
        self.download_button_id = self.add_widget(widget=self.download_button, row=13, column=11)
        self.back_button = self.make_button(text=texts.ID_SCREEN_BACK)
        self.back_button_id = self.add_widget(widget=self.back_button, row=13, column=8)

        self.output = self.make_download_output()
        self.output_id = self.add_text(text='', row=15, column=9, columnspan=2, font=self.output_font)
        self.redirect_output_to(self.output_id, text_widget=False)

        self.download_button.configure(command=self.download_clicked)
        self.back_button.configure(command=self.back_clicked)

        self.download_thread = None

        self.id_or_url_input.focus_set()
        # self.output.configure(state=tk.DISABLED)
        self.frame.pack_configure(expand=True)
        self.pack(self.frame)

    def back_clicked(self):
        from menu import MenuScreen
        go_to_next_screen(self, MenuScreen)

    def download_clicked(self):
        self.canvas.itemconfigure(self.output_id, text='')
        user_input = self.id_or_url_input.get(0.0, tk.END)
        search_ids = re.findall(r'(?<!\d)\d{8}(?!\d)', user_input, re.S)
        if search_ids:
            params = {'illust_ids': search_ids}
            download(target=self.pikax_handler.download_by_ids, kwargs=params)
        else:
            sys.stdout.write(texts.ID_SCREEN_NO_ID_FOUND)

    def destroy(self):
        self.frame.destroy()
