from pydantic import BaseModel

class DirectoryCreate(BaseModel):
    department_name: str
    directory_name: str

class SubdirectoryCreate(BaseModel):
    department_name: str
    directory_name: str
    subdirectory_name: str
