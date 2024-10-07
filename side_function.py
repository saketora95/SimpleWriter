import tkinter as tk
import json
import os
import datetime

entry_string_var_dict = {}
entry_dict = {}

def bind_button(root: tk.Tk, text_widget: tk.Text, config):
    for i in range(1, 13):
        key = 'F' + str(i)
        root.bind(f'<F{i}>', lambda event, s=config[key]: insert_text(text_widget, s))

def re_bind_button(root: tk.Tk, text_widget: tk.Text, config, original_window: tk.Toplevel):
    new_config = config
    for i in range(1, 13):
        key = 'F' + str(i)
        new_config[key] = entry_string_var_dict[key].get()

    for item in ['font']:
        new_config[item] = entry_string_var_dict[item].get()

    for item in ['font_size', 'width', 'height']:
        new_config[item] = int(entry_string_var_dict[item].get())

    configFile = open('config.json', 'w', encoding='utf-8')
    configFile.write(json.dumps(new_config, ensure_ascii=False))
    configFile.close()

    bind_button(root, text_widget, new_config)
    original_window.destroy()

def insert_text(target_widget: tk.Text, target_text: str):
    target_widget.insert(tk.INSERT, target_text)

def set_config(root: tk.Tk, text_widget: tk.Text, config):
    setting_window = tk.Toplevel(root)
    setting_window.title('系統設定')

    for i in range(12):
        key = 'F' + str(i + 1)

        label = tk.Label(setting_window, text=key + '：')
        label.grid(row=i, column=0, padx=5, pady=5)

        entry_string_var_dict[key] = tk.StringVar(value=config[key])
        entry_dict[key] = tk.Entry(setting_window, textvariable=entry_string_var_dict[key])
        entry_dict[key].grid(row=i, column=1, padx=5, pady=5)

    font_label = tk.Label(setting_window, text='字體：')
    font_label.grid(row=12, column=0, padx=5, pady=5)
    entry_string_var_dict['font'] = tk.StringVar(value=config['font'])
    entry_dict['font'] = tk.Entry(setting_window, textvariable=entry_string_var_dict['font'])
    entry_dict['font'].grid(row=12, column=1, padx=5, pady=5)

    font_size_label = tk.Label(setting_window, text='字體大小：')
    font_size_label.grid(row=13, column=0, padx=5, pady=5)
    entry_string_var_dict['font_size'] = tk.StringVar(value=config['font_size'])
    entry_dict['font_size'] = tk.Entry(setting_window, textvariable=entry_string_var_dict['font_size'])
    entry_dict['font_size'].grid(row=13, column=1, padx=5, pady=5)

    root_geometry = root.geometry().split('x')

    width_label = tk.Label(setting_window, text='視窗寬度：')
    width_label.grid(row=14, column=0, padx=5, pady=5)
    entry_string_var_dict['width'] = tk.StringVar(value=root_geometry[0])
    entry_dict['width'] = tk.Entry(setting_window, textvariable=entry_string_var_dict['width'])
    entry_dict['width'].grid(row=14, column=1, padx=5, pady=5)

    height_label = tk.Label(setting_window, text='視窗高度：')
    height_label.grid(row=15, column=0, padx=5, pady=5)
    entry_string_var_dict['height'] = tk.StringVar(value=root_geometry[1].split('+')[0])
    entry_dict['height'] = tk.Entry(setting_window, textvariable=entry_string_var_dict['height'])
    entry_dict['height'].grid(row=15, column=1, padx=5, pady=5)

    save_button = tk.Button(
        setting_window,
        text='儲存設定',
        command=lambda: re_bind_button(root, text_widget, config, setting_window)
    )
    save_button.grid(row=16, column=0, columnspan=2, pady=10)

def init_back_up():
    os.makedirs('backup', exist_ok=True)

def back_up(root: tk.Tk, text_widget: tk.Text):
    content = text_widget.get('1.0', tk.END)

    if content != '\n':
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        backup_file_path = os.path.join('backup', f'{current_time}.txt')

        with open(backup_file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        cleanup_old_backups()

    root.after(60000, lambda: back_up(root, text_widget))

def cleanup_old_backups():
    backup_files = [f for f in os.listdir('backup') if f.endswith('.txt')]
    backup_files.sort()

    while len(backup_files) > 10:
        oldest_file = os.path.join('backup', backup_files.pop(0))
        os.remove(oldest_file)