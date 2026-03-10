import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import csv
import time
import random

def parse_player_page(url, driver):
    driver.get(url)
    time.sleep(random.uniform(4, 7))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(random.uniform(1, 2))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(1, 2))
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # 从URL中提取球员姓名
    try:
        name = url.split("/players/")[1].split("/")[0].replace("-", " ").title()
    except Exception:
        name = ""

    # 基本信息
    basic_info = {}
    pd_content = soup.find('div', class_='pd_content')
    if pd_content:
        for li in pd_content.find_all("li"):
            spans = li.find_all("span")
            if len(spans) >= 2:
                key = spans[0].get_text(strip=True).replace(":", "")
                val = spans[1].get_text(strip=True)
                basic_info[key] = val

    # 简要统计数据
    stats = {}
    stats_sections = soup.select("div.atp_player-stats .player-stats-details")
    for section in stats_sections:
        stats_type = section.select_one("div.type")
        stats_type_name = stats_type.get_text(strip=True) if stats_type else "Stats"

        for stat_div in section.find_all("div", recursive=False):
            if stat_div.get("class") and "type" not in stat_div["class"]:
                label_tag = stat_div.find("span", class_="stat-label")
                if label_tag:
                    label = label_tag.get_text(strip=True)
                    value = stat_div.get_text(strip=True).replace(label, "").strip()
                    stats[f"{stats_type_name} - {label}"] = value

    # 添加扩展的统计数据页
    full_stats_url = url.replace("/overview", "") + "/player-stats?year=all&surface=all"
    try:
        driver.get(full_stats_url)
        time.sleep(random.uniform(4, 6))
        full_html = driver.page_source
        full_soup = BeautifulSoup(full_html, "html.parser")
        stats_items = full_soup.select("li.stats_items")

        for item in stats_items:
            record = item.select_one("span.stats_record")
            percentage = item.select_one("span.stats_percentage")
            if record and percentage:
                key = f"Full Stats - {record.get_text(strip=True)}"
                value = percentage.get_text(strip=True)
                stats[key] = value
    except Exception as e:
        print(f"扩展统计页解析失败：{e}")

    return {
        "Name": name,
        **basic_info,
        **stats,
        "Profile Link": url
    }

def main():
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless")  # 如果你不需要浏览器窗口可以取消注释这行

    driver = uc.Chrome(options=options)

    players_data = []
    with open("atp_players_page1.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i < 50:
                continue  # 跳过前 50 条
            if i >= 100:
                break  # 到第 101 条停止
            url = row["Profile Link"]
            print(f"解析球员：{row.get('Player', 'Unknown')} 链接：{url}")
            try:
                data = parse_player_page(url, driver)
                players_data.append(data)
            except Exception as e:
                print(f"解析失败：{e}")
            time.sleep(random.uniform(5, 10))  # 防反爬等待

    driver.quit()

    # 收集所有字段名（列）
    fieldnames = set()
    for d in players_data:
        fieldnames.update(d.keys())

    # 把 Name 放最前面
    fieldnames = list(fieldnames)
    if "Name" in fieldnames:
        fieldnames.remove("Name")
    fieldnames = ["Name"] + fieldnames

    # 写入 CSV 文件
    with open("atp_players_detailed.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(players_data)

if __name__ == "__main__":
    main()
