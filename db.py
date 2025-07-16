from sqlmodel import create_engine, select, Session, SQLModel

from models import Role, FormulaStatus, HazardClass, Permission, User, Inquiry, Formula

engine = create_engine("sqlite:///database.db", echo=False)


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    SQLModel.metadata.create_all(engine)


def add_mock_data() -> None:
    """Seed the database with minimal but complete demo data."""
    with Session(engine) as session:
        # Abort if already seeded
        if session.exec(select(Role)).first():
            return

        # lookup tables
        statuses = [
            FormulaStatus(code="APP", name="Approved"),
            FormulaStatus(code="REV", name="Under Review"),
            FormulaStatus(code="PEN", name="Pending"),
            FormulaStatus(code="REJ", name="Rejected"),
        ]
        hazards = [
            HazardClass(name="None"),
            HazardClass(name="Flammable"),
            HazardClass(name="Toxic"),
            HazardClass(name="Corrosive"),
        ]

        perms = [
            Permission(code="formula:create", description="Create formulas"),
            Permission(code="formula:read", description="Read formulas"),
            Permission(code="formula:update", description="Update formulas"),
            Permission(code="formula:delete", description="Delete formulas"),
        ]

        session.add_all(statuses)
        session.add_all(hazards)
        session.add_all(perms)

        status_app = next(s for s in statuses if s.code == "APP")
        status_pen = next(s for s in statuses if s.code == "PEN")

        hazard_none = next(h for h in hazards if h.name == "None")
        hazard_flammable = next(h for h in hazards if h.name == "Flammable")

        # roles
        def pick(*codes: str):
            return [p for p in perms if p.code in codes]

        roles = [
            Role(
                name="Nsight Admin",
                description="Nsight Administrator with full access",
                permissions=perms,
            ),
            Role(
                name="Admin",
                description="Company Administrator with most access",
                permissions=pick("formula:create", "formula:read", "formula:update"),
            ),
            Role(
                name="Employee",
                description="Employee with limited access",
                permissions=pick("formula:create", "formula:read"),
            ),
        ]
        session.add_all(roles)
        session.commit()  # IDs now available

        nsight_admin_role, admin_role, employee_role = roles

        # users
        users = [
            User(
                first_name="User1",
                last_name="Last1",
                email="user1@example.com",
                hashed_password=b"pass",
                role=nsight_admin_role,
            ),
            User(
                first_name="User2",
                last_name="Last2",
                email="user2@example.com",
                hashed_password=b"pass",
                role=admin_role,
            ),
            User(
                first_name="User3",
                last_name="Last3",
                email="user3@example.com",
                hashed_password=b"pass",
                role=employee_role,
            ),
        ]
        session.add_all(users)
        session.commit()

        user1, user2, user3 = users

        # formulas
        formulas = [
            Formula(
                user_id=user2.id,
                name="Water",
                ingredients=[
                    {"element": "Hydrogen", "percent": 66},
                    {"element": "Oxygen", "percent": 34},
                ],
                properties={"density": 1.0, "melting_point": 0},
                tags=["liquid", "inorganic"],
                hazard_class_id=hazard_none.id,
                status_id=status_app.id,
                notes="Just water",
            ),
            Formula(
                user_id=user3.id,
                name="SuperSolvent X",
                ingredients=[
                    {"element": "Acetone", "percent": 50},
                    {"element": "Ethanol", "percent": 30},
                    {"element": "Water", "percent": 20},
                ],
                properties={
                    "density": 0.79,
                    "melting_point": -114,
                    "viscosity": 0.32,
                },
                tags=["solvent", "organic"],
                hazard_class_id=hazard_flammable.id,
                status_id=status_pen.id,
                notes="Highly flammable cleaning solvent",
            ),
        ]
        session.add_all(formulas)
        session.commit()

        # inquiries
        inquiries = [
            Inquiry(
                user_id=user1.id,
                prompt="What is the density of water?",
                response="The density of water is 1 g/cm³.",
            ),
            Inquiry(
                user_id=user2.id,
                prompt="What is the melting point of water?",
                response="The melting point of water is 0 °C.",
            ),
            Inquiry(
                user_id=user3.id,
                prompt="What is the boiling point of water?",
                response="The boiling point of water is 100 °C.",
            ),
        ]
        session.add_all(inquiries)
        session.commit()
