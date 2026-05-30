#!/usr/bin/env bash
set -e

# Скрипт для автоматического git add/commit/push в origin/main
# Использование:
# chmod +x scripts/auto_push.sh
# ./scripts/auto_push.sh

echo "Проверяю статус git..."
git status --porcelain=v1 -b

if [ -z "$(git status --porcelain)" ]; then
  echo "Нет изменений для коммита."
  exit 0
fi

# Устанавливаем локальный git user при необходимости
if ! git config user.name >/dev/null 2>&1; then
  echo "Настройка git user.name -> auto-commit-bot"
  git config user.name "auto-commit-bot"
fi
if ! git config user.email >/dev/null 2>&1; then
  echo "Настройка git user.email -> autocommit@example.com"
  git config user.email "autocommit@example.com"
fi

git add .

echo "Создаю коммит..."
# Попытка закоммитить, если нет изменений в индексе, commit вернёт ненулевой код
if git commit -m "Save local changes (automated commit)"; then
  echo "Коммит создан. Пытаюсь пушить на origin/main..."
  if git push origin main; then
    echo "Push выполнен успешно."
  else
    echo "Push не удался. Проверьте доступы или выполните push вручную."
    exit 2
  fi
else
  echo "Коммит не создан (возможно, нечего коммитить)."
fi
