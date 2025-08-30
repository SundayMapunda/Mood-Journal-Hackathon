from app import create_app, db

app = create_app()

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    
    print("Creating all tables...")
    db.create_all()
    
    print("All tables recreated successfully!")
    
    # Verify the new structure
    from app.models import Entry
    import inspect
    print("\nEntry model attributes:")
    for attr_name, attr_value in inspect.getmembers(Entry):
        if not attr_name.startswith('_'):
            print(f"  {attr_name}: {type(attr_value)}")