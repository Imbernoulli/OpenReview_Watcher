from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from cookies import COOKIES
import time
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- OpenReview 配置 ---
URL = "https://openreview.net/group?id=ICML.cc/2025/Conference/Authors"
CHECK_INTERVAL = 30  # 秒

# --- 网易邮箱 SMTP 配置 ---
SMTP_SERVER = 'smtp.163.com'
SMTP_PORT = 465  # 使用 SSL
EMAIL_SENDER = ''      # 你的网易邮箱地址
EMAIL_PASSWORD = ''       # 必须是授权码
EMAIL_RECEIVER = ''      # 接收方邮箱

def extract_scores(driver):
    html = driver.page_source
    scores = re.findall(r"Overall_recommendation:\s*(\d+)", html)
    return list(map(int, scores))

def send_email_notification(new_scores):
    subject = '【OpenReview提醒】评分已发生变化！'
    body = f'检测到评分发生变化，新的评分如下：\n\n{new_scores}\n\n请及时查看 OpenReview 页面。'

    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print("📧 邮件已发送通知评分变化")
    except Exception as e:
        print("❌ 邮件发送失败：", e)

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    # 登录并加载页面
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
                send_email_notification(current_scores)
                last_scores = current_scores
            else:
                print("无变动", time.strftime("%H:%M:%S"))

    except KeyboardInterrupt:
        print("🛑 已退出监控")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()