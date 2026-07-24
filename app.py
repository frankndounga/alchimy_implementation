from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

try:
    engine = create_engine('mysql+pymysql://frank:maloul@127.0.0.1:3307/alchemy')
    
except Exception as e:
    print('Error while connecting to the db.')
    raise

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20))
    email = Column(String(40), nullable=False)
    password = Column(String(20), nullable=False)
    tasks = relationship('Task', back_populates='user')

    def __str__(self):
        return f'User: {self.username}, email: {self.email}'

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    description = Column(String(500))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='tasks')

    def __str__(self):
        return f'Task: {self.name}'


Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

def get_user_by_email(session, email):
    user = session.query(User).filter_by(email=email).first()
    if not user:
       print('This user do not exist')
       return
    return user

def check_if_user_exist(session, email):
    if not email:
        print('An email is required')
        return
    user = get_user_by_email(session, email)
    if user:
        return True
    else:
        return False

def insert_user(session):
    email = input('Enter the user\'s email: ')
    if check_if_user_exist(session, email):
        print('This user already exist.')
        return
    
    username = input('Enter the username: ')
    password = input('Enter the password: ')
    user = User(username=username, email=email, password=password)
    session.add(user)
    session.commit()

def update_user(session):
    email = input('Enter the user\'s email: ')
    if not check_if_user_exist(session, email):
        print('Cannot update a user who does not exist.')
        return
    user = get_user_by_email(session, email)
    user.username = input('enter the user username: ') or user.username
    user.email = input('Enter the user email: ') or user.email
    user.password = input('Enter the user password: ') or user.password
    session.commit()

def delete_user(session):
    email = input('Enter the user\'s email: ')
    if not check_if_user_exist(session, email):  
        print('This user do not exist.')
        return
    user = get_user_by_email(session, email)
    session.delete(user)
    session.commit()     

def get_users(session):
    users = session.query(User).all()
    for user in users:
        print(user)

def get_one_user(session):
    email = input('Enter the user\'s email: ')
    user = get_user_by_email(session, email)   
    print(user) 

users = [
    {'username': 'frank', 'email': 'frank@gmail.com', 'password': 'frankpassword'},
    {'username': 'megane', 'email': 'megane@gmail.com', 'password': 'meganepassword'},
    {'username': 'armel', 'email': 'armel@gmail.com', 'password': 'armelpassword'},
    
]

def menu():
    print('=== Menu ===')
    print("1. insert a user")
    print("2. get a specific user")
    print("3. update user")
    print("4. delete user")
    print("5. get all users")
    print("0. to stop the program")

def main():
    action = {
        "1": insert_user,
        "2": get_one_user,
        "3": update_user,
        "4": delete_user,
        "5": get_users
    }

    while True:
        menu()
        choice = input('Select your action: ')

        if choice == "0":
            print('Good bye dear')
            break
        else:
            action[choice](session)


if __name__ == '__main__':
    main()
    