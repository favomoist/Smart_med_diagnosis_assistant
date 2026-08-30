from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User, Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse

router = APIRouter()


@router.get("", response_model=List[ProfileResponse])
def list_profiles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all profiles belonging to the current user (self and dependents)."""
    return db.query(Profile).filter(Profile.user_id == current_user.id).all()


@router.post("", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(
    payload: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new profile (e.g. dependent parent/child for caregivers)."""
    new_profile = Profile(
        user_id=current_user.id,
        name=payload.name,
        relationship=payload.relationship or "dependent",
        age=payload.age,
        sex=payload.sex,
        known_allergies=payload.known_allergies,
        chronic_conditions=payload.chronic_conditions
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile


@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile(
    profile_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get details of a specific profile."""
    profile = db.query(Profile).filter(
        Profile.id == profile_id,
        Profile.user_id == current_user.id
    ).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile


@router.put("/{profile_id}", response_model=ProfileResponse)
def update_profile(
    profile_id: int,
    payload: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update profile details (age, sex, medical baseline)."""
    profile = db.query(Profile).filter(
        Profile.id == profile_id,
        Profile.user_id == current_user.id
    ).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    for field, val in payload.model_dump(exclude_unset=True).items():
        setattr(profile, field, val)

    db.commit()
    db.refresh(profile)
    return profile


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(
    profile_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a dependent profile."""
    profile = db.query(Profile).filter(
        Profile.id == profile_id,
        Profile.user_id == current_user.id
    ).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    if profile.relationship == "self":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete primary self profile"
        )

    db.delete(profile)
    db.commit()
    return None
