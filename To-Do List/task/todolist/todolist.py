from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def Menu():
    print("1) Today's tasks\n"
          "2) Week's tasks\n"
          "3) All tasks\n"
          "4) Missed tasks\n"
          "5) Add task\n"
          "6) Delete task\n"
          "0) Exit")


def AddTask():
    new_row = Table(task=input('Enter task\n'),
                    deadline=datetime.strptime(input("Enter deadline\n"), '%Y-%m-%d').date())
    session.add(new_row)
    session.commit()
    print('The task has been added!')
    print('')


def TodaysTasks(today):
    rows = session.query(Table).filter(Table.deadline == today).all()
    if rows == []:
        print('Nothing to do!')
    else:
        for row in rows:
            print(f'{row.id}. {row.task} - {row.deadline}')
    print('')


def WeeksTasks():
    for i in range(0, 7):
        day = (datetime.today() + timedelta(days=i)).date()
        week_day = {0: 'Monday', 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
        print(f"{week_day[day.weekday()]} {day.day} {day.strftime('%b')}")
        TodaysTasks(day)


def AllTasks():
    rows = session.query(Table).all()
    if not rows:
        print("Nothing to do!")
    else:
        for row in rows:
            print(f'{row.id}. {row.task} - {row.deadline}')
    print('')


def MissedTasks():
    print('Missed tasks:')
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    if rows == []:
        print('Nothing is missed!')
    else:
        for row in rows:
            print(f"{row.id}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
    print('')


def DeleteTask():
    session.query(Table).filter(Table.id == int(input())).delete()
    session.commit()
    print('The task has been deleted!')
    print('')

def ToDo():
    while True:
        Menu()
        choice = int(input())
        if choice == 1:
            print('')
            print(f"Today: {datetime.today().day} {datetime.today().strftime('%b')}")
            TodaysTasks(datetime.today())
        elif choice == 2:
            print('')
            WeeksTasks()
        elif choice == 3:
            print('')
            print("All tasks:")
            AllTasks()
        elif choice == 4:
            print('')
            MissedTasks()
        elif choice == 5:
            print('')
            AddTask()
        elif choice == 6:
            print('')
            print("Chose the number of the task you want to delete:")
            AllTasks()
            DeleteTask()
        elif choice == 0:
            print('\nBye!')
            exit()
        else:
            continue


ToDo()
