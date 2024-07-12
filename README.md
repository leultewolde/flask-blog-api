
# Flask Blog API

## Overview

This project is a simple blogging platform API built with Python Flask. It supports user authentication and allows users to create, retrieve, update, and delete blog posts. The API uses JWT for secure authentication and SQLite for database storage.

## Features

- User Signup and Signin
- JWT Authentication
- Create, Read, Update, Delete (CRUD) operations for blog posts
- Unit tests for reliability

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/leultewolde/flask-blog-api
   cd flask-blog-api
   ```

2. **Set up a virtual environment and install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**

   Create a `.env` file in the project root with the following content:

   ```env
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///blog.db
   JWT_SECRET_KEY=your-jwt-secret-key
   ```

4. **Initialize the database:**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. **Run the application:**
   ```bash
   flask run
   ```

## API Documentation

### Authentication

#### Sign Up

- **Endpoint:** `POST /signup`
- **Description:** Register a new user.
- **Request Body:**
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **Response:**
  - `201 Created` on success
  - `400 Bad Request` if username or email already exists

#### Sign In

- **Endpoint:** `POST /signin`
- **Description:** Log in an existing user.
- **Request Body:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response:**
  - `200 OK` with JWT token
  - `401 Unauthorized` if credentials are invalid

### Blog Posts

#### Create a Post

- **Endpoint:** `POST /posts`
- **Description:** Create a new blog post.
- **Authentication:** Bearer token required
- **Request Body:**
  ```json
  {
    "title": "string",
    "body": "string"
  }
  ```
- **Response:**
  - `201 Created` on success
  - `403 Forbidden` if unauthorized

#### Get All Posts

- **Endpoint:** `GET /posts`
- **Description:** Retrieve a list of all blog posts.
- **Response:**
  - `200 OK` with list of posts

#### Get a Single Post

- **Endpoint:** `GET /posts/<post_id>`
- **Description:** Retrieve a single blog post by its ID.
- **Response:**
  - `200 OK` with post details
  - `404 Not Found` if post does not exist

#### Update a Post

- **Endpoint:** `PUT /posts/<post_id>`
- **Description:** Update an existing blog post.
- **Authentication:** Bearer token required
- **Request Body:**
  ```json
  {
    "title": "string",
    "body": "string"
  }
  ```
- **Response:**
  - `200 OK` on success
  - `403 Forbidden` if unauthorized
  - `404 Not Found` if post does not exist

#### Delete a Post

- **Endpoint:** `DELETE /posts/<post_id>`
- **Description:** Delete a blog post.
- **Authentication:** Bearer token required
- **Response:**
  - `200 OK` on success
  - `403 Forbidden` if unauthorized
  - `404 Not Found` if post does not exist

## Testing

To run the unit tests, use the following command:

```bash
python -m unittest discover -s tests
```

## Design Decisions and Trade-offs

- **Authentication:** JWT was chosen for its simplicity and stateless nature, making it easy to scale.
- **Database:** SQLite is used for simplicity, but can be replaced with PostgreSQL or MySQL for production environments.
- **Flask:** Chosen for its lightweight and modular design, making it ideal for building RESTful APIs quickly.

## Future Improvements

- Implementing pagination for retrieving blog posts.
- Adding user roles and permissions.
- Integrating with a front-end framework like React for a complete web application.

