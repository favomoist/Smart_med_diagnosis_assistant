from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User, Profile, RoleEnum
from app.schemas.auth import UserRegister, UserLogin, Token, UserResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserRegister, db: Session = Depends(get_db)):
    """Register a new user account (Patient, Clinician, Caregiver, or Admin)."""
    existing_user = db.query(User).filter(User.email == payload.email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )

    # Validate role
    role = payload.role.lower() if payload.role else "patient"
    valid_roles = [r.value for r in RoleEnum]
    if role not in valid_roles:
        role = "patient"

    # Create User
    new_user = User(
        email=payload.email.lower(),
        hashed_password=get_password_hash(payload.password),
        full_name=payload.full_name,
        role=role,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Automatically create default 'self' profile for patient/caregiver
    default_profile = Profile(
        user_id=new_user.id,
        name=new_user.full_name,
        relationship="self"
    )
    db.add(default_profile)
    db.commit()

    token = create_access_token(subject=str(new_user.id), role=new_user.role)
    return Token(
        access_token=token,
        token_type="bearer",
        role=new_user.role,
        user_id=new_user.id,
        full_name=new_user.full_name
    )


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """Authenticate and obtain JWT access token."""
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is inactive"
        )

    token = create_access_token(subject=str(user.id), role=user.role)
    return Token(
        access_token=token,
        token_type="bearer",
        role=user.role,
        user_id=user.id,
        full_name=user.full_name
    )


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Return currently logged-in user profile."""
    return current_user
