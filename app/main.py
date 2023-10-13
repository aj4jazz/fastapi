from random import randrange
from typing import Optional
from fastapi import  Depends, FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import SessionLocal, engine, get_db
from .routers import user, post

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="kfpay-Data-Services-App",
    description="The Data services FastAPI endpoints include get and post methods for receiving a request from the KF Pay Reporting Service application and routing it to get the aggregated result from Databricks workspace",
    summary="Intermediate service to get computed results from Databricks",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Abhisehk Jaiswal",
        "email": "abhishek.jaiswal@kornferry.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


# def get_db():
#     db = SessionLocal()
#     try:
#         yeild db
#     finally:
#         db.close()

    

class Post(BaseModel):
    title: str 
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:
    
    try:
        conn = psycopg2.connect(host="localhost",database="fastapi", user="postgres", 
                                password="password123", cursor_factory=RealDictCursor)
        cursor=conn.cursor();
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to Database failed")
        print("Error", error)
        time.sleep(2)


my_posts = [{"title": "title of Post 1", "content": "content of Post 1", "id": 1},
             {"title": "title of Post 2", "content": "content of Post 1", "id": 2}]
    

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World!!!"}


@app.get("/marketfilters/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    print(posts)
    return {"data":posts}


@app.get("/benchmarkccdata/sqlalchemy/{id}")
def get_posts(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} does not exist! ')
    return {"post_detail":post}





@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    #print(post)
    #print(post.dict())
    return {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}

@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    print(type(id))
    post = find_post(id)
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found!")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found!"}
    return {"post_detail": post}



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return {"message": "Post was successfully deleted"}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict} 


#router
app.include_router(user.router)
app.include_router(post.router)