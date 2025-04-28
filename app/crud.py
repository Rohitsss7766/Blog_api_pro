from datetime import datetime
from sqlalchemy.orm import Session
from app import models, schemas

# Create a new post
def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Get active (non-deleted) posts only
def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Post)
        .filter(models.Post.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )

# Get a single active (non-deleted) post by ID
def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(
        models.Post.id == post_id,
        models.Post.is_deleted == False
    ).first()

# Update an existing post (only if not deleted)
def update_post(db: Session, post_id: int, post: schemas.PostCreate):
    db_post = db.query(models.Post).filter(
        models.Post.id == post_id,
        models.Post.is_deleted == False
    ).first()
    if db_post:
        db_post.title = post.title
        db_post.content = post.content
        db_post.author = post.author
        db_post.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_post)
    return db_post

# Soft delete (set is_deleted = True instead of deleting)
def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post and not db_post.is_deleted:
        db_post.is_deleted = True
        db.commit()
        return True
    return False

# View deleted posts only
def get_deleted_posts(db: Session):
    return db.query(models.Post).filter(models.Post.is_deleted == True).all()

# Restore a soft-deleted post
def restore_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post and db_post.is_deleted:
        db_post.is_deleted = False
        db.commit()
        return db_post
    return None
