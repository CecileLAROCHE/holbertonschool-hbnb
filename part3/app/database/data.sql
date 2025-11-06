-- ===========================
-- Initial Data
-- ===========================

-- Admin user
INSERT INTO user (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$QKItT7oZUJghJhFZKoKp7e1h8g3HqYAhO0k4vI8qIfAok9O9T8weK', -- bcrypt hash de 'admin1234'
    TRUE
);

-- Amenities
INSERT INTO amenity (id, name) VALUES
    ('a1f1f1b2-1234-4a56-9876-1b2c3d4e5f6a', 'WiFi'),
    ('b2e2e2c3-2345-4b67-9876-2c3d4e5f6a7b', 'Swimming Pool'),
    ('c3d3d3d4-3456-4c78-9876-3d4e5f6a7b8c', 'Air Conditioning');
