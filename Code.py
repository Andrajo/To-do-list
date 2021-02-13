# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()

class task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field

Base.metadata.create_all(engine)

Session=sessionmaker(bind=engine)
session=Session()



def showcase_today():
    today=datetime.today()
    rows=session.query(task).filter(task.deadline == today.date()).all()
    print("Today {} {}:".format(today.day,today.strftime('%b')))
    if len(rows)==0:
        print("Nothing to do!\n")
    else:
        q=0
        for i in rows:
            q+=1
            print("{}. {}".format(q,i.task))
        print()






def add_to_tasks():
    rows=session.query(task).all()
    task_added=input("Enter task\n")
    deadline_added=datetime.strptime(input("Enter deadline\n"),'%Y-%m-%d')
    print("The task has been added!\n")
    new_task=task(id=len(rows)+1,task=task_added,deadline=deadline_added)
    session.add(new_task)
    session.commit()





def showcase_all_week():
    today=datetime.today()
    week_days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    for i in range(7):
        if i>0:
            day=today+timedelta(days=i)
        else:
            day=today
        print("{} {} {}:".format(week_days[day.weekday()],day.day,day.strftime('%b')))
        rows=session.query(task).filter(task.deadline == day.date()).all()
        if len(rows)==0:
            print("Nothing to do!\n")
        else:
            q=0
            for j in rows:
                q+=1
                print("{}. {}".format(q,j.task))
            print()



def showcase_all():
    rows=session.query(task).order_by(task.deadline).all()
    j=0
    if len(rows)==0:
        print("You have nothing more to do!")    
    else:
        print("All tasks:")
        for i in rows:
            j+=1
            print("{}. {}. {} {}".format(j,i.task,i.deadline.day,i.deadline.strftime('%b')))
        print()





def missed_tasks():
    rows=session.query(task).filter(task.deadline < datetime.today().date()).all()
    if len(rows)==0:
        print("Nothing is missed!\n")
    else:
        q=0
        for i in rows:
            q+=1
            print("{}. {}. {} {}".format(q,i.task,i.deadline.day,i.deadline.strftime('%b')))
        print()




def delete_task():
    print("Choose the number of the task you want to delete:")
    rows=session.query(task).order_by(task.deadline).all()
    j=0
    for i in rows:
        j+=1
        print("{}. {}. {} {}".format(j,i.task,i.deadline.day,i.deadline.strftime('%b')))
    command=int(input())
    print("The task has been deleted!")
    deleted_row=rows[command-1]
    session.delete(deleted_row)
    session.commit()




def startup_menu():
    command=int(input("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit\n"""))
    while command!=0:
        if command==1:
            showcase_today()
        if command==2:
            showcase_all_week()
        if command==3:
            showcase_all()
        if command==4:
            missed_tasks()
        if command==5:
            add_to_tasks()
        if command==6:
            delete_task()
        command=int(input("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit\n"""))
    return "Bye!"


print(startup_menu())


