import tkinter as tk
from tkinter import font
import json
import side_function

config = {
    'F1': '，',
    'F2': '。',
    'F3': '「',
    'F4': '」',
    'F5': '『',
    'F6': '』',
    'F7': '\n\n　　',
    'F8': '',
    'F9': '',
    'F10': '',
    'F11': '',
    'F12': '',
    'font': 'LXGW WenKai Mono TC',
    'font_size': 15,
    'width': 800,
    'height': 600,
}

try:
    configFile = open('config.json', 'r', encoding='utf-8')
    configContent = json.loads(configFile.read())
    for key in configContent:
        config[key] = configContent[key]
    configFile.close()
except FileNotFoundError:
    configFile = open('config.json', 'w', encoding='utf-8')
    configFile.write(json.dumps(config, ensure_ascii=False))
    configFile.close()

root = tk.Tk()
root.title('Simple Writer by 95')

root.geometry('{0}x{1}+{2}+{3}'.format(
    config['width'],
    config['height'],
    (root.winfo_screenwidth() // 2) - (config['width'] // 2),
    (root.winfo_screenheight() // 2) - (config['height'] // 2)
))

root_font = font.Font(family=config['font'], size=config['font_size'])

writer_text_widget = tk.Text(root, font=root_font, undo=True)
writer_text_widget.place(x=0, y=30, width=800, height=570)

side_function.bind_button(
    root,
    writer_text_widget,
    config
)

edit_setting_button = tk.Button(root, text='編輯設定', command=lambda: side_function.set_config(root, writer_text_widget, config))
edit_setting_button.place(relx=1.0, rely=0.0, anchor='ne')

text_cnt_label = tk.Label(root, text='0', font=root_font)
text_cnt_label.place(relx=0.0, rely=0.0, anchor='nw')

side_function.init_back_up()
side_function.back_up(root, writer_text_widget)
side_function.update_text_cnt(root, writer_text_widget, text_cnt_label)

root.mainloop()
