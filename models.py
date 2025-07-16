from datetime import datetime, timezone
from typing import Any
from sqlalchemy import LargeBinary, CheckConstraint

from sqlmodel import Column, Field, JSON, Relationship, SQLModel


def iso_datetime() -> str:
    # ISO=8601 format for datetime (e.g., "2000-01-01T00:00:00")
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


# base model for all entities
class BaseModel(SQLModel, table=False):
    id: int | None = Field(default=None, primary_key=True)
    created_at: str = Field(default_factory=iso_datetime)


# lookup tables
class FormulaStatus(BaseModel, table=True):
    code: str = Field(unique=True)  # APP, REV, PEN, REJ
    name: str  # "Approved", "Under Review", "Pending", "Rejected"


class HazardClass(BaseModel, table=True):
    name: str = Field(unique=True)  # "Flammable", "Toxic", "Corrosive"


# role
class RolePermission(SQLModel, table=True):
    role_id: int = Field(foreign_key="role.id", primary_key=True)
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)
    
    
class Permission(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(unique=True, index=True)  # "formula:create"
    description: str | None = None
    roles: list["Role"] = Relationship(
        back_populates="permissions", link_model=RolePermission
    )


class Role(BaseModel, table=True):
    name: str = Field(unique=True)
    description: str | None = None
    permissions: list[Permission] = Relationship(
        back_populates="roles", link_model=RolePermission
    )

    users: list["User"] = Relationship(back_populates="role")


# core
class User(BaseModel, table=True):
    first_name: str
    last_name: str
    email: str = Field(unique=True, index=True)
    hashed_password: bytes = Field(
        sa_column=Column(LargeBinary)
    )  # password hashes can be large
    role_id: int = Field(foreign_key="role.id")

    role: Role = Relationship(back_populates="users")
    inquiries: list["Inquiry"] = Relationship(back_populates="user")
    formulas: list["Formula"] = Relationship(back_populates="user")

    __table_args__ = (
        CheckConstraint("email LIKE '%_@__%.__%'", name="check_email_format"),
    )


class Inquiry(BaseModel, table=True):
    user_id: int = Field(foreign_key="user.id")
    prompt: str
    response: str | None = None

    user: User = Relationship(back_populates="inquiries")
    uploads: list["FileUpload"] = Relationship(back_populates="inquiry")


class Formula(BaseModel, table=True):
    user_id: int = Field(foreign_key="user.id")
    name: str = Field(unique=True, index=True)
    vendor: str | None = None
    ingredients: list[dict[str, Any]] = Field(
        sa_column=Column(JSON), default_factory=list
    )
    properties: dict[str, Any] = Field(sa_column=Column(JSON), default_factory=dict)
    tags: list[str] = Field(sa_column=Column(JSON), default_factory=list)
    hazard_class_id: int = Field(foreign_key="hazardclass.id")
    status_id: int = Field(foreign_key="formulastatus.id")
    notes: str | None = None

    user: User = Relationship(back_populates="formulas")
    status: FormulaStatus = Relationship()
    hazard_class: HazardClass = Relationship()
    uploads: list["FileUpload"] = Relationship(back_populates="formula")


class FileUpload(BaseModel, table=True):
    file_name: str
    file_path: str
    content_type: str  # MIME type
    inquiry_id: int | None = Field(default=None, foreign_key="inquiry.id")
    formula_id: int | None = Field(default=None, foreign_key="formula.id")

    __table_args__ = (
        # either inquiry_id or formula_id must be set, but not both
        CheckConstraint(
            "(inquiry_id IS NOT NULL) != (formula_id IS NOT NULL)",
            name="check_parent_xor",
        ),
    )

    inquiry: Inquiry | None = Relationship(back_populates="uploads")
    formula: Formula | None = Relationship(back_populates="uploads")
