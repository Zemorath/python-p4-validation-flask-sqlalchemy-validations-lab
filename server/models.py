from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validate_name(self, key, address):
        if address == '':
            raise ValueError("Name can not be empty")
        elif Author.query.filter_by(name=address).first() is not None:
            raise ValueError("Name already exists")
        return address
    
    @validates("phone_number")
    def validate_phone_number(self, key, address):
        if len(address) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        elif address.isdigit() == False:
            raise ValueError("Phone number must contain only numbers")
        return address



    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('title')
    def validate_title(self, key, title):
        list = ["Won't Believe", "Secret", "Top", "Guess"]
        if not title:
            raise ValueError("Title must not be blank")
        elif any(ele in title for ele in list) == False:
            raise ValueError("Title must contain wow words!")
        return title


    @validates('content')
    def validate_content(self, key, address):
        if len(address) < 250:
            raise ValueError("Must be at least 250 characters")
        return address
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary must have no more than 250 characters")
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError("Category must be either fiction or non-fiction")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
