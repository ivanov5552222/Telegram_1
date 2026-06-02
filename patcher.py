import os
import re
import sys

def patch_clean_telegram():
    settings_path = "TMessagesProj/src/main/java/org/telegram/ui/SettingsActivity.java"
    
    if not os.path.exists(settings_path):
        print(f"🚨 КРИТИЧЕСКАЯ ОШИБКА: Файл не найден: {settings_path}")
        sys.exit(1)

    print("⏳ Авто-патчер начал работу...")

    with open(settings_path, "r", encoding="utf-8") as f:
        code = f.read()

    is_button_ok = False
    is_click_ok = False

    # 0. ОЧИСТКА: Удаляем старую кнопку из шапки, чтобы не было дублей
    werygram_btn = 'items.add(SettingCell.Factory.of(9999, 0xFF55CA47, 0xFF27B434, R.drawable.msg_settings, "WeryGram"));'
    code = code.replace(werygram_btn, "") # Стираем старые следы
    code = code.replace('items.add(UItem.asAction(9999, R.drawable.msg_settings, "WeryGram"));', "")

    # 1. ПРАВИЛЬНАЯ ВСТАВКА: Ищем "Настройки чатов" (ChatSettings) и ставим под ними
    # Регулярка ищет строчку добавления ChatSettings
    match_chat = re.search(r'(items\.add\(.*?[cC]hat[sS]ettings.*?\);)', code)
    match_privacy = re.search(r'(items\.add\(.*?[pP]rivacy.*?\);)', code)

    if match_chat:
        anchor = match_chat.group(1)
        code = code.replace(anchor, f'{anchor}\n        {werygram_btn}')
        is_button_ok = True
        print("✅ Кнопка WeryGram вставлена в список (сразу под 'Настройки чатов')!")
    elif match_privacy:
        anchor = match_privacy.group(1)
        code = code.replace(anchor, f'{anchor}\n        {werygram_btn}')
        is_button_ok = True
        print("✅ Кнопка WeryGram вставлена в список (сразу под 'Конфиденциальность')!")
    else:
        print("\n🚨🚨🚨 ОШИБКА! Не смог найти 'Настройки чатов' для якоря. 🚨🚨🚨")
        sys.exit(1)

    # 2. Обработчик клика (остается без изменений, он был правильным)
    if "case 9999:" in code:
        is_click_ok = True
        print("✅ Обработчик клика уже на месте.")
    else:
        switch_anchor = "switch (item.id) {"
        if switch_anchor in code:
            case_code = "case 9999:\n                SettingsActivity.this.presentFragment(new org.telegram.ui.WeryGramActivity());\n                break;"
            code = code.replace(switch_anchor, f"{switch_anchor}\n            {case_code}")
            is_click_ok = True
            print("✅ Обработчик клика добавлен!")

    if not is_button_ok or not is_click_ok:
        sys.exit(1)

    with open(settings_path, "w", encoding="utf-8") as f:
        f.write(code)

    print("\n🎉 ПАТЧ УСПЕШЕН! Кнопка перенесена в тело списка.")

if __name__ == "__main__":
    patch_clean_telegram()
