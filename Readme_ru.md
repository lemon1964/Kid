# Kid Project

**Kid** — учебный проект, созданный для демонстрации навыков в веб-разработке. Проект состоит из двух частей: **фронтенда** и **бэкенда**, которые взаимодействуют между собой и развернуты на **Render**.

- **Бэкенд:** [https://kid-wlsf.onrender.com](https://kid-wlsf.onrender.com)
- **Фронтенд:** [https://kid-front.onrender.com](https://kid-front.onrender.com)

### Стек технологий:
- **Backend:** Django, Django REST Framework, PostgreSQL, JWT, Stripe, ЮКасса
- **Frontend:** React, Next.js, Redux Toolkit, NextAuth, Tailwind CSS
- **CI/CD:** GitHub Actions для автоматического развертывания на Render

---

### Описание

Проект **Kid** ориентирован на обучение и развитие детей через интерактивные задания. Включает несколько типов заданий, таких как викторины, задачи с перетаскиванием элементов и графические задачи с анимациями, что помогает развивать различные навыки у детей. Все компоненты работают в рамках одного приложения и интегрированы с платёжными системами для обеспечения монетизации.

Проект включает в себя функциональность для **аутентификации пользователей**, **регистрации**, **восстановления пароля**, а также тестирования различных компонентов с интеграцией с платежными системами.

---

### Основной функционал

- **Обучающие задания для детей**:
  - **quiz_app**: Создание и управление викторинами для детей, с возможностью создания вопросов и ответов, а также задания с изображениями и музыкой для улучшения восприятия.
  - **dragdrop_app**: Задачи, связанные с перетаскиванием объектов, что помогает развивать логику и внимательность у детей.
  - **pixi_app2**: Анимационные задачи с элементами графики, которые помогают развивать зрительное восприятие и моторику.

- **Аутентификация и управление пользователями** с использованием **django-allauth** и **dj-rest-auth**, а также авторизация через JWT.
- **Интеграция с платежными системами** (Stripe, ЮКасса) для одноразовых покупок и подписок.
- **Защищенные API** с авторизацией через **JWT**.

---

### Структура проекта

Проект разделен на несколько приложений Django, каждое из которых отвечает за отдельные функциональные блоки. Основные приложения:

- **auth_app** — управление пользователями: регистрация, аутентификация, восстановление пароля.
- **brevo** — интеграция с сервисом для рассылок.
- **quiz_app** — создание и управление викторинами и вопросами.
- **dragdrop_app** — функциональность для перетаскивания элементов на странице.
- **pixi_app2** — работа с графикой и анимациями через PixiJS.
- **payment** — интеграция с платежными системами (Stripe, ЮКасса).
- **common** — универсальный API для задач и общих функций.

---

### Модели данных и их обработка

#### Quiz App, PixiTask, DragDropTask

Викторины могут быть связаны между собой, создавая цепочку тестов для пользователя. Пример модели **Quiz**:

```python
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    music = models.ForeignKey('Music', on_delete=models.SET_NULL, blank=True, null=True, related_name="quizzes")
    next_quizzes = models.ManyToManyField('self', blank=True, related_name="previous_quizzes", symmetrical=False)
    # ...
    def __str__(self):
        return self.title
```
Другие игровые модели в проекте выстроены аналогично.

#### Pixi App

Pixi приложение работает с различными типами задач, такими как геометрические фигуры и изображения в JPG и SVG форматах. Пример маршрутов для Pixi задач:

```python
router = DefaultRouter()
router.register(r"task-types", PixiTaskTypeViewSet, basename="pixi-task-type")  # ✅ Типы задач
router.register(r"tasks", PixiTaskViewSet, basename="pixi-task")  # ✅ Задачи Pixi
router.register(r"objects", PixiObjectViewSet, basename="pixi-object")  # ✅ Фигуры (геометрия)
router.register(r"svgs", PixiSVGViewSet, basename="pixi-svg")  # ✅ SVG-файлы (раскраски)
router.register(r"images", PixiImageViewSet, basename="pixi-image")  # ✅ JPG/PNG изображения
```

#### DragDrop App

В dragdrop_app сериалайзер использует другие сериалайзеры, например для контейнеров, музыки и изображений. Пример сериалайзера для **DragDrop**:

```python
class DragDropTaskSerializer(serializers.ModelSerializer):
    name = DragDropNameSerializer(read_only=True)
    music = MusicSerializer(read_only=True)
    containers = ContainerSerializer(many=True, read_only=True)
    items = ItemSerializer(many=True, read_only=True)
    background_image = serializers.SerializerMethodField()
    next_task = serializers.SerializerMethodField()
```
Эта структура позволяет легко комбинировать различные данные в одном сериализаторе, упрощая работу с взаимосвязанными моделями.

---

### Платежи

Модели для обработки платежей через **Stripe** и **ЮКассу**.

```python
class StripePayment(models.Model):
    user = models.ForeignKey(User, related_name='stripe_payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # ...
    def __str__(self):
        return f"{self.user.username} - {self.subscription_type} - {self.status}"
```

---

### Статические файлы

Для раздачи статических файлов на сервере используется **Whitenoise**. Этот инструмент позволяет эффективно обслуживать статические файлы (CSS, JavaScript, изображения и т.д.) без необходимости настроек внешнего сервера (например, Nginx).

---

### Развертывание на сервере

Для развертывания проекта используется **GitHub Actions**. Каждый пуш в ветку `main` автоматически запускает процесс развертывания на сервере **Render**. Это позволяет быстро внедрять изменения и поддерживать актуальную версию проекта.

Пример конфигурации **GitHub Actions** для автоматического развертывания:

```yaml
- name: Checkout code
  uses: actions/checkout@v3

- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.10'

- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -U -r requirements.txt

- name: Run migrations
  run: python manage.py migrate

- name: Trigger Render deployment
  run: |
    curl -X POST "https://api.render.com/v1/services/srv-${{ secrets.RENDER_SERVICE_ID }}/deploys" \
      -H "Authorization: Bearer ${{ secrets.RENDER_API_KEY }}"
```

---

### Установка и запуск

1. Клонируйте репозиторий:

```bash
git clone https://github.com/lemon1964/Kid.git
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Примените миграции:

```bash
python manage.py migrate
```

4. Запустите сервер:

```bash
python manage.py runserver
```

5. Введите тестовые данные и проверьте функциональность.
