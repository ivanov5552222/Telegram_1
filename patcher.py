import os
import re
import sys

def patch_clean_telegram():
    settings_path = "TMessagesProj/src/main/java/org/telegram/ui/SettingsActivity.java"
    
    if not os.path.exists(settings_path):
        print(f"🚨 КРИТИЧЕСКАЯ ОШИБКА: Файл не найден: {settings_path}")
        sys.exit(1)

    print("⏳ Авто-патчер WeryGram начал работу...")

    with open(settings_path, "r", encoding="utf-8") as f:
        code = f.read()

    # 0. ОЧИСТКА: Полностью вычищаем старые кейсы 9999, чтобы избежать дублирования кода
    code = re.sub(r'case 9999:.*?break;', '', code, flags=re.DOTALL)

    is_button_ok = False
    is_click_ok = False

    # Базовое объявление нашей кнопки в списке
    werygram_btn = 'items.add(SettingCell.Factory.of(9999, 0xFF55CA47, 0xFF27B434, R.drawable.msg_settings, "WeryGram"));'

    # 1. Проверяем/вставляем кнопку в меню настроек
    if "9999" in code and "SettingCell.Factory.of" in code:
        is_button_ok = True
    else:
        match_chat = re.search(r'(items\.add\(.*?[cC]hat[sS]ettings.*?\);)', code)
        if match_chat:
            anchor = match_chat.group(1)
            code = code.replace(anchor, f'{anchor}\n        {werygram_btn}')
            is_button_ok = True
            print("✅ Кнопка WeryGram успешно добавлена под 'Настройки чатов'.")

    # 2. Мощный инжект диалогового окна с кнопками Вкл/Выкл прямо в switch(item.id)
    switch_anchor = "switch (item.id) {"
    if switch_anchor in code:
        # Пишем чистый Java-код для диалогового окна и сохранения состояния в SharedPreferences
        dialog_code = """case 9999:
            if (SettingsActivity.this.getParentActivity() != null) {
                android.app.AlertDialog.Builder builder = new android.app.AlertDialog.Builder(SettingsActivity.this.getParentActivity());
                
                // Читаем текущий статус из памяти для заголовка
                boolean isEnabled = SettingsActivity.this.getParentActivity().getSharedPreferences("werygram_settings", android.content.Context.MODE_PRIVATE).getBoolean("visual_premium", false);
                builder.setTitle("WeryGram Premium (" + (isEnabled ? "Включен" : "Выключен") + ")");
                
                // Твой текст описания функции
                builder.setMessage("Premium данная функция включает телеграм премиум визуально");
                
                // Кнопка ВКЛЮЧИТЬ
                builder.setPositiveButton("Включить", new android.content.DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(android.content.DialogInterface dialog, int which) {
                        SettingsActivity.this.getParentActivity().getSharedPreferences("werygram_settings", android.content.Context.MODE_PRIVATE).edit().putBoolean("visual_premium", true).apply();
                        android.widget.Toast.makeText(SettingsActivity.this.getParentActivity(), "Визуальный Premium успешно ВКЛЮЧЕН! Перезапустите приложение.", android.widget.Toast.LENGTH_SHORT).show();
                    }
                });
                
                // Кнопка ВЫКЛЮЧИТЬ
                builder.setNegativeButton("Выключить", new android.content.DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(android.content.DialogInterface dialog, int which) {
                        SettingsActivity.this.getParentActivity().getSharedPreferences("werygram_settings", android.content.Context.MODE_PRIVATE).edit().putBoolean("visual_premium", false).apply();
                        android.widget.Toast.makeText(SettingsActivity.this.getParentActivity(), "Визуальный Premium ВЫКЛЮЧЕН!", android.widget.Toast.LENGTH_SHORT).show();
                    }
                });
                
                builder.show();
            }
            break;"""
        
        code = code.replace(switch_anchor, f"{switch_anchor}\n            {dialog_code}")
        is_click_ok = True
        print("✅ Интерактивное диалоговое окно успешно вшито в обработчик кликов!")

    if not is_button_ok or not is_click_ok:
        print("🚨 Ошибка применения патча.")
        sys.exit(1)

    with open(settings_path, "w", encoding="utf-8") as f:
        f.write(code)

    print("\n🎉 ВСЁ ГОТОВО! Логика полностью перенесена в главный файл настроек.")

if __name__ == "__main__":
    patch_clean_telegram()
