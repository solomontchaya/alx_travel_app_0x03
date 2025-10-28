from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing, Booking, Review
import random
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with sample listings, bookings, and reviews'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Create sample users if they don't exist
        host_user, created = User.objects.get_or_create(
            email='host@example.com',
            defaults={
                'first_name': 'John',
                'last_name': 'Host',
                # Removed 'role' field since it doesn't exist in your User model
            }
        )
        if created:
            host_user.set_password('password123')
            host_user.save()
            self.stdout.write(f'Created host user: {host_user.email}')

        guest_user, created = User.objects.get_or_create(
            email='guest@example.com',
            defaults={
                'first_name': 'Jane',
                'last_name': 'Guest',
                # Removed 'role' field since it doesn't exist in your User model
            }
        )
        if created:
            guest_user.set_password('password123')
            guest_user.save()
            self.stdout.write(f'Created guest user: {guest_user.email}')

        # Sample listings data
        sample_listings = [
            {
                'title': 'Beautiful Beach Villa',
                'description': 'Stunning beachfront property with panoramic ocean views',
                'property_type': 'villa',
                'price_per_night': 250.00,
                'max_guests': 6,
                'bedrooms': 3,
                'bathrooms': 2,
                'amenities': ['wifi', 'pool', 'air_conditioning', 'kitchen', 'parking'],
                'address': '123 Beach Road',
                'city': 'Miami',
                'country': 'USA',
                'latitude': 25.7617,
                'longitude': -80.1918
            },
            {
                'title': 'Cozy Mountain Cabin',
                'description': 'Rustic cabin perfect for nature lovers and hikers',
                'property_type': 'cabin',
                'price_per_night': 120.00,
                'max_guests': 4,
                'bedrooms': 2,
                'bathrooms': 1,
                'amenities': ['wifi', 'fireplace', 'kitchen', 'hiking_trails'],
                'address': '456 Mountain View',
                'city': 'Aspen',
                'country': 'USA',
                'latitude': 39.1911,
                'longitude': -106.8175
            },
            {
                'title': 'Luxury Downtown Apartment',
                'description': 'Modern apartment in the heart of the city with amazing skyline views',
                'property_type': 'apartment',
                'price_per_night': 180.00,
                'max_guests': 4,
                'bedrooms': 2,
                'bathrooms': 2,
                'amenities': ['wifi', 'gym', 'pool', 'concierge', 'parking'],
                'address': '789 Downtown Street',
                'city': 'New York',
                'country': 'USA',
                'latitude': 40.7128,
                'longitude': -74.0060
            }
        ]

        # Create listings
        listings = []
        for listing_data in sample_listings:
            listing, created = Listing.objects.get_or_create(
                title=listing_data['title'],
                defaults={
                    'host': host_user,
                    'description': listing_data['description'],
                    'property_type': listing_data['property_type'],
                    'price_per_night': listing_data['price_per_night'],
                    'max_guests': listing_data['max_guests'],
                    'bedrooms': listing_data['bedrooms'],
                    'bathrooms': listing_data['bathrooms'],
                    'amenities': listing_data['amenities'],
                    'address': listing_data['address'],
                    'city': listing_data['city'],
                    'country': listing_data['country'],
                    'latitude': listing_data['latitude'],
                    'longitude': listing_data['longitude']
                }
            )
            listings.append(listing)
            if created:
                self.stdout.write(f'Created listing: {listing.title}')
            else:
                self.stdout.write(f'Listing already exists: {listing.title}')

        # Create sample bookings
        for i, listing in enumerate(listings):
            check_in = datetime.now().date() + timedelta(days=30 + i*7)
            check_out = check_in + timedelta(days=3 + i)
            
            booking, created = Booking.objects.get_or_create(
                user=guest_user,
                listing=listing,
                check_in=check_in,
                defaults={
                    'check_out': check_out,
                    'guests': min(2, listing.max_guests),
                    'total_price': float(listing.price_per_night) * (check_out - check_in).days,
                    'status': 'confirmed',
                    'special_requests': f'Looking forward to staying at {listing.title}!'
                }
            )
            if created:
                self.stdout.write(f'Created booking for: {listing.title}')
            else:
                self.stdout.write(f'Booking already exists for: {listing.title}')

        # Create sample reviews
        for listing in listings:
            try:
                booking = Booking.objects.get(listing=listing, user=guest_user)
                review, created = Review.objects.get_or_create(
                    user=guest_user,
                    listing=listing,
                    defaults={
                        'booking': booking,
                        'rating': random.randint(4, 5),
                        'comment': f'Amazing stay at {listing.title}! Highly recommended.'
                    }
                )
                if created:
                    self.stdout.write(f'Created review for: {listing.title}')
                else:
                    self.stdout.write(f'Review already exists for: {listing.title}')
            except Booking.DoesNotExist:
                self.stdout.write(f'No booking found for {listing.title}, skipping review')
                continue

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database with sample data!')
        )