import os
import customtkinter as ui

from logic import logic


class App(ui.CTk):
    def __init__(self):
        super().__init__()
        self.title("Расчет оптического кабеля")
        self.minsize(width=700, height=400)

        self.file_name = None
        self.file_content = None

        # left screen part
        self.left_buttons = ui.CTkFrame(self)
        self.left_buttons.pack(
            padx=10, pady=10,
            ipadx=20, ipady=20,
            side=ui.LEFT, fill="both",
        )

        # left top half
        self.file_top_half = ui.CTkFrame(self.left_buttons)
        self.file_top_half.pack(
            padx=10, pady=10,
            ipadx=20, ipady=20,
            side=ui.TOP, fill="both", expand=True,
        )

        self.file_button = ui.CTkButton(
            self.file_top_half, text='Выберите файл',
            command=self.select_file,
        )
        self.file_button.pack(expand=True)

        self.file_name_label = ui.CTkLabel(
            self.file_top_half, text="Имя файла",
        )
        self.file_name_label.pack(expand=True)

        # left bottom half
        self.result_bottom_half = ui.CTkFrame(self.left_buttons)
        self.result_bottom_half.pack(
            padx=10, pady=10,
            ipadx=20, ipady=20,
            side=ui.BOTTOM, fill="both", expand=True,
        )

        self.count_button = ui.CTkButton(
            self.result_bottom_half, text="Рассчитать",
            command=self.count,
        )
        self.count_button.pack(expand=True)

        self.result_label = ui.CTkLabel(
            self.result_bottom_half, text="0.0 метров",
        )
        self.result_label.pack(expand=True)

        # right screen part
        self.right_loc_list = ui.CTkScrollableFrame(self)
        self.right_loc_list.pack(padx=10, pady=10, side=ui.RIGHT, fill="both", expand=True)

    def count(self):
        length, points = logic(self.file_content)
        self.result_label.configure(text=str(length))

        [child.destroy() for child in self.right_loc_list.winfo_children()]
        for (point, line) in zip(points, self.file_content):
            lat, lon, level = point
            text = f'{line.strip()}\n\n' \
                   f'Широта: {lat:.3f}    ' \
                   f'Долгота: {lon:.3f}    ' \
                   f'Этажей: {level}'
            child = ui.CTkButton(
                self.right_loc_list, text=text, border_spacing=10,
                state=ui.DISABLED, text_color_disabled="white", fg_color="grey32"
            )
            child.pack(padx=10, pady=10, fill="both")

    def select_file(self):
        file_type = (
            ('Текстовые файлы', '*.txt'),
            ('Все файлы', '*.*'),
        )
        temp_name = ui.filedialog.askopenfilename(
            title='Откройте файл со списком адресов площадок узлов связи',
            filetypes=file_type,
        )
        if temp_name == '':
            return

        self.file_content = open(temp_name, mode='r', encoding='utf-8').readlines()
        self.file_name_label.configure(text=os.path.basename(temp_name).strip())

        self.result_label.configure(text="0.0 метров")
        [child.destroy() for child in self.right_loc_list.winfo_children()]
        for line in self.file_content:
            child = ui.CTkButton(
                self.right_loc_list, text=line.strip(), border_spacing=10,
                state=ui.DISABLED, text_color_disabled="white", fg_color="grey32"
            )
            child.pack(padx=10, pady=10, fill="both")
