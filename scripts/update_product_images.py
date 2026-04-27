"""
Script to update product images with dummy images based on category.
Run this script to populate image_url field for existing products.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app.db.database import SessionLocal
from app.models.e_commerce import Product, Category
from sqlalchemy.orm import joinedload

# Dummy image URLs based on category
CATEGORY_IMAGES = {
    'electronics': [
        'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1572569028738-411a29a16ac4?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400&h=300&fit=crop',
    ],
    'clothing': [
        'https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=400&h=300&fit=crop',
    ],
    'books': [
        'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=400&h=300&fit=crop',
    ],
    'home': [
        'https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1484101403633-562f891dc89a?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1556911220-bff31c812dba?w=400&h=300&fit=crop',
    ],
    'sports': [
        'https://images.unsplash.com/photo-1461896836934- voices?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400&h=300&fit=crop',
    ],
    'food': [
        'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=400&h=300&fit=crop',
    ],
    'default': [
        'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1572569028738-411a29a16ac4?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop',
    ]
}


def get_image_for_category(category_name):
    """Get a random image URL for a given category."""
    category_lower = category_name.lower() if category_name else 'default'
    
    # Find matching category
    for key in CATEGORY_IMAGES:
        if key in category_lower:
            images = CATEGORY_IMAGES[key]
            # Use product ID to pick a consistent image
            import random
            return random.choice(images)
    
    # Default fallback
    import random
    return random.choice(CATEGORY_IMAGES['default'])


def update_product_images():
    """Update all products with dummy images based on their category."""
    db = SessionLocal()
    
    try:
        # Fetch all products with their categories
        products = db.query(Product).options(joinedload(Product.category)).all()
        
        print(f"Found {len(products)} products to update...")
        
        updated_count = 0
        for product in products:
            if not product.image_url:
                category_name = product.category.name if product.category else 'default'
                image_url = get_image_for_category(category_name)
                product.image_url = image_url
                updated_count += 1
                print(f"Updated: {product.name} ({category_name}) -> {image_url}")
            else:
                print(f"Skipped: {product.name} (already has image)")
        
        db.commit()
        print(f"\n✅ Successfully updated {updated_count} products!")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("🖼️  Product Image Update Script")
    print("=" * 50)
    update_product_images()
