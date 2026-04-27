"""
Script to add image_url column to products table if it doesn't exist.
Run this before update_product_images.py
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app.db.database import engine
from sqlalchemy import text

def add_image_column():
    """Add image_url column to products table if it doesn't exist."""
    
    try:
        with engine.connect() as conn:
            # Check if column already exists
            result = conn.execute(text("""
                SELECT COUNT(*) as count 
                FROM pragma_table_info('products') 
                WHERE name='image_url'
            """))
            
            column_exists = result.fetchone()[0] > 0
            
            if column_exists:
                print("✅ Column 'image_url' already exists in products table.")
            else:
                # Add the column
                conn.execute(text("""
                    ALTER TABLE products 
                    ADD COLUMN image_url VARCHAR(500)
                """))
                conn.commit()
                print("✅ Successfully added 'image_url' column to products table.")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nNote: If you're using PostgreSQL, use this SQL instead:")
        print("ALTER TABLE products ADD COLUMN image_url VARCHAR(500);")

if __name__ == "__main__":
    print("🔧 Add Image Column Script")
    print("=" * 50)
    add_image_column()
