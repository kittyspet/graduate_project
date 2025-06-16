"""Database models declarations."""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.sqlalchemy import Base
from sqlalchemy import UniqueConstraint


class RecordModel(Base):
    """Simple database model for example."""

    __tablename__ = "records"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )
    record_data: Mapped[str]

    def __repr__(self) -> str:
        """Show string representation of record."""
        return self.record_data


class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )


    # user_id: Mapped[int] = mapped_column(
    #     primary_key=True, autoincrement=True
    # )
    # record_data: Mapped[str]

    full_name: Mapped[str] = mapped_column(
        String, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String, nullable=False
    )

    huid: Mapped[str] = mapped_column(
        String, nullable=False
    )

    chat_id: Mapped[str] = mapped_column(
        String, nullable=False
    )

    accesses: Mapped[list["UserAccess"]] = relationship("UserAccess", back_populates="user", cascade="all, delete-orphan")

    # accesses_user: Mapped[list["UserAccess"]] = relationship("UserAccess", back_populates="user")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, full_name={self.full_name}, huid={self.huid})"

class Roles(Base):
    __tablename__ = "roles"

    role_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )

    designation: Mapped[str] = mapped_column(
        String, nullable=False
    )

    # accesses: Mapped[list["Access"]] = relationship("Access", back_populates="roles")

    def __repr__(self):
        return f"<Role(role_id={self.role_id}, designation={self.designation})"

class Functions(Base):
    __tablename__ = "functions"

    func_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    ) 

    designation: Mapped[str] = mapped_column(
        String, nullable=False
    )

    # accesses: Mapped[list["Access"]] = relationship("Access", back_populates="functions")   

    def __repr__(self):
        return f"<Function(func_id={self.func_id}, designation={self.designation})"

class Programm(Base):
    __tablename__ = "programm"

    programm_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )

    designation: Mapped[str] = mapped_column(
        String, nullable=False
    )
    
    # accesses: Mapped[list["Access"]] = relationship("Access", back_populates="programm")   

    def __repr__(self):
        return f"<Programm(programm_id={self.programm_id}, designation={self.designation})"


class UserAccess(Base):
    __tablename__ = "user_access"
    __table_args__ = (UniqueConstraint('user_id', 'access_id'), )
    
    user_access_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.user_id'), nullable=False
    ) 

    access_id: Mapped[int] = mapped_column(
        ForeignKey('access.access_id'), nullable=False
    )
    
    user: Mapped["Users"] = relationship("Users", back_populates="accesses")
    
    access: Mapped["Access"] = relationship("Access", back_populates="user_accesses")
    
    def __repr__(self):
        return f"<UserAccess(user_access_id={self.user_access_id}, user_id={self.user_id}, access_id={self.access_id})"
    
    # user: Mapped["Users"] = relationship("Users", backref='user_accesses')

    # TODO: unique constrint for user_id id_acces
 
class Access(Base):
    __tablename__ = "access"

    access_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey('roles.role_id'), nullable=False
    )

    func_id: Mapped[int] = mapped_column(
        ForeignKey('functions.func_id'), nullable=False
    )
    programm_id: Mapped[int] = mapped_column(
        ForeignKey('programm.programm_id'), nullable=False
    )

    user_accesses: Mapped[list["UserAccess"]] = relationship("UserAccess", back_populates="access", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Access(access_id={self.access_id})>"
    # roles: Mapped["Roles"] = relationship("Roles", backref='accesses')
    # functions: Mapped["Functions"] = relationship("Functions", backref='accesses')
    # programm: Mapped["Programm"] = relationship("Programm", backref='accesses')

#     def __repr__(self) -> str:
#         """Show string representation of record."""
#         return self.record_data