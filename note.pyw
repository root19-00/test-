import requests
import time
import win32com.client
import pyautogui
import subprocess # المكتبة المسؤولة عن فتح برنامج المفكرة تلقائياً

DB_BASE_URL = "https://a0zai-56c3a-default-rtdb.europe-west1.firebasedatabase.app/A0Z_CORE"

def speak(text):
    """دالة لتحويل النص إلى كلام مسموع"""
    try:
        print(f"[صوت] نطق: {text}")
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(text)
    except Exception as e:
        print(f"خطأ في محرك الصوت: {e}")

def start_gateway():
    print("=========================================")
    print("      A0Z CORE - SMART ASSISTANT ACTIVE  ")
    print("=========================================")
    print("بانتظار تلقي الأوامر من لوحة التحكم...")
    
    cmd_url = f"{DB_BASE_URL}/current_command.json"
    last_ts = 0  # لتجنب تكرار الأوامر القديمة عند بدء التشغيل
    
    while True:
        try:
            response = requests.get(cmd_url)
            data = response.json()
            if data:
                text = data.get('text', '')
                ts = data.get('timestamp', 0)
                
                # التحقق من أن الأمر جديد بناءً على الوقت (Timestamp)
                if ts > last_ts:
                    print(f"\n[أمر جديد] تم تلقي: {text}")
                    
                    if text.startswith("/say "):
                        clean_text = text.replace("/say ", "")
                        speak(clean_text)
                        
                    elif text.startswith("/type "):
                        clean_text = text.replace("/type ", "")
                        
                        # 💡 فتح المفكرة تلقائياً وتجهيزها للكتابة
                        print("[نظام] جاري فتح برنامج المفكرة (Notepad)...")
                        subprocess.Popen("notepad.exe")
                        time.sleep(1.5) # ننتظر ثانية ونصف لتفتح المفكرة تماماً وتصبح الشاشة النشطة
                        
                        print(f"[محاكاة كيبورد] كتابة نص: {clean_text}")
                        pyautogui.write(clean_text, interval=0.05)
                        
                    elif text.startswith("/press "):
                        key = text.replace("/press ", "")
                        print(f"[محاكاة كيبورد] الضغط على زر: {key}")
                        pyautogui.press(key)
                        
                    last_ts = ts  # تحديث طابع الوقت لتجنب التكرار
        except Exception as e:
            print(f"[خطأ اتصال] غير قادر على الاتصال بقاعدة البيانات: {e}")
            
        time.sleep(1) # فحص قاعدة البيانات كل ثانية واحدة

if __name__ == "__main__":
    start_gateway()