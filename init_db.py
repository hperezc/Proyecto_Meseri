from app import app, db

with app.app_context():
    try:
        db.create_all()
        print("Base de datos creada exitosamente")
    except Exception as e:
        print(f"Error al crear la base de datos: {str(e)}")
