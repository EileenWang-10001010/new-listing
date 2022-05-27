import os
import logging
import pathlib
import sqlite3
import hashlib
import io
from PIL import ImageFilter
from PIL import Image
import base64
from fastapi import FastAPI, Form, HTTPException, UploadFile,File, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO
images = pathlib.Path(__file__).parent.resolve() / "image"
origins = [ os.environ.get('FRONT_URL', 'http://localhost:3000') ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
)

conn = sqlite3.connect('mercari.sqlite3')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category_id INTEGER,
    image TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY,
    name TEXT
)""")

conn.commit()
conn.close()

sql = """SELECT items.name,category.name as category,items.image
        FROM  items INNER JOIN category
        ON items.category_id =category.id
        """

def hash_img(image):
    image = hashlib.sha256(image.strip('jpg').encode('utf-8')).hexdigest() + '.jpg'
    return image

@app.get("/")
def root():
    return {"message": "Hello, world!"}

@app.get("/items")
async def get_all_items():
    conn = sqlite3.connect('mercari.sqlite3')
    c = conn.cursor()
    c.execute(sql)
    r = [dict((c.description[i][0], value)
                  for i, value in enumerate(row)) for row in c.fetchall()]
    conn.close()
    
    return {"items":r}

@app.get("/search")
async def search_items(keyword: str):
    
    conn = sqlite3.connect('mercari.sqlite3')
    c = conn.cursor()
    # Inner JOIN is advised by yuting0203 and reference to LingYi0612
    c.execute(sql+"WHERE items.name LIKE "+ "'%"+keyword+"%'")
    # list comprehension is reference to LingYi0612
    r_name = [dict((c.description[i][0], value)
                  for i, value in enumerate(row)) for row in c.fetchall()]
    
    c.execute(sql+"WHERE category LIKE "+ "'%"+keyword+"%'")
    r_category = [dict((c.description[i][0], value)
                  for i, value in enumerate(row)) for row in c.fetchall()]

    if len(r_name+r_category)>0:
        return (f"items:{r_name+r_category}")
    else:return("Sorry items are not found, please search for keyword name or category ")

@app.get("/items/{item_id}")
def get_by_id(item_id: int):
    conn = sqlite3.connect('mercari.sqlite3')
    c = conn.cursor()
    c.execute(sql+"WHERE items.id ==(?)",(item_id,))
    item = c.fetchone()
    conn.close()
    try:
        if(len(item)):
            r = {f"name:{item[0]} category:{item[1]} image:{item[2]}"}
            return(f"{r}")
    except:
        return("This index has no related item. Please input another index.")

def resize_image(filename: str):

    image = Image.open(filename, mode="r")
    # logger.info(type(image)) #<class 'PIL.JpegImagePlugin.JpegImageFile'>
    image = image.resize((256,256))
    # image = image.filter(ImageFilter.EDGE_ENHANCE)
    image.save(filename)

@app.post("/items")
async def add_item(background_tasks: BackgroundTasks, name: str = Form(...), category: str = Form(...), image: UploadFile = File(...)):
    conn = sqlite3.connect('mercari.sqlite3')
    c = conn.cursor()
    
    try:
        c.execute("""SELECT * from category WHERE name == (?)""",[category])
        categoryData = c.fetchone()
        if(categoryData == None):
            c.execute("""INSERT INTO category VALUES (?,?)""",(None,category))
            c.execute("""SELECT * from category WHERE name == (?)""",[category])
            categoryData = c.fetchone()

        hashed_image_path = hash_img(image.filename)
        file_location = f"image/{hashed_image_path}"

        with open(file_location, 'wb+') as file_object:  
            file_object.write(image.file.read())
            file_object.close()
            logger.info({"info": f"file '{image.filename}' saved at '{file_location}'"})

        background_tasks.add_task(resize_image, filename=file_location)

        c.execute("""INSERT INTO items VALUES (?,?,?,?)""",(None,name,categoryData[0],hashed_image_path))
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")
    
    conn.commit()
    conn.close()

@app.get("/image/{items_image}")
async def get_image(items_image):
    # Create image path
    image = images / items_image

    if not items_image.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.info(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)
