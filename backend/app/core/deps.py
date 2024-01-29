from app.db.database import SessionLocal
from sqlalchemy.orm import Session

# from fastapi.security import OAuth2PasswordBearer
# from jose import jwt
# from fastapi import HTTPException, Depends, status
# from app.models.user import User
# from app.core.config import settings
# from app.core import security
# from pydantic import ValidationError
# from app.services.ingredient_service import IngredientService
# from app.services.user_service import UserService
# from app.services.recipie_service import RecipieService


# reusable_oauth2 = OAuth2PasswordBearer(
#     tokenUrl=f"{settings.API_V1_STR}/login/access-token"
# )


def get_db() -> Session:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# def get_current_user(
#     db: Database = Depends(get_database), token: str = Depends(reusable_oauth2)
# ) -> User:
#     try:
#         token_data = security.decode_access_token(token)
#     except (jwt.JWTError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials",
#         )
#     user = db.get_collection("users").find_one({"_id": token_data.sub})
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return User(**user)


# def get_current_active_user(
#     current_user: User = Depends(get_current_user),
# ) -> User:
#     if not current_user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# def get_current_active_superuser(
#     current_user: User = Depends(get_current_active_user),
# ) -> User:
#     if not current_user.is_superuser:
#         raise HTTPException(
#             status_code=400, detail="The user doesn't have enough privileges"
#         )
#     return current_user


# def recipie_service(db: Database = Depends(get_database)):
#     collection = db.get_collection("recipies")
#     return RecipieService(collection)


# def ingredient_service(db: Database = Depends(get_database)):
#     collection = db.get_collection("ingredients")
#     return IngredientService(collection)


# def user_service(db: Database = Depends(get_database)):
#     collection = db.get_collection("users")
#     return UserService(collection)
