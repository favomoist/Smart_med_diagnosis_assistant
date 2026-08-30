from typing import Generator, Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User

security_bearer = HTTPBearer(auto_error=False)


def get_current_user_optional(
    auth_header: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """Retrieves user if valid Bearer token is passed; otherwise returns None (for guest sessions)."""
    if not auth_header:
        return None
    token = auth_header.credentials
    payload = decode_access_token(token)
    if not payload:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    try:
        user = db.query(User).filter(User.id == int(user_id)).first()
        return user
    except Exception:
        return None


def get_current_user(
    auth_header: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer),
    db: Session = Depends(get_db),
) -> User:
    """Enforces valid JWT authentication."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not auth_header:
        raise credentials_exception
    token = auth_header.credentials
    payload = decode_access_token(token)
    if not payload:
        raise credentials_exception
    user_id = payload.get("sub")
    if not user_id:
        raise credentials_exception
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    return user


def require_role(allowed_roles: List[str]):
    """Role-based access control dependency factory."""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Required roles: {allowed_roles}, your role: {current_user.role}"
            )
        return current_user
    return role_checker
