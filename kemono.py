import requests
from bs4 import BeautifulSoup
from os.path import join, exists
from pathlib import Path
from os import makedirs
import sys
from urllib.parse import unquote
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

def kemono(url):
    # Khởi tạo trình duyệt
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=800x600")
    chromedrv = join(sys.path[0], "chromedriver_(135.0.7049.42_(r1427262)).exe")
    service = Service(executable_path=chromedrv)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Mở trang web
        driver.get(url)

        # Chờ cho đến khi phần tử mong muốn được tải
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'post__body'))
        )

        # Lấy nội dung trang sau khi tải xong
        page_source = driver.page_source
    finally:
        # Đóng trình duyệt
        driver.quit()

    # Phân tích cú pháp HTML từ trang web
    soup = BeautifulSoup(page_source, 'html.parser')
    print(soup)

    # Tìm tất cả các thẻ <a> trong HTML, lấy thuộc tính href (URL của liên kết)
    links = [a['href'] for a in soup.find_all('a', class_='post__attachment-link')]
    pics = [a['href'] for a in soup.find_all('a', class_='fileThumb image-link')]
    print(links)
    print(pics)

    title = soup.title.string
    folder_name = re.sub(r'[\\/*?:"<>|]', "", title)
    down_dir = Path(sys.path[0]) / "downloads"
    if not exists(down_dir):
        makedirs(down_dir)
    down_dir2 = Path(down_dir) / folder_name
    if not exists(down_dir2):
        makedirs(down_dir2)

    # Tải và lưu tất cả các liên kết
    if links:
        for link in links:
            if '.' in link:
                response = requests.get(link, stream=True)
                l = link.split('/')
                file = l[-1].split('?f=')[-1]
                file = unquote(file)
                output_dir = join(down_dir2, file)
                with open(output_dir, 'wb') as out_file:
                    out_file.write(response.content)
                print(f"Đã tải {link}")
    if pics:
        for link in pics:
            if '.' in link:
                response = requests.get(link, stream=True)
                l = link.split('/')
                file = l[-1].split('?f=')[-1]
                file = unquote(file)
                output_dir = join(down_dir2, file)
                with open(output_dir, 'wb') as out_file:
                    out_file.write(response.content)
                print(f"Đã tải {link}")

if __name__ == "__main__":
    while True:
        web = input("Nhập URL (hoặc gõ 'exit' để thoát): ").strip()
        if web.lower() == 'exit':
            print("Đã thoát chương trình.")
            break
        print("Running...")
        start_time = time.time()
        try:
            kemono(web)
        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Thời gian chạy: {elapsed_time:.2f} giây")
        print("Tất cả đã hoàn thành!")