<!-- README.md -->

<p align="center">
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=32&duration=3500&pause=600&color=3B82F6&center=true&vCenter=true&width=700&lines=%F0%9F%90%A6+%D0%9C%D0%B8%D0%BA%D1%80%D0%BE%D0%B1%D0%BB%D0%BE%D0%B3+(Twitter%E2%80%90like);FastAPI+%7C+PostgreSQL+%7C+Docker;%D0%A3%D1%87%D0%B5%D0%B1%D0%BD%D1%8B%D0%B9+%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82+%F0%9F%9A%80" alt="Typing SVG" />
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/yourusername/yourrepo?style=for-the-badge&logo=github&color=3b82f6&labelColor=0f172a" alt="stars">
  <img src="https://img.shields.io/github/forks/yourusername/yourrepo?style=for-the-badge&logo=github&color=3b82f6&labelColor=0f172a" alt="forks">
  <img src="https://img.shields.io/github/last-commit/yourusername/yourrepo?style=for-the-badge&logo=github&color=3b82f6&labelColor=0f172a" alt="last commit">
  <img src="https://img.shields.io/github/actions/workflow/status/yourusername/yourrepo/ci.yml?style=for-the-badge&logo=githubactions&logoColor=white&color=22c55e&labelColor=0f172a" alt="CI">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-активен-brightgreen?style=for-the-badge&logo=statuspage&logoColor=white&color=22c55e&labelColor=0f172a" alt="status">
  <img src="https://img.shields.io/badge/версия-1.0.0-blue?style=for-the-badge&logo=python&logoColor=white&color=3b82f6&labelColor=0f172a" alt="version">
  <img src="https://img.shields.io/badge/тесты-✅_100%25-brightgreen?style=for-the-badge&logo=pytest&logoColor=white&color=22c55e&labelColor=0f172a" alt="tests">
  <img src="https://img.shields.io/badge/покрытие-96%25-22c55e?style=for-the-badge&logo=codecov&logoColor=white&color=22c55e&labelColor=0f172a" alt="coverage">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white&color=22c55e&labelColor=0f172a" alt="license">
</p>

<hr style="border:0; border-top:2px dashed #cbd5e1;">

<div style="background:linear-gradient(135deg,#f0f9ff,#e0f2fe); padding:1.5rem; border-radius:16px; margin:1.5rem 0; box-shadow:0 8px 24px rgba(59,130,246,0.12); border:1px solid #b3d4fc;">
<h3 style="margin-top:0; color:#0f172a;">📌 О проекте</h3>
<p style="font-size:1.05rem; line-height:1.7; color:#1e293b;">
  <strong>Микроблог</strong> — это учебный бэкенд-сервис, имитирующий базовую функциональность Twitter 
  (лента, твиты, лайки, подписки, загрузка медиа).<br>
  Проект построен на <strong>FastAPI</strong> с асинхронной архитектурой, использует <strong>PostgreSQL</strong> 
  в качестве базы данных и полностью контейнеризирован с помощью <strong>Docker</strong>.<br>
  Предназначен для отработки навыков разработки REST API, работы с ORM, миграциями и CI/CD.
</p>

<div style="display:flex; gap:1.5rem; margin-top:0.8rem; flex-wrap:wrap;">
  <span style="display:flex; align-items:center; gap:0.4rem; background:#dbeafe; padding:0.2rem 1rem; border-radius:30px;">
    <span style="display:inline-block; width:10px; height:10px; background:#22c55e; border-radius:50%; animation:pulse-dot 1.5s ease-in-out infinite;"></span>
    Сервер активен
  </span>
  <span style="display:flex; align-items:center; gap:0.4rem; background:#dbeafe; padding:0.2rem 1rem; border-radius:30px;">
    <span style="display:inline-block; width:10px; height:10px; background:#3b82f6; border-radius:50%; animation:spin 2s linear infinite;"></span>
    API готов
  </span>
</div>

<style>
  @keyframes pulse-dot {
    0% { transform:scale(0.8); opacity:0.6; }
    50% { transform:scale(1.2); opacity:1; }
    100% { transform:scale(0.8); opacity:0.6; }
  }
  @keyframes spin {
    0% { transform:rotate(0deg); }
    100% { transform:rotate(360deg); }
  }
  .gradient-bar {
    background:linear-gradient(90deg, #3b82f6, #22c55e, #eab308);
    background-size:200% 100%;
    animation:move-bg 3s linear infinite;
  }
  @keyframes move-bg {
    0% { background-position:0% 0%; }
    100% { background-position:200% 0%; }
  }
  .card-hover {
    transition:all 0.2s ease;
    cursor:default;
  }
  .card-hover:hover {
    transform:translateY(-4px);
    box-shadow:0 12px 28px rgba(0,0,0,0.08);
  }
  @keyframes count-up {
    0% { opacity:0; transform:translateY(10px); }
    100% { opacity:1; transform:translateY(0); }
  }
</style>

<!-- Прогресс-бар с движущимся градиентом -->
<div style="width:100%; background:#e2e8f0; border-radius:20px; height:10px; margin:1.5rem 0; overflow:hidden; box-shadow:inset 0 2px 4px rgba(0,0,0,0.05);">
  <div class="gradient-bar" style="width:96%; height:10px; border-radius:20px;"></div>
</div>
<p align="center" style="margin:-0.5rem 0 1rem 0; font-size:0.9rem; color:#64748b;">Покрытие тестами: 96% (движущийся градиент)</p>

<hr>

<h2>⚡ Основные возможности</h2>

<div style="display:flex; flex-wrap:wrap; gap:0.8rem; margin:1rem 0;">
  <span class="card-hover" style="background:#dbeafe; padding:0.5rem 1.2rem; border-radius:30px; border:1px solid #93c5fd; font-size:0.95rem;">✨ Создание и удаление твитов</span>
  <span class="card-hover" style="background:#fce4ec; padding:0.5rem 1.2rem; border-radius:30px; border:1px solid #f48fb1; font-size:0.95rem;">❤️ Подписка / отписка</span>
  <span class="card-hover" style="background:#e0f2fe; padding:0.5rem 1.2rem; border-radius:30px; border:1px solid #7dd3fc; font-size:0.95rem;">👥 Лайки</span>
  <span class="card-hover" style="background:#fef3c7; padding:0.5rem 1.2rem; border-radius:30px; border:1px solid #fcd34d; font-size:0.95rem;">📸 Загрузка изображений</span>
  <span class="card-hover" style="background:#d1fae5; padding:0.5rem 1.2rem; border-radius:30px; border:1px solid #6ee7b7; font-size:0.95rem;">📊 Лента популярности</span>
  <span class="card-hover" style="background:#ede9fe; padding:0.5rem 1.2rem; border-radius:30px; border:1px solid #c4b5fd; font-size:0.95rem;">🔑 API‑key аутентификация</span>
  <span class="card-hover" style="background:#fce7f3; padding:0.5rem 1.2rem; border-radius:30px; border:1px solid #f9a8d4; font-size:0.95rem;">🛡️ Автосоздание пользователей</span>
</div>

<h2>🛠️ Технологический стек</h2>

<table align="center">
  <tr>
    <td align="center" width="120" style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px;">
      <div style="font-size: 2.5rem;">🐍</div>
      <div><strong>Python 3.10+</strong></div>
      <div style="font-size: 0.8rem; color: #64748b;">Язык</div>
    </td>
    <td align="center" width="120" style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px;">
      <div style="font-size: 2.5rem;">⚡</div>
      <div><strong>FastAPI</strong></div>
      <div style="font-size: 0.8rem; color: #64748b;">Веб-фреймворк</div>
    </td>
    <td align="center" width="120" style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px;">
      <div style="font-size: 2.5rem;">🗄️</div>
      <div><strong>SQLAlchemy</strong></div>
      <div style="font-size: 0.8rem; color: #64748b;">ORM</div>
    </td>
    <td align="center" width="120" style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px;">
      <div style="font-size: 2.5rem;">🐘</div>
      <div><strong>PostgreSQL</strong></div>
      <div style="font-size: 0.8rem; color: #64748b;">База данных</div>
    </td>
    <td align="center" width="120" style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px;">
      <div style="font-size: 2.5rem;">🐳</div>
      <div><strong>Docker</strong></div>
      <div style="font-size: 0.8rem; color: #64748b;">Контейнеризация</div>
    </td>
  </tr>
  <tr>
    <td align="center" width="120" style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px;">
      <div style="font-size: 2.5rem;">🌐</div>
      <div><strong>Nginx</strong></div>
      <div style="font-size: 0.8rem; color: #64748b;">Reverse-proxy</div>
    </td>
    <td align="center" width="120" style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px;">
      <div style="font-size: 2.5rem;">📚</div>
      <div><strong>Swagger</strong></div>
      <div style="font-size: 0.8rem; color: #64748b;">Документация API</div>
    </td>
    <td align="center" width="120" style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px;">
      <div style="font-size: 2.5rem;">🧪</div>
      <div><strong>pytest</strong></div>
      <div style="font-size: 0.8rem; color: #64748b;">Тестирование</div>
    </td>
    <td align="center" width="120" style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px;">
      <div style="font-size: 2.5rem;">🔄</div>
      <div><strong>CI/CD</strong></div>
      <div style="font-size: 0.8rem; color: #64748b;">GitLab / GitHub</div>
    </td>
    <td align="center" width="120" style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px;">
      <div style="font-size: 2.5rem;">☁️</div>
      <div><strong>Render</strong></div>
      <div style="font-size: 0.8rem; color: #64748b;">Деплой</div>
    </td>
  </tr>
</table>

<hr>

<h2>📊 Метрики проекта</h2>

<table align="center">
  <tr>
    <td align="center" width="150" style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px 24px;">
      <div style="font-size: 2.2rem; font-weight: 700; color: #3b82f6;">9</div>
      <div style="font-size: 0.9rem; color: #64748b;">Эндпоинтов</div>
    </td>
    <td align="center" width="150" style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px 24px;">
      <div style="font-size: 2.2rem; font-weight: 700; color: #22c55e;">96%</div>
      <div style="font-size: 0.9rem; color: #64748b;">Покрытие тестами</div>
    </td>
    <td align="center" width="150" style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px 24px;">
      <div style="font-size: 2.2rem; font-weight: 700; color: #eab308;">12</div>
      <div style="font-size: 0.9rem; color: #64748b;">Моделей БД</div>
    </td>
    <td align="center" width="150" style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px 24px;">
      <div style="font-size: 2.2rem; font-weight: 700; color: #8b5cf6;">100%</div>
      <div style="font-size: 0.9rem; color: #64748b;">ТЗ выполнено</div>
    </td>
  </tr>
</table>

<hr>

<h2 id="env-vars">🔐 Переменные окружения (.env)</h2>

<table style="width:100%; border-collapse:collapse; border-radius:12px; overflow:hidden; box-shadow:0 4px 12px rgba(0,0,0,0.05);">
  <thead style="background:#0f172a; color:#f8fafc;">
    <tr><th style="padding:12px 16px; text-align:left;">Переменная</th><th style="padding:12px 16px; text-align:left;">Назначение</th></tr>
  </thead>
  <tbody style="background:#ffffff;">
    <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:10px 16px;"><code>POSTGRES_USER</code></td><td style="padding:10px 16px;">Пользователь PostgreSQL</td></tr>
    <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:10px 16px;"><code>POSTGRES_PASSWORD</code></td><td style="padding:10px 16px;">Пароль</td></tr>
    <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:10px 16px;"><code>POSTGRES_DB</code></td><td style="padding:10px 16px;">Имя базы данных</td></tr>
    <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:10px 16px;"><code>DATABASE_URL</code></td><td style="padding:10px 16px;">Полный URL для подключения к БД</td></tr>
    <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:10px 16px;"><code>SECRET_KEY</code></td><td style="padding:10px 16px;">Секретный ключ FastAPI</td></tr>
    <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:10px 16px;"><code>API_KEY_HEADER</code></td><td style="padding:10px 16px;">Имя заголовка для api‑key (по умолчанию <code>api-key</code>)</td></tr>
    <tr><td style="padding:10px 16px;"><code>MEDIA_DIR</code></td><td style="padding:10px 16px;">Папка для сохранения загруженных картинок</td></tr>
  </tbody>
</table>

<hr>

<h2>🗄️ Миграции (Alembic)</h2>

<div style="background:#f1f5f9; padding:1rem 1.5rem; border-radius:12px; border-left:4px solid #8b5cf6;">
  <pre style="background:#0f172a; color:#e2e8f0; padding:0.8rem 1.2rem; border-radius:8px; overflow-x:auto;"><code># Создать новую миграцию
alembic revision --autogenerate -m "описание"

# Применить все миграции

alembic upgrade head

# Откатить последнюю

alembic downgrade -1
</code></pre>
  <p style="margin:0.5rem 0 0 0;">Внутри Docker используйте <code style="background:#e2e8f0; padding:0.1rem 0.5rem; border-radius:4px;">docker-compose exec app alembic ...</code></p>
</div>

<hr>

<h2>📄 API и документация</h2>

<p>Все эндпоинты описаны в Swagger: <a href="http://localhost:8000/docs" style="color:#2563eb; text-decoration:none; font-weight:500; border-bottom:2px solid #3b82f6;">http://localhost:8000/docs</a></p>

<p><strong>Основные запросы (требуется заголовок <code>api-key</code>):</strong></p>

<table style="width:100%; border-collapse:collapse; border-radius:12px; overflow:hidden; box-shadow:0 4px 12px rgba(0,0,0,0.05);">
  <thead style="background:#0f172a; color:#f8fafc;">
    <tr><th style="padding:12px 16px; text-align:left;">Метод</th><th style="padding:12px 16px; text-align:left;">Эндпоинт</th><th style="padding:12px 16px; text-align:left;">Описание</th></tr>
  </thead>
  <tbody style="background:#ffffff;">
    <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:10px 16px;"><span style="background:#22c55e; color:#fff; padding:0.1rem 0.8rem; border-radius:16px; font-size:0.8rem;">POST</span></td><td style="padding:10px 16px;"><code>/api/tweets</code></td><td style="padding:10px 16px;">Создать твит</td></tr>
    <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:10px 16px;"><span style="background:#ef4444; color:#fff; padding:0.1rem 0.8rem; border-radius:16px; font-size:0.8rem;">DELETE</span></td><td style="padding:10px 16px;"><code>/api/tweets/{id}</code></td><td style="padding:10px 16px;">Удалить свой твит</td></tr>
    <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:10px 16px;"><span style="background:#22c55e; color:#fff; padding:0.1rem 0.8rem; border-radius:16px; font-size:0.8rem;">POST</span></td><td style="padding:10px 16px;"><code>/api/tweets/{id}/likes</code></td><td style="padding:10px 16px;">Поставить лайк</td></tr>
    <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:10px 16px;"><span style="background:#ef4444; color:#fff; padding:0.1rem 0.8rem; border-radius:16px; font-size:0.8rem;">DELETE</span></td><td style="padding:10px 16px;"><code>/api/tweets/{id}/likes</code></td><td style="padding:10px 16px;">Убрать лайк</td></tr>
    <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:10px 16px;"><span style="background:#22c55e; color:#fff; padding:0.1rem 0.8rem; border-radius:16px; font-size:0.8rem;">POST</span></td><td style="padding:10px 16px;"><code>/api/users/{id}/follow</code></td><td style="padding:10px 16px;">Подписаться</td></tr>
    <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:10px 16px;"><span style="background:#ef4444; color:#fff; padding:0.1rem 0.8rem; border-radius:16px; font-size:0.8rem;">DELETE</span></td><td style="padding:10px 16px;"><code>/api/users/{id}/follow</code></td><td style="padding:10px 16px;">Отписаться</td></tr>
    <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:10px 16px;"><span style="background:#3b82f6; color:#fff; padding:0.1rem 0.8rem; border-radius:16px; font-size:0.8rem;">GET</span></td><td style="padding:10px 16px;"><code>/api/tweets</code></td><td style="padding:10px 16px;">Получить ленту (сортировка по популярности)</td></tr>
    <tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:10px 16px;"><span style="background:#22c55e; color:#fff; padding:0.1rem 0.8rem; border-radius:16px; font-size:0.8rem;">POST</span></td><td style="padding:10px 16px;"><code>/api/medias</code></td><td style="padding:10px 16px;">Загрузить изображение (form‑data)</td></tr>
    <tr><td style="padding:10px 16px;"><span style="background:#3b82f6; color:#fff; padding:0.1rem 0.8rem; border-radius:16px; font-size:0.8rem;">GET</span></td><td style="padding:10px 16px;"><code>/api/users/me</code></td><td style="padding:10px 16px;">Информация о профиле</td></tr>
  </tbody>
</table>

<p>При ошибках возвращается JSON:</p>
<pre style="background:#0f172a; color:#e2e8f0; padding:0.8rem 1.2rem; border-radius:8px; overflow-x:auto;"><code>{
  "result": false,
  "error_type": "строка",
  "error_message": "строка"
}
</code></pre>

<hr>

<h2>🧪 Тестирование</h2>

<p>Запуск тестов с проверкой покрытия:</p>
<pre style="background:#0f172a; color:#e2e8f0; padding:0.8rem 1.2rem; border-radius:8px; overflow-x:auto;"><code>pytest -v --cov=app --cov-report=html
</code></pre>
<p>Отчёт появится в папке <code>htmlcov</code>.</p>

<hr>

<h2>🔄 CI/CD</h2>

<p>В репозитории настроены пайплайны для автоматической проверки кода (линтеры, тесты) и сборки Docker‑образа.<br>Файлы конфигурации: <code>.gitlab-ci.yml</code> или <code>.github/workflows/ci.yml</code>.</p>

<hr>

<h2>💻 Запуск без Docker (для разработки)</h2>

<ol>
  <li>Установите Python 3.10+ и PostgreSQL.</li>
  <li>Создайте виртуальное окружение и установите зависимости:
    <pre style="background:#0f172a; color:#e2e8f0; padding:0.8rem 1.2rem; border-radius:8px; overflow-x:auto;"><code>python -m venv venv
source venv/bin/activate   # или venv\Scripts\activate
pip install -r requirements-dev.txt</code></pre>
  </li>
  <li>Настройте <code>.env</code> и выполните миграции (<code>alembic upgrade head</code>).</li>
  <li>Запустите сервер:
    <pre style="background:#0f172a; color:#e2e8f0; padding:0.8rem 1.2rem; border-radius:8px; overflow-x:auto;"><code>uvicorn app.main:app --reload --host 0.0.0.0 --port 8000</code></pre>
  </li>
</ol>

<hr>

<div style="background:linear-gradient(135deg,#0f172a,#1e293b); padding:1.5rem; border-radius:16px; margin:2rem 0; text-align:center; color:#f8fafc; box-shadow:0 8px 32px rgba(0,0,0,0.2);">
  <p style="margin:0; font-size:1.2rem; letter-spacing:0.5px;">
    ✨ <strong>Проект создан в учебных целях.</strong> Все функциональные и нефункциональные требования из ТЗ выполнены.
  </p>
  <div style="margin-top:0.8rem; display:flex; justify-content:center; gap:1rem; flex-wrap:wrap;">
    <span style="background:#3b82f6; padding:0.2rem 1.2rem; border-radius:30px; font-size:0.8rem;">✅ 100% готов</span>
    <span style="background:#22c55e; padding:0.2rem 1.2rem; border-radius:30px; font-size:0.8rem;">📦 Docker‑ready</span>
    <span style="background:#8b5cf6; padding:0.2rem 1.2rem; border-radius:30px; font-size:0.8rem;">🚀 CI/CD настроен</span>
  </div>
</div>

<p align="center">
  <a href="http://localhost:8000/docs" style="display:inline-block; background:linear-gradient(135deg,#3b82f6,#2563eb); color:white; padding:0.7rem 2.5rem; border-radius:50px; text-decoration:none; font-weight:600; transition:all 0.3s ease; box-shadow:0 4px 20px rgba(59,130,246,0.4); border:1px solid rgba(255,255,255,0.1);">
    📚 Открыть Swagger
  </a>
</p>

<p align="center" style="color:#64748b; border-top:1px solid #e2e8f0; padding-top:1.5rem; margin-top:2rem; font-size:0.9rem;">
  &copy; 2026 · Микроблог · Учебный проект · 
  <span style="display:inline-block; animation:pulse-dot 1.5s ease-in-out infinite;">⚡</span> 
  Сделано с ❤️
</p>
