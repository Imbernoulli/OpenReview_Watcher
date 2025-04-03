from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from cookies import COOKIES
import time
import re

URL = "https://openreview.net/group?id=aclweb.org/ACL/ARR/2025/February/Authors"
CHECK_INTERVAL = 30  # 秒

def extract_scores(driver):
    html = driver.page_source
    scores = re.findall(r"Overall_recommendation:\s*(\d+)", html)
    return list(map(int, scores))

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://openreview.net")
    for cookie in COOKIES:
        driver.add_cookie(cookie)
    driver.get(URL)
    time.sleep(5)

    last_scores = extract_scores(driver)
    print("初始评分:", last_scores)

    try:
        while True:
            time.sleep(CHECK_INTERVAL)
            driver.refresh()
            time.sleep(5)
            current_scores = extract_scores(driver)

            if current_scores != last_scores:
                print("⚠️ 检测到评分变化！")
                print("新评分:", current_scores)
                last_scores = current_scores
            else:
                print("无变动", time.strftime("%H:%M:%S"))

    except KeyboardInterrupt:
        print("已退出监控")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()