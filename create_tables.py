from app import create_app, db
# from app.models import User, Entry, EmotionScore, Tag  # Import all models

app = create_app()

with app.app_context():
    try:
        # print("Dropping all existing tables...")
        # db.drop_all()  # This will clear everything first
        
        print("Creating all tables...")
        db.create_all()
        print("All tables created successfully!")
        
        # Verify creation
        result = db.session.execute(db.text('SHOW TABLES'))
        tables = result.fetchall()
        print(f"Tables found: {len(tables)}")
        for table in tables:
            print(f" - {table[0]}")
            
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()