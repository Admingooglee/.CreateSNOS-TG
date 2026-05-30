#!/bin/bash
# 🚀 SNOSER-TG 2.0+ - БЫСТРЫЕ КОМАНДЫ
# ====================================

echo "
╔════════════════════════════════════════════════════════════╗
║         SNOSER-TG 2.0+ - БЫСТРЫЕ КОМАНДЫ                ║
╚════════════════════════════════════════════════════════════╝
"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}\n"

echo -e "${GREEN}📋 ИНФОРМАЦИОННЫЕ КОМАНДЫ:${NC}"
echo ""
echo "1️⃣  Посмотреть структуру проекта:"
echo -e "   ${YELLOW}python3 PROJECT_STRUCTURE.py${NC}"
echo ""
echo "2️⃣  Прочитать финальные инструкции:"
echo -e "   ${YELLOW}python3 FINAL_INSTRUCTIONS.py${NC}"
echo ""
echo "3️⃣  Посмотреть документацию по прокси:"
echo -e "   ${YELLOW}python3 PROXY_DOCS.py${NC}"
echo ""
echo "4️⃣  Быстрый старт:"
echo -e "   ${YELLOW}python3 QUICKSTART.py${NC}"
echo ""
echo "5️⃣  Проверить статус украинских данных:"
echo -e "   ${YELLOW}python3 check_ukrainian_data.py${NC}"
echo ""

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}\n"

echo -e "${GREEN}🔧 ТЕСТИРОВАНИЕ:${NC}"
echo ""
echo "6️⃣  Протестировать генератор прокси:"
echo -e "   ${YELLOW}python3 proxy_generator.py${NC}"
echo ""
echo "7️⃣  Сгенерировать украинские данные:"
echo -e "   ${YELLOW}python3 ukraine_senders_1200.py${NC}"
echo ""

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}\n"

echo -e "${GREEN}🚀 ОСНОВНЫЕ КОМАНДЫ:${NC}"
echo ""
echo "8️⃣  ЗАПУСТИТЬ ОСНОВНОЙ СКРИПТ:"
echo -e "   ${RED}python3 NewLinks.py${NC}"
echo ""
echo "9️⃣  Просмотреть логи в реальном времени:"
echo -e "   ${YELLOW}tail -f logs/snoser.log${NC}"
echo ""
echo "🔟 Просмотреть успешные отправки:"
echo -e "   ${YELLOW}grep '✓' logs/snoser.log${NC}"
echo ""
echo "1️⃣1️⃣ Просмотреть ошибки:"
echo -e "   ${YELLOW}grep '✗\\|ERROR' logs/snoser.log${NC}"
echo ""

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}\n"

echo -e "${GREEN}📊 ФАЙЛОВЫЕ КОМАНДЫ:${NC}"
echo ""
echo "1️⃣2️⃣ Список всех файлов:"
echo -e "   ${YELLOW}ls -la${NC}"
echo ""
echo "1️⃣3️⃣ Размер проекта:"
echo -e "   ${YELLOW}du -sh .${NC}"
echo ""
echo "1️⃣4️⃣ Количество строк в основном скрипте:"
echo -e "   ${YELLOW}wc -l NewLinks.py${NC}"
echo ""
echo "1️⃣5️⃣ Количество строк в генераторе прокси:"
echo -e "   ${YELLOW}wc -l proxy_generator.py${NC}"
echo ""

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}\n"

echo -e "${GREEN}🐍 PYTHON КОМАНДЫ:${NC}"
echo ""
echo "1️⃣6️⃣ Проверить версию Python:"
echo -e "   ${YELLOW}python3 --version${NC}"
echo ""
echo "1️⃣7️⃣ Проверить установленные пакеты:"
echo -e "   ${YELLOW}pip3 list${NC}"
echo ""
echo "1️⃣8️⃣ Синтаксис Python файла:"
echo -e "   ${YELLOW}python3 -m py_compile NewLinks.py${NC}"
echo ""

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}\n"

echo -e "${GREEN}📈 СТАТИСТИКА:${NC}"
echo ""
echo "1️⃣9️⃣ Количество отправителей:"
echo -e "   ${YELLOW}python3 -c \"import json; f=open('data/ukraine_senders_1200.json'); d=json.load(f); print(f'📧 {len(d)} отправителей')\"${NC}"
echo ""
echo "2️⃣0️⃣ Размер файла с отправителями:"
echo -e "   ${YELLOW}ls -lh data/ukraine_senders_1200.json${NC}"
echo ""
echo "2️⃣1️⃣ Размер логов:"
echo -e "   ${YELLOW}ls -lh logs/snoser.log${NC}"
echo ""

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}\n"

echo -e "${GREEN}🎯 РЕКОМЕНДУЕМЫЙ ПОРЯДОК:${NC}"
echo ""
echo "Первый запуск:"
echo "  1. python3 PROJECT_STRUCTURE.py    (информация)"
echo "  2. python3 FINAL_INSTRUCTIONS.py   (инструкции)"
echo "  3. python3 proxy_generator.py      (тест)"
echo "  4. python3 check_ukrainian_data.py (проверка)"
echo "  5. python3 NewLinks.py             (запуск!)"
echo ""

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}\n"

echo -e "${GREEN}⚡ БЫСТРЫЙ СТАРТ (одна команда):${NC}"
echo ""
echo -e "   ${RED}python3 NewLinks.py${NC}"
echo ""

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}\n"

echo -e "${GREEN}💾 ФАЙЛЫ ПРОЕКТА:${NC}"
echo ""
echo "Основные:"
echo "  ✓ NewLinks.py - главный скрипт"
echo "  ✓ proxy_generator.py - генератор прокси"
echo "  ✓ utils.py - утилиты"
echo ""
echo "Документация:"
echo "  ✓ PROXY_DOCS.py"
echo "  ✓ FINAL_INSTRUCTIONS.py"
echo "  ✓ PROJECT_STRUCTURE.py"
echo "  ✓ COMPLETION_REPORT.txt"
echo ""
echo "Данные:"
echo "  ✓ data/ukraine_senders_1200.json"
echo "  ✓ data/receivers.json"
echo "  ✓ config/settings.json"
echo ""
echo "Логи:"
echo "  ✓ logs/snoser.log"
echo ""

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}\n"

echo -e "${GREEN}🎉 ВСЕ ГОТОВО!${NC}"
echo ""
echo -e "Начните с: ${RED}python3 NewLinks.py${NC}"
echo ""

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}\n"
