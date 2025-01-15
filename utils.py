from os import popen
from database import add_indicators, create_db_connection
import time


def get_memory_usage() -> str:
    """Функция получает уровень загруженности ОЗУ"""
    
    result = popen('free -m').read()
    
    # Поиск строки с информацией о памяти
    lines = result.split('\n')
    mem_line = lines[1]
    
    # Извлечение значения используемой памяти
    mem_values = mem_line.split()
    used_memory = int(mem_values[2])
    
    return f'{used_memory}мб'


def get_cpu_usage() -> str:
    """Функция получает уровень загруженности ОЗУ"""
    
    # Выполнение команды `top` и чтение результата
    result = popen('top -bn1 | grep "Cpu(s)"').read().strip()
    
    # Разделение строки и извлечение значений "us" и "sy"
    values = result.split(',')
    user_space = float(values[0].split()[1])
    system_space = float(values[1].split()[0])
    
    # Сумма значений user space и system space
    cpu_usage = user_space + system_space
    return f'{cpu_usage:.2f}%'


def get_disk_usage() -> str:
    """Функция получает уровень загруженности ПЗУ"""

    # Выполнение команды `df` и чтение результата
    result = popen('df -h /').read().strip()
    
    # Разделение строки на строки и извлечение данных
    lines = result.split('\n')
    disk_info = lines[1].split()
    
    # Извлечение процента загрузки дискового пространства
    disk_usage = disk_info[4]
    return disk_usage


def timer_rec(timer_text: str, page, list_view, stop_timer,  
    ft_obj) -> None:
    """
    Таймер, который отсчитывает время с момента записи в бд и 
    записывает данные в бд
    """
    from datetime import datetime

    start_time = datetime.now()
    conn, cursor = create_db_connection()

    while not stop_timer.is_set():
        elapsed_time = datetime.now() - start_time
        minutes, seconds = divmod(int(elapsed_time.total_seconds()), 60)
        timer_text.value = f"{minutes}:{seconds}"
        
        memory_use = get_memory_usage()
        cpu_use = get_cpu_usage()
        disk_use = get_disk_usage()
        
        indicators_use = f"ЦП: {cpu_use}, ОЗУ: {memory_use}, ПЗУ: {disk_use}"
        data = indicators_use.split(', ')
        list_view.controls.clear()

        for item in data:
            list_view.controls.append(ft_obj.Text(item))

        page.update()
        add_indicators(cursor=cursor, conn=conn, indicators_use=indicators_use)
        time.sleep(1)
    
    timer_text.value = ""
    conn.close()
