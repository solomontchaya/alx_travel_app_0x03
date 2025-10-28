# ALX Travel App 0x02

## Overview

`alx_travel_app_0x02` is a Django-based travel booking application with **Chapa payment integration**. Users can make bookings and pay securely through the Chapa payment gateway. The system supports initiating payments, verifying transactions, and tracking payment status.

---

## Features

* Booking creation and management
* Secure payment processing with Chapa
* Payment status tracking (`Pending`, `Completed`, `Failed`)
* Email confirmation for successful payments (via Celery)
* Sandbox testing for safe development

---

## Project Structure

```
alx_travel_app_0x02/
├── alx_travel_app/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── listings/
│   ├── models.py      # Payment and Booking models
│   ├── views.py       # Payment API endpoints
│   ├── tasks.py       # Celery email tasks
│   └── ...
├── manage.py
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Clone Project

```bash
git clone https://github.com/yourusername/alx_travel_app_0x02.git
cd alx_travel_app_0x02
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your_django_secret_key
CHAPA_SECRET_KEY=your_chapa_secret_key
DATABASE_URL=your_database_url
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start Development Server

```bash
python manage.py runserver
```

---

## Chapa Payment Integration

### Initiate Payment

**Endpoint:** `POST /api/initiate-payment/`
**Payload Example:**

```json
{
  "booking_reference": "BK123456",
  "amount": 500,
  "currency": "ETB",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
```

**Response:**

```json
{
  "payment_link": "https://checkout.chapa.co/checkout/payment/..."
}
```

---

### Verify Payment

**Endpoint:** `GET /api/verify-payment/?tx_ref=BK123456`

**Response:**

```json
{
  "status": "Completed"
}
```

Payment statuses:

* `Pending` – Payment initialized but not completed
* `Completed` – Payment successful
* `Failed` – Payment failed or canceled

---

## Email Notifications

* Successful payments trigger an email confirmation using **Celery**.
* Make sure Celery is running for background tasks:

```bash
celery -A alx_travel_app worker -l info
```

---

## Testing

1. Use **Chapa sandbox credentials** for testing payments.
2. Initiate a payment via the `/api/initiate-payment/` endpoint.
3. Complete payment in the sandbox environment.
4. Verify payment using `/api/verify-payment/`.
5. Confirm that the payment status updates in the Django admin or `Payment` model.

---

## Screenshots / Logs

* Include screenshots showing:

  * Payment initiation
  * Redirect to Chapa checkout
  * Payment verification
  * Updated status in Payment model

