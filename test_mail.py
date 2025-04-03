import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 网易邮箱 SMTP 配置 ---
SMTP_SERVER = 'smtp.163.com'
SMTP_PORT = 465  # 使用 SSL

EMAIL_SENDER = 'yourname@163.com'      # 你的网易邮箱地址
EMAIL_PASSWORD = '你的授权码'           # 必须是授权码，不是登录密码
EMAIL_RECEIVER = 'someone@example.com'  # 接收方邮箱

# --- 邮件内容 ---
subject = '【测试邮件】来自网易邮箱的提醒'
body = '你好！这是一封来自网易邮箱的 SMTP 测试邮件。\n\n如果你收到了，说明设置成功！'

# --- 构造邮件对象 ---
msg = MIMEMultipart()
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_RECEIVER
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

# --- 发送邮件 ---
try:
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
    print("✅ 邮件发送成功！")
except Exception as e:
    print("❌ 邮件发送失败：", e)