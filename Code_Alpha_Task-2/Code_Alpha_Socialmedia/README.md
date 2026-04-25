# 🌐 SocialApp — Mini Instagram-style Django Project

A full-stack social media web app built with Django for internship submission.

---

## ✨ Features

| Feature | Status |
|---|---|
| User Registration & Login | ✅ |
| Follow / Unfollow users | ✅ |
| Follower & Following counts | ✅ |
| Home feed (followed users only) | ✅ |
| Create posts (text + image + video) | ✅ |
| Like / Unlike posts | ✅ |
| Comment on posts | ✅ |
| User profile pages | ✅ |
| Explore page (discover users) | ✅ |
| Delete own posts | ✅ |
| Django Admin panel | ✅ |
| Sample seed data | ✅ |

---

## 🚀 Setup Instructions

### 1. Clone / unzip the project
```
cd socialmedia/
```

### 2. Create & activate a virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Seed sample data (optional but recommended)
```bash
python manage.py seed_data
```
This creates 4 sample users (alice, bob, carol, david) with posts, likes, comments, and follow relationships. All share the password `Pass1234!`.

### 6. Create a superuser (for admin panel)
```bash
python manage.py createsuperuser
```

### 7. Start the development server
```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

Admin panel: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## 📁 Project Structure

```
socialmedia/
├── core/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── 0002_post_image_post_video.py   ← NEW: adds image & video fields
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py                ← NEW: sample data command
│   ├── templates/core/
│   │   ├── base.html       ← layout, nav, shared CSS & JS
│   │   ├── feed.html       ← home feed with post creation form
│   │   ├── profile.html    ← user profile page
│   │   ├── explore.html    ← discover other users
│   │   ├── login.html
│   │   └── register.html
│   ├── models.py    ← Post, Comment, Like, Follow
│   ├── views.py     ← all view functions
│   ├── urls.py      ← URL routing
│   ├── forms.py     ← PostForm (text+image+video), CommentForm
│   └── admin.py
├── socialmedia/
│   ├── settings.py  ← MEDIA_URL / MEDIA_ROOT added
│   └── urls.py      ← media serving added for development
├── media/           ← uploaded files stored here (git-ignored in production)
│   └── posts/images/  ← placeholder images for seed data
└── requirements.txt
```

---

## 🔑 Key Changes Made (v2)

### 1. Post Model — Image & Video Upload
`models.py`: Added `image = ImageField(...)` and `video = FileField(...)`.  
Both are optional so text-only posts still work.

### 2. Settings — Media Configuration
`settings.py`: Added `MEDIA_URL` and `MEDIA_ROOT` so Django knows where to store and serve uploaded files.

### 3. Main URL Config — Media Serving
`socialmedia/urls.py`: Added `+ static(MEDIA_URL, document_root=MEDIA_ROOT)` so uploaded files are accessible during development.

### 4. Post Form — File Upload Support
`forms.py`: Added `image` and `video` fields to `PostForm`.  
The form validates that at least one of (text / image / video) is provided.

### 5. Feed View — Handle File Uploads
`views.py`: Changed `PostForm(request.POST)` → `PostForm(request.POST, request.FILES)`.

### 6. Templates — Display Images & Videos
`feed.html` and `profile.html`: Added `<img>` and `<video>` tags that only render when a post has media. Added `enctype="multipart/form-data"` to the post creation form.

### 7. Seed Data Command
`management/commands/seed_data.py`: Run `python manage.py seed_data` to populate the app with sample users, posts (with placeholder images), likes, and comments.

---

## 📦 Requirements

```
Django>=4.2
Pillow>=9.0   # required for ImageField
```
