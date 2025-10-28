from rest_framework import serializers
from .models import Listing, Booking, Review
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']  # Removed 'user_id' if it doesn't exist

class ListingSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    
    class Meta:
        model = Listing
        fields = [
            'listing_id', 'host', 'title', 'description', 'property_type',
            'price_per_night', 'max_guests', 'bedrooms', 'bathrooms',
            'amenities', 'address', 'city', 'country', 'latitude', 'longitude',
            'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['listing_id', 'host', 'created_at', 'updated_at']

class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    listing_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'user', 'listing', 'listing_id', 'check_in', 'check_out',
            'guests', 'total_price', 'status', 'special_requests', 'created_at', 'updated_at'
        ]
        read_only_fields = ['booking_id', 'user', 'total_price', 'created_at', 'updated_at']
    
    def validate(self, data):
        if data['check_out'] <= data['check_in']:
            raise serializers.ValidationError("Check-out date must be after check-in date.")
        if data['guests'] <= 0:
            raise serializers.ValidationError("Number of guests must be positive.")
        return data

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'review_id', 'user', 'listing', 'booking', 'rating', 'comment',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['review_id', 'user', 'listing', 'created_at', 'updated_at']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value