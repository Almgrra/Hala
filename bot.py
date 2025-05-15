
import requests
import time
import logging
import json
from datetime import datetime
from bs4 import BeautifulSoup
import html
import traceback

# إعدادات البوت
BOT_TOKEN = "7033096284:AAH3w5cHWCYxW-9t0GlACl5-cTI-Mo-4sGU"
CHAT_ID = "6898083876"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# سجل الأحداث
logging.basicConfig(level=logging.INFO)

# السعر السابق لمقارنته
last_price = None

# دالة إرسال الرسائل
def send_message(text, to_admin=False):
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    try:
        requests.post(API_URL, data=payload)
    except Exception as e:
        logging.error(f"فشل الإرسال: {e}")

# دالة جلب سعر الدولار من موقع غير رسمي (محلي)
def get_black_market_price():
    try:
        res = requests.get("https://sp-today.com/app/api/cur.php?do=pricelist&region=damascus", timeout=10)
        data = res.json()
        usd_data = next((item for item in data if item["name_ar"] == "دولار أمريكي"), None)
        if usd_data:
            buy = int(usd_data["price"].replace(",", ""))
            return buy
    except:
        return None

# دالة تحليل الوضع السياسي والأمني البسيط (كمثال - يمكن تطويرها)
def analyze_context():
    # مكان إدخال خوارزمية أكثر تعقيدًا لاحقاً
    return "تحليل خاص: لا توجد مؤشرات مباشرة من الساحة السياسية حالياً، لكن استمرار الغموض الحكومي الداخلي يفتح المجال لتقلبات الدولار خلال الأيام القادمة."

# التشغيل المستمر
def main_loop():
    global last_price
    while True:
        try:
            price = get_black_market_price()
            if price and (last_price is None or abs(price - last_price) >= 50):
                direction = "ارتفاع" if price > (last_price or 0) else "انخفاض"
                send_message(f"تنبيه: {direction} في سعر الدولار - السعر الحالي: {price} ل.س")
                analysis = analyze_context()
                send_message(analysis, to_admin=True)
                last_price = price
            time.sleep(3600)  # كل ساعة
        except Exception as e:
            logging.error(traceback.format_exc())
            time.sleep(600)

if __name__ == "__main__":
    send_message("تم تشغيل بوت الدولار وتحليل السوق بنجاح.")
    main_loop()
