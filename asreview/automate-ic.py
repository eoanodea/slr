import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



# CONFIG
PROJECT_URL = 'http://localhost:5001/projects/7438b4fcd1df4854945cbef3ce5bb78c/review'

GROUP_A = ['micro', 'cloud application']
GROUP_B = ['green', 'sustain', 'energy']
IRR_THRESHOLD = 100

# AVVIO
# service = Service(CHROMEDRIVER_PATH)
# driver = webdriver.Chrome(service=service)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(PROJECT_URL)
time.sleep(5)

irrelevant_streak = 0
max_irrelevant_streak = 0

while irrelevant_streak < IRR_THRESHOLD:
    try:
        # Estrai abstract
        abstract_text = None
        for div in driver.find_elements(By.TAG_NAME, "div"):
            text = div.text.strip()
            if len(text) > 100:
                abstract_text = text.lower()
                break

        if not abstract_text:
            print("❗ Nessun abstract valido trovato.")
            break

        # Valuta keyword
        matched_a = [kw for kw in GROUP_A if kw in abstract_text]
        matched_b = [kw for kw in GROUP_B if kw in abstract_text]
        is_relevant = bool(matched_a) and bool(matched_b)

        # Output
        # print("\n🔍 ABSTRACT:")
        # print(abstract_text)
        print("\n✅ MATCH GROUP A:", matched_a if matched_a else "Nessuna")
        print("✅ MATCH GROUP B:", matched_b if matched_b else "Nessuna")
        print("📌 Rilevanza:", "✅ RILEVANTE" if is_relevant else "❌ IRRILEVANTE")

        # Click bottone
        buttons = driver.find_elements(By.TAG_NAME, "button")
        if is_relevant:
            print("➡️ Clicco su RELEVANT")
            buttons[5].click()
            irrelevant_streak = 0
        else:
            print("➡️ Clicco su IRRELEVANT")
            buttons[4].click()
            irrelevant_streak += 1
            max_irrelevant_streak = max(max_irrelevant_streak, irrelevant_streak)

        print(f"🔁 Consecutivi irrilevanti: {irrelevant_streak}")
        print(f"🔁 Massimo consecutivi irrilevanti: {max_irrelevant_streak}")
        time.sleep(2)

    except Exception as e:
        print("❌ Errore:", e)
        break

# FINALE
print("\n📊 Screening terminato.")
print(f"🔢 Max irrilevanti consecutivi raggiunti: {max_irrelevant_streak}")
driver.quit()