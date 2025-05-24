from app.database import SessionLocal
from app import model,utils


def load_users():
    db = SessionLocal()
    try:
        some_users = [
            {"email":"brendanstartk@gmail.com", "password":"password9999"},
            {"email":"aryastark@gmail.com", "password":"password9999"},
            {"email":"sansastark@gmail.com", "password":"password9999"},
            {"email":"johnybravisimo@gmail.com", "password":"password9999"}
            ]
        added_uzars = []

        existing_emails = {user.email for user in db.query(model.User).all()}
        
        for user_data in some_users:
            if user_data["email"] in existing_emails:
                print(f"Already exists {user_data["email"]} , skipping")
                continue
            hashed_password = utils.hash(user_data["password"])
            new_db_user = model.User(email=user_data["email"], password=hashed_password)
            db.add(new_db_user)
            added_uzars.append(user_data["email"])
        db.commit()
        print(f"Successfully created {len(added_uzars)} users: {added_uzars}")
            
    
    except Exception as e:
        db.rollback()
        print(e)
    finally:
        db.close()

if __name__ == "__main__":
    load_users()