from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas, models
from .database import SessionLocal, engine
from .database import SessionLocal, engine
from . import models
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
import os

# Ensure tables are created
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create-directory")
def create_directory(data: schemas.DirectoryCreate, db: Session = Depends(get_db)):
    department = crud.get_or_create_department(db, data.department_name)
    directory = crud.create_directory(db, department_id=department.id, directory_name=data.directory_name)
    return {"directory_id": directory.id, "directory_name": directory.name}

@app.post("/create-subdirectory")
def create_subdirectory(data: schemas.SubdirectoryCreate, db: Session = Depends(get_db)):
    department = crud.get_or_create_department(db, data.department_name)
    directory = db.query(models.Directory).filter(
        models.Directory.department_id == department.id,
        models.Directory.name == data.directory_name
    ).first()

    if not directory:
        raise HTTPException(status_code=404, detail="Directory not found")

    subdirectory = crud.create_subdirectory(db, directory_id=directory.id, subdirectory_name=data.subdirectory_name)
    return {"subdirectory_id": subdirectory.id, "subdirectory_name": subdirectory.name}

# @app.post("/upload-md-file")
# async def upload_md_file(department_name: str, directory_name: str, subdirectory_name: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
#     # Ensure directory exists
#     department = crud.get_or_create_department(db, department_name)
#     directory = db.query(models.Directory).filter(models.Directory.department_id == department.id, models.Directory.name == directory_name).first()
#     subdirectory = db.query(models.Subdirectory).filter(models.Subdirectory.directory_id == directory.id, models.Subdirectory.name == subdirectory_name).first()

#     # Save the file
#     path = f"./app/file_uploads/{department_name}/{directory_name}/{subdirectory_name}"
#     os.makedirs(path, exist_ok=True)
#     file_location = f"{path}/{file.filename}"
#     with open(file_location, "wb") as file_object:
#         file_object.write(file.file.read())

    # return {"message": f"File {file.filename} uploaded successfully to {file_location}"}
# @app.post("/upload-md-file")
# async def upload_md_file(
#     department_name: str, 
#     directory_name: str, 
#     subdirectory_name: str, 
#     file: UploadFile = File(...), 
#     db: Session = Depends(get_db)
# ):
#     # Ensure department exists
#     department = crud.get_or_create_department(db, department_name)
    
#     # Check if the directory exists within the department
#     directory = db.query(models.Directory).filter(
#         models.Directory.department_id == department.id,
#         models.Directory.name == directory_name
#     ).first()
    
#     if not directory:
#         raise HTTPException(status_code=404, detail="Directory not found in specified department")
    
#     # Check if the subdirectory exists within the directory
#     subdirectory = db.query(models.Subdirectory).filter(
#         models.Subdirectory.directory_id == directory.id, 
#         models.Subdirectory.name == subdirectory_name
#     ).first()

#     if not subdirectory:
#         raise HTTPException(status_code=404, detail="Subdirectory not found in specified directory")
    
#     # Save the file to the designated path
#     path = f"./app/file_uploads/{department_name}/{directory_name}/{subdirectory_name}"
#     os.makedirs(path, exist_ok=True)
#     file_location = f"{path}/{file.filename}"
    
#     with open(file_location, "wb") as file_object:
#         file_object.write(file.file.read())
    
#     return {"message": f"File {file.filename} uploaded successfully to {file_location}"}

# @app.post("/upload-md-file")
# async def upload_md_file(
#     department_name: str, 
#     directory_name: str = None, 
#     subdirectory_name: str = None, 
#     file: UploadFile = File(...), 
#     db: Session = Depends(get_db)
# ):
#     # Ensure department exists
#     department = db.query(models.Department).filter(models.Department.name == department_name).first()
#     if not department:
#         raise HTTPException(status_code=404, detail="Department not found")

#     # Fetch directories and subdirectories for the given department
#     directories = db.query(models.Directory).filter(models.Directory.department_id == department.id).all()
#     folder_structure = {directory.name: [] for directory in directories}
    
#     # Populate subdirectories in the folder structure
#     for directory in directories:
#         subdirectories = db.query(models.Subdirectory).filter(models.Subdirectory.directory_id == directory.id).all()
#         folder_structure[directory.name] = [subdirectory.name for subdirectory in subdirectories]
    
#     # Validate directory and subdirectory names, if provided
#     selected_directory = db.query(models.Directory).filter(
#         models.Directory.department_id == department.id,
#         models.Directory.name == directory_name
#     ).first() if directory_name else None
    
#     if directory_name and not selected_directory:
#         raise HTTPException(status_code=404, detail="Directory not found in specified department")
    
#     # Check subdirectory if provided
#     selected_subdirectory = None
#     if subdirectory_name:
#         selected_subdirectory = db.query(models.Subdirectory).filter(
#             models.Subdirectory.directory_id == selected_directory.id,
#             models.Subdirectory.name == subdirectory_name
#         ).first()
#         if not selected_subdirectory:
#             raise HTTPException(status_code=404, detail="Subdirectory not found in specified directory")
    
#     # Determine upload path based on provided directory/subdirectory
#     if selected_directory and selected_subdirectory:
#         path = f"./app/file_uploads/{department_name}/{directory_name}/{subdirectory_name}"
#     elif selected_directory:
#         path = f"./app/file_uploads/{department_name}/{directory_name}"
#     else:
#         raise HTTPException(status_code=400, detail="No valid directory selected for upload")

#     os.makedirs(path, exist_ok=True)  # Create the path if it doesn’t exist
#     file_location = f"{path}/{file.filename}"

#     with open(file_location, "wb") as file_object:
#         file_object.write(file.file.read())
    
#     return {
#         "message": f"File {file.filename} uploaded successfully to {file_location}",
#         "folder_structure": folder_structure  # Return folder structure for reference
#     }

@app.post("/upload-md-file")
async def upload_md_file(
    department_name: str, 
    directory_name: str, 
    subdirectory_name: str = None,  # Optional subdirectory
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    # Ensure department exists
    department = db.query(models.Department).filter(models.Department.name == department_name).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    # Fetch the specified directory within the department
    directory = db.query(models.Directory).filter(
        models.Directory.department_id == department.id,
        models.Directory.name == directory_name
    ).first()
    
    if not directory:
        raise HTTPException(status_code=404, detail="Directory not found in specified department")

    # If subdirectory_name is provided, validate it and set the upload path accordingly
    if subdirectory_name:
        subdirectory = db.query(models.Subdirectory).filter(
            models.Subdirectory.directory_id == directory.id,
            models.Subdirectory.name == subdirectory_name
        ).first()

        if not subdirectory:
            raise HTTPException(status_code=404, detail="Subdirectory not found in specified directory")

        # Path with subdirectory
        path = f"./app/file_uploads/{department_name}/{directory_name}/{subdirectory_name}"
    else:
        # Path without subdirectory (only directory)
        path = f"./app/file_uploads/{department_name}/{directory_name}"

    # Ensure the path exists
    os.makedirs(path, exist_ok=True)
    file_location = f"{path}/{file.filename}"

    # Save the file
    with open(file_location, "wb") as file_object:
        file_object.write(file.file.read())
    
    return {
        "message": f"File {file.filename} uploaded successfully to {file_location}"
    }

@app.get("/get-folder-structure")
def get_folder_structure(department_name: str, db: Session = Depends(get_db)):
    # Ensure the department exists
    department = db.query(models.Department).filter(models.Department.name == department_name).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    # Retrieve directories in the department
    directories = db.query(models.Directory).filter(models.Directory.department_id == department.id).all()
    folder_structure = []

    for directory in directories:
        # Retrieve subdirectories for each directory
        subdirectories = db.query(models.Subdirectory).filter(models.Subdirectory.directory_id == directory.id).all()
        
        # Build the structure for each directory
        dir_info = {
            "directory_name": directory.name,
            "subdirectories": []
        }

        for subdirectory in subdirectories:
            # Fetch files in the corresponding directory and subdirectory path
            path = f"./app/file_uploads/{department_name}/{directory.name}/{subdirectory.name}"
            files = []
            if os.path.exists(path):
                files = os.listdir(path)  # List all files in the subdirectory

            # Add subdirectory and its files to the directory info
            dir_info["subdirectories"].append({
                "subdirectory_name": subdirectory.name,
                "files": files
            })

        # Append directory info to the folder structure
        folder_structure.append(dir_info)

    return {"department_name": department_name, "folder_structure": folder_structure}
