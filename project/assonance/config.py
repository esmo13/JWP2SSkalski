import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@postgres/asso_pyton'
    SQLALCHEMY_TRACK_MODIFICATIONS = False