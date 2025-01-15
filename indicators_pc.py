#!/usr/bin/env python3

import flet as ft
import threading
from database import create_db, get_history
from utils import get_cpu_usage, get_memory_usage, get_disk_usage, timer_rec


# Флаг для управления таймером 
stop_timer = threading.Event()


def history_indicators(page: ft.Page) -> None:
    """Страница с историей уровня загруженности ПК"""
    
    page.title = "История"
    page.controls.clear()
    
    rows = get_history()
    data = [f"Дата: {row[0]}, {row[1]}" for row in rows]

    list_view = ft.ListView(auto_scroll=True, expand=True)
    list_view.controls.clear()

    for item in data: 
        if data.index(item) == 0:
            list_view.controls.append(ft.Divider())
        
        list_view.controls.append(ft.Text(item))
        list_view.controls.append(ft.Divider())

    message = ft.Text(value="История:", style="headlineMedium")
    back_button = ft.ElevatedButton(
        text="Назад", 
        on_click=lambda e: chek_indicators(page)
    )
    
    page.add(message, list_view, back_button)
    page.update()
    

def chek_indicators(page: ft.Page) -> None:
    """Страница с уровнем загруженности ПК"""

    page.title = "Уровень загруженности"
    flag = False
    global stop_timer
    page.controls.clear()

    memory_use = get_memory_usage()
    cpu_use = get_cpu_usage()
    disk_use = get_disk_usage()

    data = [f"ЦП: {cpu_use}", f"ОЗУ: {memory_use}", f"ПЗУ: {disk_use}"]
    list_view = ft.Column()

    for item in data: 
        list_view.controls.append(ft.Text(item))

    # Текстовое поле таймера
    timer_text = ft.Text(value="", visible=False)

    def fetch_data(e):
        nonlocal flag
        flag = not flag
        
        memory_use = get_memory_usage()
        cpu_use = get_cpu_usage()
        disk_use = get_disk_usage()
        
        indicators_use = f"ЦП: {cpu_use}, ОЗУ: {memory_use}, ПЗУ: {disk_use}"
        data = indicators_use.split(', ')

        list_view.controls.clear()

        for item in data: 
            list_view.controls.append(ft.Text(item))

        if flag:
            stop_timer.clear()
            threading.Thread(
                target=timer_rec, 
                args=(timer_text, page, list_view, stop_timer, ft)
            ).start()
            button_rec.text = "Остановить"
            timer_text.visible = True
        else:
            stop_timer.set()
            button_rec.text = "Начать запись"
            timer_text.visible = False
        page.update()


    message = ft.Text(value="Уровень загруженности:", style="headlineMedium")
    button_rec = ft.ElevatedButton(text="Начать запись", on_click=fetch_data)
    button_hist = ft.ElevatedButton(
        text="История", 
        on_click=lambda e: history_indicators(page)
    )

    button_row = ft.Row(controls=[button_rec, button_hist])

    page.add(message, list_view, button_row, timer_text)
    page.update()


create_db()
ft.app(target=chek_indicators)
