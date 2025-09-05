#!/usr/bin/env python3
"""
Database migration script to update LargeBinary column sizes
"""

import mysql.connector
from mysql.connector import Error
from app.config import Config

def update_database_schema():
    """Update the database schema to increase LargeBinary column sizes"""
    try:
        # Connect to database
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            print("Connected to MySQL database")
            print("Updating application table schema...")
            
            # Update degree_certificate column to LONGBLOB (up to 4GB)
            alter_degree_cert = """
            ALTER TABLE application 
            MODIFY COLUMN degree_certificate LONGBLOB NOT NULL
            """
            
            # Update id_proof column to LONGBLOB (up to 4GB)
            alter_id_proof = """
            ALTER TABLE application 
            MODIFY COLUMN id_proof LONGBLOB NOT NULL
            """
            
            print("Updating degree_certificate column...")
            cursor.execute(alter_degree_cert)
            
            print("Updating id_proof column...")
            cursor.execute(alter_id_proof)
            
            # Commit the changes
            connection.commit()
            print("✅ Database schema updated successfully!")
            print("   - degree_certificate column: LONGBLOB (up to 4GB)")
            print("   - id_proof column: LONGBLOB (up to 4GB)")
            
    except Error as e:
        print(f"❌ Error updating database schema: {e}")
        if connection:
            connection.rollback()
    
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed")

if __name__ == "__main__":
    print("Database Schema Migration")
    print("=" * 50)
    update_database_schema()
