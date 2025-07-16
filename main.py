from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import select, Session
from models import User, Formula, FormulaStatus, HazardClass, Permission, Role, Inquiry
from db import get_session, engine
import os

from db import add_mock_data, init_db
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    add_mock_data()
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/")
def get_root():
    return {"message": "db", "status": "running"}


# User endpoints
@app.get("/users", response_model=list[User])
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


@app.post("/users", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    user.hashed_password = user.hashed_password.encode()
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# Formula endpoints
@app.get("/formulas", response_model=list[Formula])
def get_formulas(session: Session = Depends(get_session)):
    formulas = session.exec(select(Formula)).all()
    return formulas


@app.post("/formulas", response_model=Formula)
def create_formula(formula: Formula, session: Session = Depends(get_session)):
    session.add(formula)
    session.commit()
    session.refresh(formula)
    return formula


# Lookup tables
@app.get("/formula-statuses", response_model=list[FormulaStatus])
def get_formula_statuses(session: Session = Depends(get_session)):
    statuses = session.exec(select(FormulaStatus)).all()
    return statuses

@app.get("/hazard-classes", response_model=list[HazardClass])
def get_hazard_classes(session: Session = Depends(get_session)):
    classes = session.exec(select(HazardClass)).all()
    return classes

# permissions
@app.get("/permissions", response_model=list[Permission])
def get_permissions(session: Session = Depends(get_session)):
    perms = session.exec(select(Permission)).all()
    return perms

@app.post("/permissions", response_model=Permission)
def create_permission(permission: Permission, session: Session = Depends(get_session)):
    session.add(permission)
    session.commit()
    session.refresh(permission)
    return permission

# roles
@app.get("/roles", response_model=list[Role])
def get_roles(session: Session = Depends(get_session)):
    roles = session.exec(select(Role)).all()
    return roles

@app.post("/roles", response_model=Role)
def create_role(role: Role, session: Session = Depends(get_session)):
    session.add(role)
    session.commit()
    session.refresh(role)
    return role

# Inquiry endpoints
@app.get("/inquiries", response_model=list[Inquiry])
def get_inquiries(session: Session = Depends(get_session)):
    inquiries = session.exec(select(Inquiry)).all()
    return inquiries


@app.post("/inquiries", response_model=Inquiry)
def create_inquiry(inquiry: Inquiry, session: Session = Depends(get_session)):
    session.add(inquiry)
    session.commit()
    session.refresh(inquiry)
    return inquiry