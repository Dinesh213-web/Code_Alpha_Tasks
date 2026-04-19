from django.core.management.base import BaseCommand
from store.models import Product

SAMPLE_PRODUCTS = [
    {"name": "Wireless Noise-Cancelling Headphones", "description": "Premium over-ear headphones with 30-hour battery life, active noise cancellation, and crystal-clear audio. Perfect for work-from-home setups or long commutes. Features Bluetooth 5.0 and a foldable design for easy storage.", "price": 79.99, "stock": 15},
    {"name": "Mechanical Keyboard — TKL Edition", "description": "Tenkeyless mechanical keyboard with Cherry MX Blue switches. Tactile and clicky typing experience with RGB backlighting and PBT double-shot keycaps. USB-C connectivity and NKRO support for gaming and programming.", "price": 59.99, "stock": 8},
    {"name": "Smart Fitness Watch", "description": "Track your health 24/7 with this sleek fitness tracker. Monitors heart rate, SpO2, sleep quality, and 12 workout modes. Water-resistant to 50m and features a 7-day battery life with a stunning AMOLED display.", "price": 45.00, "stock": 20},
    {"name": "USB-C Hub — 7-in-1", "description": "Expand your laptop's connectivity with this compact hub. Includes 4K HDMI, 100W PD charging, 3x USB-A 3.0, SD and microSD card slots. Plug-and-play, no drivers needed. Supports MacBook, iPad Pro, and all USB-C laptops.", "price": 29.99, "stock": 25},
    {"name": "Ergonomic Desk Chair", "description": "Work in comfort with full lumbar support, adjustable armrests, and breathable mesh back. Height-adjustable with 360-degree swivel and 135-degree recline. Supports up to 120kg. Recommended by physiotherapists for long working hours.", "price": 249.00, "stock": 5},
    {"name": "Portable Bluetooth Speaker", "description": "360-degree surround sound in a waterproof IPX7 package. 20W output with 12-hour playback, built-in mic for hands-free calls, and True Wireless Stereo pairing. Your music follows you anywhere.", "price": 39.99, "stock": 18},
    {"name": "LED Desk Lamp with Wireless Charger", "description": "3-in-1 productivity companion: adjustable LED lamp with 5 colour temperatures, 10W wireless charging pad, and USB-A port. Memory function remembers your last setting. Eye-care technology reduces blue light strain.", "price": 34.99, "stock": 12},
    {"name": "Webcam 1080p HD with Ring Light", "description": "Look your best on every video call. Built-in ring light with 3 brightness levels, autofocus, and noise-cancelling dual microphone. Plug-and-play USB, compatible with Zoom, Teams, and Google Meet.", "price": 55.00, "stock": 3},
]

class Command(BaseCommand):
    help = 'Seed the database with sample products'

    def handle(self, *args, **kwargs):
        if Product.objects.exists():
            self.stdout.write(self.style.WARNING('Products already exist. Skipping seed.'))
            return
        for data in SAMPLE_PRODUCTS:
            Product.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'  Created: {data["name"]}'))
        self.stdout.write(self.style.SUCCESS(f'\n✅ {len(SAMPLE_PRODUCTS)} products seeded!'))
