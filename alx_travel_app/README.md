# alx_travel_app_0x01

This project is a continuation of `alx_travel_app_0x00`, focused on implementing API development for listings and bookings using Django REST Framework.

## 🧩 Features

- Full CRUD API for Listings and Bookings
- RESTful endpoints with DRF's `ModelViewSet`
- URL routing via DRF's `DefaultRouter`
- Swagger/OpenAPI schema generation and docs
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

## 🛠 Technologies Used

- Python 3
- Django
- Django REST Framework
- drf-yasg (Swagger)

## 🧪 Testing

Test the endpoints using Postman.