import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.security import create_access_token, get_password_hash
from app.models.user import User, Profile, RoleEnum
from app.engine.triage_engine import init_knowledge_base
from app.main import app

# SQLite in-memory test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    init_knowledge_base(db)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_patient_user(db_session):
    user = db_session.query(User).filter(User.email == "patient@example.com").first()
    if not user:
        user = User(
            email="patient@example.com",
            hashed_password=get_password_hash("patientpassword123"),
            full_name="Priya Patient",
            role=RoleEnum.PATIENT.value,
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        profile = Profile(
            user_id=user.id,
            name="Priya Patient",
            relationship="self",
            age=28,
            sex="female"
        )
        db_session.add(profile)
        db_session.commit()
    return user


@pytest.fixture
def test_clinician_user(db_session):
    user = db_session.query(User).filter(User.email == "clinician@example.com").first()
    if not user:
        user = User(
            email="clinician@example.com",
            hashed_password=get_password_hash("clinicianpassword123"),
            full_name="Dr. Arjun Clinician",
            role=RoleEnum.CLINICIAN.value,
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
    return user


@pytest.fixture
def test_admin_user(db_session):
    user = db_session.query(User).filter(User.email == "admin@example.com").first()
    if not user:
        user = User(
            email="admin@example.com",
            hashed_password=get_password_hash("adminpassword123"),
            full_name="System Admin",
            role=RoleEnum.ADMIN.value,
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
    return user


@pytest.fixture
def patient_headers(test_patient_user):
    token = create_access_token(subject=str(test_patient_user.id), role=test_patient_user.role)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def clinician_headers(test_clinician_user):
    token = create_access_token(subject=str(test_clinician_user.id), role=test_clinician_user.role)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(test_admin_user):
    token = create_access_token(subject=str(test_admin_user.id), role=test_admin_user.role)
    return {"Authorization": f"Bearer {token}"}
