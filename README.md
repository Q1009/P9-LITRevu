# LITRevu

A Django-based web application for literary reviews. LITRevu lets users request and publish reviews for books and articles, and subscribe to other users' feeds.

---

## Features

- **Authentication**: sign up, log in, and log out
- **Tickets**: create a review request for a book or article (with optional image upload)
- **Reviews**: respond to an existing ticket, or create a standalone review (ticket + review on a single page)
- **Feed**: display tickets and reviews from followed users, sorted by date
- **My posts**: view and manage your own tickets and reviews
- **Subscriptions**: follow / unfollow other users
- **Business rules**:
  - A ticket can only receive one review (the button is hidden and the URL is blocked if a review already exists)
  - A user cannot follow themselves

---

## Tech stack

| Component     | Version  |
|---------------|----------|
| Python        | 3.13     |
| Django        | 6.0.2    |
| Pillow        | 12.1.1   |
| SQLite        | (default)|

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Q1009/P9-LITRevu.git
cd "P9-LITRevu"
```

### 2. Create and activate the virtual environment

```bash
python3 -m venv env
source env/bin/activate  # macOS / Linux
env\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
cd litrevu
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

The application is available at [http://localhost:8000/](http://localhost:8000/).

---

## Project structure

```
P9 - LITRevu/
├── requirements.txt
├── env/                        # Virtual environment (not versioned)
└── litrevu/                    # Django root
    ├── manage.py
    ├── db.sqlite3
    ├── media/                  # User-uploaded images
    ├── static/
    │   └── styles.css
    ├── templates/
    │   └── base.html
    ├── litrevu/                # Project configuration
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── authentication/         # App: sign up / log in
    │   ├── models.py           # Custom user model
    │   ├── views.py
    │   ├── forms.py
    │   └── templates/
    └── flux/                   # App: tickets, reviews, subscriptions
        ├── models.py           # Ticket, Review, UserFollows
        ├── views.py
        ├── forms.py
        ├── urls.py
        ├── templatetags/
        │   └── flux_extras.py  # Custom filters (rating_stars, model_type)
        └── templates/
```

---

## Main routes

| URL                                  | Description                              |
|--------------------------------------|------------------------------------------|
| `/`                                  | Login page                               |
| `/signup/`                           | Sign up                                  |
| `/flux/home/`                        | Feed from followed users                 |
| `/flux/posts/`                       | My tickets and reviews                   |
| `/flux/subscriptions/`               | Subscription management                  |
| `/flux/create-ticket/`               | Create a ticket                          |
| `/flux/edit-ticket/<id>/`            | Edit / delete a ticket                   |
| `/flux/create-review/`               | Create a standalone review               |
| `/flux/create-review/<ticket_id>/`   | Create a review in response to a ticket  |
| `/flux/edit-review/<id>/`            | Edit / delete a review                   |

---

## Data models

### `Ticket`
| Field          | Type              | Description                    |
|----------------|-------------------|--------------------------------|
| `title`        | CharField(128)    | Book / article title           |
| `description`  | TextField(8192)   | Description                    |
| `image`        | ImageField        | Optional image (UUID filename) |
| `author`       | ForeignKey(User)  | Ticket author                  |
| `date_created` | DateTimeField     | Creation date                  |
| `date_edited`  | DateTimeField     | Last edit date                 |

### `Review`
| Field          | Type              | Description                    |
|----------------|-------------------|--------------------------------|
| `ticket`       | ForeignKey(Ticket)| Associated ticket              |
| `rating`       | PositiveSmallInt  | Rating from 0 to 5             |
| `headline`     | CharField(128)    | Review title                   |
| `body`         | TextField(8192)   | Review body                    |
| `user`         | ForeignKey(User)  | Review author                  |
| `time_created` | DateTimeField     | Creation date                  |

### `UserFollows`
| Field          | Type              | Description                    |
|----------------|-------------------|--------------------------------|
| `user`         | ForeignKey(User)  | Subscriber                     |
| `user_followed`| ForeignKey(User)  | Followed user                  |

The `unique_together` constraint prevents duplicate subscriptions.

---

## Create a superuser (admin access)

```bash
python manage.py createsuperuser
```

The admin interface is available at [http://localhost:8000/admin/](http://localhost:8000/admin/).

