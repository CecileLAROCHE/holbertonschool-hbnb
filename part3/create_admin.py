#!/usr/bin/env python3

from app.services.facade import HBnBFacade

facade = HBnBFacade()

# Définir les infos du premier admin
admin_data = {
    "first_name": "Admin",
    "last_name": "User",
    "email": "admin@example.com",
    "password": "StrongSecurePassword",
    "is_admin": True
}

# Vérifie si l'admin existe déjà
if not facade.get_user_by_email(admin_data["email"]):
    admin = facade.create_user(admin_data, password=admin_data["password"])
    print(f"Admin created with id: {admin.id}")
else:
    print("Admin already exists")
