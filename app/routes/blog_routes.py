from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import SessionLocal
from app.auth import get_current_user
from app.logger import logger
from app.aws_client import s3


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload")
async def upload_file(file: UploadFile):
    content = await file.read()
    s3.put_object(Bucket="my-test-bucket", Key=file.filename, Body=content)
    return {"message": "Uploaded to LocalStack S3!"}


# Create a new post with title uniqueness check
@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    # Check if the title already exists and is not soft-deleted
    existing_post = db.query(models.Post).filter(
        models.Post.title == post.title,
        models.Post.is_deleted == False
    ).first()
    if existing_post:
        raise HTTPException(status_code=400, detail="Title already exists. Please choose a different title.")

    return crud.create_post(db, post)


# Get all posts (including deleted ones, with optional filter)
@router.get("/", response_model=list[schemas.Post])
def read_posts(
    skip: int = 0,
    limit: int = 10,
    include_deleted: bool = False,  # Optional parameter to include deleted posts
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    if include_deleted:
        posts = db.query(models.Post).offset(skip).limit(limit).all()
    else:
        posts = db.query(models.Post).filter(models.Post.is_deleted == False).offset(skip).limit(limit).all()
    
    return posts


# List all soft-deleted posts
@router.get("/deleted", response_model=list[schemas.Post])
def view_deleted_posts(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return db.query(models.Post).filter(models.Post.is_deleted.isnot(False)).all()


# Get a specific post by ID (if not deleted)
@router.get("/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    if post_id is None:
        raise HTTPException(status_code=400, detail="Post ID must be provided")
    post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.is_deleted == False).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


# Update a post (only if not deleted)
@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.is_deleted == False).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found or has been deleted")

    updated_post = crud.update_post(db, post_id, post)
    return updated_post


# Soft-delete a post (mark as deleted)
@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    if post_id is None:
        raise HTTPException(status_code=400, detail="Post ID must be provided")
    
    # Fetch the post (only if it's not already deleted)
    post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.is_deleted == False).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or already deleted")
    
    # Mark as deleted (soft delete)
    post.is_deleted = True
    db.commit()  # Save the change in the database
    
    return {"message": "Post soft-deleted successfully"}


# Restore a soft-deleted post
@router.put("/{post_id}/restore")
def restore_post(post_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    if post_id is None:
        raise HTTPException(status_code=400, detail="Post ID must be provided")
    
    # Fetch the post to restore
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # If already active, no need to restore
    if post.is_deleted is False:
        return {"message": "Post is already active"}
    
    # Restore the post
    post.is_deleted = False
    db.commit()
    
    return {"message": "Post restored successfully"}

logger.info("Blog post routes registered successfully.")
