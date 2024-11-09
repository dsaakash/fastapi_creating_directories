from sqlalchemy.orm import Session
from . import models, schemas

def get_or_create_department(db: Session, department_name: str):
    department = db.query(models.Department).filter(models.Department.name == department_name).first()
    if not department:
        department = models.Department(name=department_name)
        db.add(department)
        db.commit()
        db.refresh(department)
    return department

def create_directory(db: Session, department_id: int, directory_name: str):
    directory = models.Directory(name=directory_name, department_id=department_id)
    db.add(directory)
    db.commit()
    db.refresh(directory)
    return directory

def create_subdirectory(db: Session, directory_id: int, subdirectory_name: str):
    subdirectory = models.Subdirectory(name=subdirectory_name, directory_id=directory_id)
    db.add(subdirectory)
    db.commit()
    db.refresh(subdirectory)
    return subdirectory
