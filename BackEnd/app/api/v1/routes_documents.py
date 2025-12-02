from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.session import get_db
from app.db.models import Document, Animal, User
from app.core.dependencies import get_current_user
import os
from datetime import datetime
import shutil

router = APIRouter()

# Configure upload directory
UPLOAD_DIR = "uploads/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Allowed file types
ALLOWED_EXTENSIONS = {
    'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx', 'txt'
}
ALLOWED_MIME_TYPES = {
    'application/pdf',
    'image/jpeg',
    'image/png',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain'
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def get_file_extension(filename: str) -> str:
    """Extract file extension from filename."""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''


def validate_file(file: UploadFile) -> None:
    """Validate uploaded file."""
    # Check file extension
    ext = get_file_extension(file.filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type: {file.content_type}"
        )


@router.post("/animals/{animal_id}/documents")
async def upload_document(
    animal_id: int,
    file: UploadFile = File(...),
    document_type: str = Form(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a document for an animal (vaccination record, certificate, etc.).
    """
    # Check if animal exists
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    # Validate file
    validate_file(file)
    
    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # Generate unique filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    ext = get_file_extension(file.filename)
    safe_filename = f"animal_{animal_id}_{timestamp}_{current_user.id}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )
    
    # Create document record
    document = Document(
        animal_id=animal_id,
        document_type=document_type,
        file_name=file.filename,
        file_path=file_path,
        file_size=file_size,
        mime_type=file.content_type,
        description=description,
        uploaded_by=current_user.id
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return {
        "id": document.id,
        "animal_id": document.animal_id,
        "document_type": document.document_type,
        "file_name": document.file_name,
        "file_size": document.file_size,
        "description": document.description,
        "uploaded_at": str(document.uploaded_at),
        "uploaded_by": current_user.username
    }


@router.get("/animals/{animal_id}/documents")
def get_animal_documents(
    animal_id: int,
    document_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all documents for an animal, optionally filtered by type.
    """
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    query = db.query(Document).filter(Document.animal_id == animal_id)
    
    if document_type:
        query = query.filter(Document.document_type == document_type)
    
    documents = query.order_by(Document.uploaded_at.desc()).all()
    
    result = []
    for doc in documents:
        uploader = db.query(User).filter(User.id == doc.uploaded_by).first()
        result.append({
            "id": doc.id,
            "document_type": doc.document_type,
            "file_name": doc.file_name,
            "file_size": doc.file_size,
            "mime_type": doc.mime_type,
            "description": doc.description,
            "uploaded_at": str(doc.uploaded_at),
            "uploaded_by": uploader.username if uploader else "Unknown"
        })
    
    return {
        "animal_id": animal_id,
        "animal_name": animal.name,
        "documents": result,
        "total": len(result)
    }


@router.get("/documents/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Get document details by ID.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    uploader = db.query(User).filter(User.id == document.uploaded_by).first()
    animal = db.query(Animal).filter(Animal.id == document.animal_id).first()
    
    return {
        "id": document.id,
        "animal_id": document.animal_id,
        "animal_name": animal.name if animal else "Unknown",
        "document_type": document.document_type,
        "file_name": document.file_name,
        "file_size": document.file_size,
        "mime_type": document.mime_type,
        "description": document.description,
        "uploaded_at": str(document.uploaded_at),
        "uploaded_by": uploader.username if uploader else "Unknown"
    }


@router.delete("/documents/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a document. Only the uploader or admin can delete.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check permissions
    if document.uploaded_by != current_user.id and current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this document"
        )
    
    # Delete file from filesystem
    try:
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
    except Exception as e:
        print(f"Warning: Failed to delete file {document.file_path}: {str(e)}")
    
    # Delete database record
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}


@router.get("/documents/types")
def get_document_types():
    """
    Get available document types.
    """
    return {
        "document_types": [
            {"value": "vaccination_record", "label": "Vaccination Record"},
            {"value": "certificate", "label": "Certificate"},
            {"value": "test_result", "label": "Test Result"},
            {"value": "health_record", "label": "Health Record"},
            {"value": "movement_permit", "label": "Movement Permit"},
            {"value": "other", "label": "Other"}
        ]
    }
