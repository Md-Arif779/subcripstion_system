# 🚀 Django Subscription System API

This is a Django-based subscription system that provides user registration, authentication, subscription management, and periodic exchange rate fetching using Celery. It also includes a basic Bootstrap-based frontend for plan listings.

---

## 🛠️ Local Setup Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Md-Arif779/subcripstion_system
cd subcripstion_system


# For Windows
python -m venv env
env\Scripts\activate



pip install -r requirements.txt


python manage.py makemigrations
python manage.py migrate


python manage.py createsuperuser

python manage.py runserver


celery -A subscription_system worker -l info

User Registration
{
  "username": "admin",
  "password": "1234"
}


User Login
{
  "username": "admin",
  "password": "1234"
}

GET /api/plans/
Authorization: Token your-auth-token

Subscribe to a Plan
Authorization: Token your-auth-token

{
  "plan_id": 1
}


POST /api/cancel-subscription/

POST /api/cancel-subscription/

GET /api/exchange-rate/
Authorization: Token your-auth-token