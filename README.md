# Restaurant Table Booking System

## Overview
This system provides a platform for managing restaurant table reservations. It has two types of users:

1. **Admin**: Manages tables in the system.
   - Username: `admin`
   - Password: `admin123`

2. **User**: Reserves or cancels table bookings.
   - Username: `user`
   - Password: `user123`

The application is deployed at the following URL:
[Restaurant Table Booking System](https://restaurant-table-booking-system-gfcs.onrender.com/)

## Features

### Admin Routes
1. **View All Tables**
   - **Endpoint**: `GET /admin/tables`
   - **Description**: Displays all tables with their details.
   - **How to Access**: Navigate to `/admin/tables` after logging in as an admin.

2. **Add a New Table**
   - **Endpoint**: `POST /admin/tables`
   - **Description**: Allows the admin to add a new table with details like table number and capacity.
  

3. **Update Table Details**
   - **Endpoint**: `PUT /admin/tables/<table_id>`
   - **Description**: Updates the details of a specific table.
   - **How to Access**: Navigate to `/admin/tables`, select a table, and submit the updated details.

4. **Delete a Table**
   - **Endpoint**: `DELETE /admin/tables/<table_id>`
   - **Description**: Removes a specific table from the system.
   - **How to Access**: Navigate to `/admin/tables`, select the table to delete, and confirm the action.

### User Routes
1. **View Available Tables**
   - **Endpoint**: `GET /tables`
   - **Description**: Displays all available (unreserved) tables.
   - **How to Access**: Navigate to `/tables` after logging in as a user.

2. **Reserve a Table**
   - **Endpoint**: `POST /tables/reserve`
   - **Description**: Allows the user to reserve a specific table.
   - **How to Access**: Use the form displayed on the `/tables` page.

3. **Cancel Reservation**
   - **Endpoint**: `DELETE /tables/cancel`
   - **Description**: Cancels the user’s current reservation.
   - **How to Access**: Navigate to `/tables/cancel` and confirm the cancellation.

## Getting Started

### Steps to Use the System
1. Visit the deployed URL: [https://restaurant-table-booking-system-gfcs.onrender.com/](https://restaurant-table-booking-system-gfcs.onrender.com/).
2. Log in with the appropriate credentials based on your role:
   - **Admin**:
     - Username: `admin`
     - Password: `admin123`
   - **User**:
     - Username: `user`
     - Password: `user123`
3. Use the routes as described above to perform actions.

## Technologies Used
- **Backend**: Flask
- **Database**: SQLite
- **Deployment**: Render

