from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

CHROMEDRIVER_PATH = r"E:\down\chromedriver-win64\chromedriver-win64\chromedriver.exe"

def get_player_links():
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/110.0.5481.100 Safari/537.36"
    )

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://www.atptour.com/en/rankings/singles"
    driver.get(url)

    wait = WebDriverWait(driver, 20)
    # 等待表格加载完成
    wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "table.mobile-table.mega-table.non-live tbody tr")
    ))
    time.sleep(3)  # 额外等待确保JS加载

    rows = driver.find_elements(By.CSS_SELECTOR, "table.mobile-table.mega-table.non-live tbody tr")
    print(f"共找到 {len(rows)} 行数据")

    data_all = []
    for idx, row in enumerate(rows, 1):
        try:
            rank = row.find_element(By.CSS_SELECTOR, "td.rank").text.strip()

            # 前10名结构和后面结构不完全一样，先尝试简单方式获取名字
            try:
                player_name = row.find_element(By.CSS_SELECTOR, "ul.player-stats li.name a span").text.strip()
            except:
                player_name = row.find_element(By.CSS_SELECTOR, "ul.player-stats li.name a span.lastName").text.strip()

            player_link = row.find_element(By.CSS_SELECTOR, "ul.player-stats li.name a").get_attribute("href")
            if player_link.startswith("/"):
                player_link = "https://www.atptour.com" + player_link

            points = row.find_element(By.CSS_SELECTOR, "td.points a").text.strip()

            print(f"第{idx}行: 排名={rank}, 球员={player_name}, 积分={points}, 链接={player_link}")
            data_all.append([rank, player_name, points, player_link])
        except Exception as e:
            print(f"第{idx}行解析出错: {e}")
            print(row.get_attribute("outerHTML"))

    driver.quit()

    with open("atp_players_page1.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Rank", "Player", "Points", "Profile Link"])
        writer.writerows(data_all)

    print("数据写入完成！")

if __name__ == "__main__":
    get_player_links()
