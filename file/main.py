from fastapi import FastAPI
from sqlalchemy import delete
from sqlmodel import SQLModel, Session, create_engine, Field, select

DATABASE_KEY = 'postgresql://neondb_owner:fsc1HhEBpxJ7@ep-proud-wildflower-a10j8u22.ap-southeast-1.aws.neon.tech/todo?sslmode=require'

class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    task: str

engine = create_engine(DATABASE_KEY, echo=True)

SQLModel.metadata.create_all(engine)

app = FastAPI()
@app.get("/todo")
def get_todo():
    with Session(engine) as session:
        todo = session.exec(select(Todo)).all()
    return todo
   
@app.post("/todo")
def add_todo(task:str):
     with Session(engine) as session:
         session.add(Todo(task=task))
         session.commit()
         return "Task added Successfully"
     
@app.put("/todo")
def edit_todo(id:int,new_task:str):
    with Session(engine) as session:
        todo = session.exec(select(Todo).where(id== Todo.id)).one()
        todo.task = new_task
        session.add(todo)
        session.commit()
    return "Task updated Successfully"

@app.delete("/todo")
def delete_todo(id:int):
    with Session(engine) as session:
        session.exec(delete(Todo).where(id== Todo.id))
        session.commit()
    return "Task deleted Successfully"
    