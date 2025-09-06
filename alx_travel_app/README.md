# alx_travel_app_0x03

This project is a continuation of `alx_travel_app_0x00`, focused on implementing API development for listings and bookings using Django REST Framework.

## 🧩 Features

- Full CRUD API for Listings and Bookings  
- RESTful endpoints with DRF's `ModelViewSet`  
- URL routing via DRF's `DefaultRouter`  
- Swagger/OpenAPI schema generation and docs  
- Celery integration for background tasks (e.g., booking email notifications)  
- Tested with Postman  

## 🚀 API Endpoints

| Endpoint              | Method | Description              |
|-----------------------|--------|--------------------------|
| `/api/listings/`      | GET    | List all listings        |
| `/api/listings/`      | POST   | Create a new listing     |
| `/api/listings/{id}/` | PUT    | Update a listing         |
| `/api/listings/{id}/` | DELETE | Delete a listing         |
| `/api/bookings/`      | GET    | List all bookings        |
| `/api/bookings/`      | POST   | Create a new booking     |
| `/api/bookings/{id}/` | PUT    | Update a booking         |
| `/api/bookings/{id}/` | DELETE | Delete a booking         |
| `/api/payments/initiate/` | POST | Initiate a payment      |
| `/api/payments/verify/{id}/` | GET | Verify a payment      |

## 🛠 Technologies Used

- Python 3  
- Django  
- Django REST Framework  
- Celery (with RabbitMQ as the broker)  
- drf-yasg (Swagger for API docs)  
- Requests (for payment gateway integration)  

## 🧪 Testing

- Test the endpoints using Postman/Swagger  
- Confirm payment initiation and verification  
- Verify that Celery background tasks (email notifications) run correctly  

---

## 📌 Task Requirements

**Objective**  
Deploy the application to a server and ensure Swagger documentation is publicly accessible.  

**Instructions**  

1. **Deploy Application**  
   - Deploy the application to a cloud server (e.g., Render, PythonAnywhere – recommended).  
   - Ensure all necessary environment variables are configured correctly on the server.  

2. **Run Celery Worker on Server**  
   - Configure Celery to run with RabbitMQ.  
   - Verify that background tasks work as expected in the live environment.  

3. **Configure Swagger**  
   - Ensure that Swagger documentation is accessible publicly at `/swagger/` on the deployed server.  

4. **Test Deployed Application**  
   - Test all endpoints, including the email notification feature, to confirm they function correctly in production.  
