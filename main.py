from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By 
import telebot
import time
import schedule
import io
import re
from bs4 import BeautifulSoup
def run_code():
    driver = webdriver.Chrome(executable_path = "C:\\Users\\асер\\Рабочий стол\\парсинг\\chromedriver.exe")
    url = "https://lk.kinderphoto.ru/pp/index.php"
    try:
        driver.get(url=url)
        time.sleep(5)
        login_input = driver.find_element(By.ID, "ilogin")
        login_input.clear()
        login_input.send_keys("556")
        time.sleep(5)
        pass_input = driver.find_element(By.ID, "password")
        pass_input.clear()
        pass_input.send_keys("497487")
        pass_input.send_keys(Keys.ENTER)
        time.sleep(5)
        button = driver.find_element(By.XPATH, "//a[@onclick=\"javascript:XXQ('SetSPar^ZwKPP','VOPP_CPage','SELS');document.location.href='?';\"]")
        action = ActionChains(driver)
        time.sleep(2)
        driver.execute_script("arguments[0].click();", button)
        time.sleep(5)
        # Получаем код страницы
        page_source = driver.page_source
        # Записываем код страницы в файл
        with io.open('page.html', 'w', encoding='utf-8') as f:
            f.write(page_source)    
            time.sleep(5)
        # Читаем содержимое файла
        with open("page.html", "r", encoding='utf-8') as f:
            html_content = f.read()
        # Создаем объект BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        td_tags = soup.find_all("td")
        # Записываем данные в файл
        with io.open('Data_foto.html', 'w', encoding='utf-8') as f:
            for tag in td_tags:
                f.write(str(tag))
            time.sleep(5)
        with io.open('Data_foto.html', 'r', encoding='utf-8') as f:
        # читаем содержимое файла
            content = f.read()
        # используем регулярное выражение для извлечения текста на русском языке и цифр
        pattern = re.compile('[а-яА-Я0-9]+')
        matches = pattern.findall(content)   
        # Записываем результат в новый файл и добавляем строки 
        with io.open('Data_foto_ru.txt', 'w', encoding='utf-8') as f:
            for match in matches:
                if match == "Тема":    
                    f.write("\n")  # добавляем символ переноса строки перед словом "Тема"
                f.write(match + " ")
        with io.open('Data_foto_ru.txt', 'r', encoding='utf-8') as f:
        # читаем содержимое файла
            lines = f.readlines()
        # удаляем строки, содержащие "инф Д"
        lines = [line for line in lines if "инф Д" not in line]
        # сохраняем изменения в том же файле
        with io.open('Data_foto_ru.txt', 'w', encoding='utf-8') as f:
            f.writelines(lines)
        with io.open('Data_foto_ru.txt', 'r', encoding='utf-8') as f:
            # читаем содержимое файла
            lines = f.readlines()
    # удаляем первую строку и заменяем на новую
        lines[0] = "Сейчас доступны вот такие съемки\n"
        # удаляем строки, содержащие "инф Д"
        lines = [line for line in lines if "инф Д" not in line]
        # оставляем только текст между "Тема" и "Учреждение"
        new_lines = []
        for line in lines:
            if "Тема" in line and "Учреждение" in line:
                new_lines.append(line.split("Тема")[1].split("Учреждение")[0] + "\n")
        # сохраняем изменения в том же файле
        with io.open('Data_foto_ru.txt', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        # Устанавливаем токен бота и ID вашего чата в Telegram
        TOKEN = '5389354945:AAEL8T7PFmzeLyiGSVgXT7M6FDInjhONE-o'
        CHAT_ID = '1870658619'

        # Создание экземпляра бота
        bot = telebot.TeleBot(TOKEN)
        # Чтение данных из файла
        with open('Data_foto_ru.txt', 'r', encoding='utf-8') as f:
            data = f.read()
            # Отправляем сообщение
        bot.send_message(chat_id=CHAT_ID, text = data)

    finally:
        driver.close()
        driver.quit()
    pass

# запускаем код каждый час
schedule.every().hour.do(run_code)
# schedule.every(10).minutes.do(run_code)

while True:
    schedule.run_pending()
    time.sleep(1)   