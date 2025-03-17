# Kid Project

**Kid** is an educational project created to demonstrate skills in web development. The project consists of two parts: **frontend** and **backend**, which interact with each other and are deployed on **Render**.

- **Backend:** [https://kid-wlsf.onrender.com](https://kid-wlsf.onrender.com)
- **Frontend:** [https://kid-front.onrender.com](https://kid-front.onrender.com)

### Tech Stack:
- **Backend:** Django, Django REST Framework, PostgreSQL, JWT, Stripe, YooKassa
- **Frontend:** React, Next.js, Redux Toolkit, NextAuth, Tailwind CSS
- **CI/CD:** GitHub Actions for automatic deployment on Render

---

### Description

The **Kid** project focuses on children's learning and development through interactive tasks. It includes several types of tasks such as quizzes, drag-and-drop tasks, and graphic tasks with animations, helping children develop various skills. All components work within one application and are integrated with payment systems for monetization.

The project includes functionality for **user authentication**, **registration**, **password recovery**, as well as testing different components with payment system integrations.

---

### Main Functionality

- **Educational tasks for children**:
  - **quiz_app**: Creating and managing quizzes for children, with the ability to create questions and answers, as well as tasks with images and music to enhance perception.
  - **dragdrop_app**: Tasks related to dragging and dropping objects, helping children develop logic and attention.
  - **pixi_app2**: Animation tasks with graphic elements that help develop visual perception and motor skills.

- **Authentication and user management** using **django-allauth** and **dj-rest-auth**, as well as authorization via JWT.
- **Payment system integration** (Stripe, YooKassa) for one-time purchases and subscriptions.
- **Secure APIs** with JWT authorization.

---

### Project Structure

The project is divided into several Django apps, each responsible for a specific functional block. The main apps are:

- **auth_app** — user management: registration, authentication, password recovery.
- **brevo** — integration with the Brevo service for email notifications.
- **quiz_app** — creating and managing quizzes and questions.
- **dragdrop_app** — functionality for dragging and dropping elements on the page.
- **pixi_app2** — working with graphics and animations through PixiJS.
- **payment** — integration with payment systems (Stripe, YooKassa).
- **common** — universal API for tasks and general functions.

---

### Data Models and Processing

#### Quiz App, PixiTask, DragDropTask

Quizzes can be linked together to create a sequence of tasks for the user. Example of the **Quiz** model:

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
Other game models in the project are structured similarly.

#### Pixi App

The Pixi application works with various types of tasks, such as geometric shapes and images in JPG and SVG formats. Example of routes for Pixi tasks:

```python
router = DefaultRouter()
router.register(r"task-types", PixiTaskTypeViewSet, basename="pixi-task-type")  # ✅ Task Types
router.register(r"tasks", PixiTaskViewSet, basename="pixi-task")  # ✅ Pixi Tasks
router.register(r"objects", PixiObjectViewSet, basename="pixi-object")  # ✅ Shapes (Geometry)
router.register(r"svgs", PixiSVGViewSet, basename="pixi-svg")  # ✅ SVG Files (Coloring)
router.register(r"images", PixiImageViewSet, basename="pixi-image")  # ✅ JPG/PNG Images
```

#### DragDrop App

In **dragdrop_app**, the serializer uses other serializers, for example for containers, music, and images. Example serializer for **DragDrop**:

```python
class DragDropTaskSerializer(serializers.ModelSerializer):
    name = DragDropNameSerializer(read_only=True)
    music = MusicSerializer(read_only=True)
    containers = ContainerSerializer(many=True, read_only=True)
    items = ItemSerializer(many=True, read_only=True)
    background_image = serializers.SerializerMethodField()
    next_task = serializers.SerializerMethodField()
```
This structure allows easy combination of different data in a single serializer, simplifying working with interrelated models.

---

### Payments

Models for processing payments via **Stripe** and **YooKassa**.

```python
class StripePayment(models.Model):
    user = models.ForeignKey(User, related_name='stripe_payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # ...
    def __str__(self):
        return f"{self.user.username} - {self.subscription_type} - {self.status}"
```

---

### Static Files

**Whitenoise** is used for serving static files on the server. This tool allows efficient serving of static files (CSS, JavaScript, images, etc.) without the need for external server configurations (e.g., Nginx).

---

### Deployment on the Server

The project is deployed using **GitHub Actions**. Each push to the `main` branch automatically triggers the deployment process on the **Render** server. This ensures quick implementation of changes and keeps the project up-to-date.

Example **GitHub Actions** configuration for automatic deployment:

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

### Installation and Run

1. Clone the repository:

```bash
git clone https://github.com/lemon1964/Kid.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Apply migrations:

```bash
python manage.py migrate
```

4. Run the server:

```bash
python manage.py runserver
```

5. Add test data and check the functionality.
