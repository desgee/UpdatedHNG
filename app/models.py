from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

user_organisation = db.Table('user_organisation',
    db.Column('userId', UUID(as_uuid=True), db.ForeignKey('users.userId', ondelete='CASCADE')),
    db.Column('orgId', UUID(as_uuid=True), db.ForeignKey('organisations.orgId', ondelete='CASCADE'))
)

class User(db.Model):
    __tablename__ = 'users'

    userId = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))

    organisations = db.relationship('Organisation', secondary=user_organisation, back_populates='users')

    def __repr__(self):
        return f"<User {self.userId}>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Organisation(db.Model):
    __tablename__ = 'organisations'

    orgId = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    users = db.relationship('User', secondary=user_organisation, back_populates='organisations')
