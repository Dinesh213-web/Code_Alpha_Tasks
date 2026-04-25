"""
Management command: seed_data
Usage:  python manage.py seed_data

Creates sample users, follow relationships, posts (some with placeholder images),
likes, and comments so the app looks active when submitted for review.
Run this AFTER `python manage.py migrate`.
"""

import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files import File
from core.models import Post, Comment, Like, Follow


SAMPLE_USERS = [
    {"username": "alice",  "password": "Pass1234!", "email": "alice@example.com"},
    {"username": "bob",    "password": "Pass1234!", "email": "bob@example.com"},
    {"username": "carol",  "password": "Pass1234!", "email": "carol@example.com"},
    {"username": "david",  "password": "Pass1234!", "email": "david@example.com"},
]

SAMPLE_POSTS = [
    # (author_username, text_content, image_filename_or_None)
    ("alice",  "Just started this social app — loving it so far! 🚀",          "placeholder_1.jpg"),
    ("alice",  "Beautiful morning today. Went for a walk and cleared my head.", "placeholder_2.jpg"),
    ("bob",    "Working on a new Django project. Full-stack is so rewarding!",  "placeholder_3.jpg"),
    ("bob",    "Pro tip: always use virtual environments for Python projects.",  None),
    ("carol",  "Coffee + code = perfect Sunday ☕",                             "placeholder_4.jpg"),
    ("carol",  "Just deployed my first web app. What a feeling! 🎉",            None),
    ("david",  "Exploring the city today. Found an amazing bookstore!",         "placeholder_5.jpg"),
    ("david",  "Finished reading 'Clean Code' — highly recommend it.",          "placeholder_6.jpg"),
]

SAMPLE_COMMENTS = [
    # (post_index, commenter_username, comment_text)
    (0, "bob",   "Congrats on joining! 🙌"),
    (0, "carol", "Welcome to the community!"),
    (2, "alice", "Django is the best! What are you building?"),
    (2, "david", "Agreed, full-stack devs are awesome."),
    (4, "bob",   "Coffee is life ☕"),
    (4, "david", "Same energy every Sunday lol"),
    (6, "carol", "Which bookstore? I love finding hidden gems!"),
    (7, "alice", "That book changed how I write code 💯"),
]

# Follow pairs: (follower, following)
FOLLOW_PAIRS = [
    ("alice", "bob"),
    ("alice", "carol"),
    ("alice", "david"),
    ("bob",   "alice"),
    ("bob",   "carol"),
    ("carol", "alice"),
    ("carol", "david"),
    ("david", "bob"),
    ("david", "carol"),
]

# Likes: list of (post_index, liker_username)
LIKES = [
    (0, "bob"), (0, "carol"), (0, "david"),
    (1, "bob"), (1, "david"),
    (2, "alice"), (2, "carol"),
    (4, "alice"), (4, "bob"), (4, "david"),
    (6, "alice"), (6, "carol"),
    (7, "alice"), (7, "bob"),
]


class Command(BaseCommand):
    help = "Seeds the database with sample users, posts, likes, and comments."

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("── Seeding database ──"))

        # ── Users ────────────────────────────────────────────────────────────
        users = {}
        for u in SAMPLE_USERS:
            obj, created = User.objects.get_or_create(
                username=u["username"],
                defaults={"email": u["email"]},
            )
            if created:
                obj.set_password(u["password"])
                obj.save()
                self.stdout.write(f"  Created user: {obj.username}")
            else:
                self.stdout.write(f"  User already exists: {obj.username}")
            users[u["username"]] = obj

        # ── Follows ──────────────────────────────────────────────────────────
        for follower_name, following_name in FOLLOW_PAIRS:
            Follow.objects.get_or_create(
                follower=users[follower_name],
                following=users[following_name],
            )
        self.stdout.write(f"  Follow relationships: {len(FOLLOW_PAIRS)} created/verified")

        # ── Posts ────────────────────────────────────────────────────────────
        media_dir = os.path.join(
            os.path.dirname(__file__),          # commands/
            '..', '..', '..', '..', '..', 'media', 'posts', 'images'
        )
        media_dir = os.path.abspath(media_dir)

        posts = []
        for author_name, text, img_filename in SAMPLE_POSTS:
            author = users[author_name]

            # Skip if this exact post already exists (idempotent)
            if Post.objects.filter(author=author, content=text).exists():
                posts.append(Post.objects.filter(author=author, content=text).first())
                self.stdout.write(f"  Post already exists for {author_name}: {text[:40]}...")
                continue

            post = Post(author=author, content=text)

            # Attach placeholder image if available on disk
            if img_filename:
                img_path = os.path.join(media_dir, img_filename)
                if os.path.exists(img_path):
                    with open(img_path, 'rb') as f:
                        post.image.save(img_filename, File(f), save=False)

            post.save()
            posts.append(post)
            self.stdout.write(f"  Created post by {author_name}: {text[:40]}...")

        # ── Likes ────────────────────────────────────────────────────────────
        like_count = 0
        for post_idx, liker_name in LIKES:
            if post_idx < len(posts) and posts[post_idx]:
                Like.objects.get_or_create(post=posts[post_idx], user=users[liker_name])
                like_count += 1
        self.stdout.write(f"  Likes: {like_count} created/verified")

        # ── Comments ─────────────────────────────────────────────────────────
        comment_count = 0
        for post_idx, commenter_name, text in SAMPLE_COMMENTS:
            if post_idx < len(posts) and posts[post_idx]:
                Comment.objects.get_or_create(
                    post=posts[post_idx],
                    author=users[commenter_name],
                    defaults={"content": text},
                )
                comment_count += 1
        self.stdout.write(f"  Comments: {comment_count} created/verified")

        self.stdout.write(self.style.SUCCESS(
            "\n✅ Seed complete!\n"
            "   Login credentials for all sample users:\n"
            "   Username: alice / bob / carol / david\n"
            "   Password: Pass1234!\n"
        ))
