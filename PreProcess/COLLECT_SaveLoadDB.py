# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

__DB_PATH__ = '../data/himmr.db'
__DEMO_DATA__ = [{'url': 'https://github.com/0wliver',
                 'title': '0wliver', 
                 'content_line': ['https://github.com/', '0wliver'], 
                 'content_all':'https://github.com/0wliver', 
                 'personal_info': {'sex': '0', 
                                   'birth': '0', 
                                   'school': '0', 
                                   'subject': '0', 
                                   'job': '0', 
                                   'location': '0', 
                                   'hometown': '0', 
                                   'sign': '0', 
                                   'height': '0'}}]

# create a mapping base class
# 创建映射基类
Base = declarative_base()   

# definite tables     
# 定义数据表
class Raw(Base):    
    __tablename__ = 'raw_data' # 表名
    id = Column(Integer, primary_key=True)
    data = Column(Text)
    title = Column(String(50))
    url = Column(String(1000))
    
class Person(Base):
    __tablename__ = 'person_info'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    birth = Column(String(100))
    height = Column(String(100))
    hometown = Column(String(100))
    job = Column(String(100))
    location = Column(String(100))
    school = Column(String(100))
    sex = Column(String(100))
    sign = Column(String(100))
    subject = Column(String(100))
    title = Column(String(50))
    url = Column(String(1000))


# save data to target path like 'test.db'
def save_to_path(list_info, db_path):
    # connect database
    DB_CONNECT_STRING = 'sqlite:///' + db_path
    engine = create_engine(DB_CONNECT_STRING)   # echo=True: show operate echo
    
    # establish a session
    DBSession = sessionmaker(bind=engine)    # 以上两句可合成 Session = sessionmaker(bind=engine)
    session = DBSession()
    
    # execute a creating operation
    # 执行创建(若已有该对象则不需要创建)
    Base.metadata.create_all(engine)
    
    #------------------------------------#
    for li in list_info:
        raw_insert = Raw(data=str(li), title=li['title'], url=li['url'])
        person_insert = Person(content=li['content_all'],
                               birth=li['personal_info']['birth'],
                               height=li['personal_info']['height'],
                               hometown=li['personal_info']['hometown'],
                               job=li['personal_info']['job'],
                               location=li['personal_info']['location'],
                               school=li['personal_info']['school'],
                               sex=li['personal_info']['sex'],
                               sign=li['personal_info']['sign'],
                               subject=li['personal_info']['subject'],
                               title=li['title'],
                               url=li['url'])
        
        session.add(raw_insert)
        session.add(person_insert)
    
    try:
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        return True
    
    #------------------------------------#
    
    # Base.metadata.drop_all(engine) 
    

# load and return a session from target path like 'test.db'
def load_from_path(db_path):   
    # connect database
    engine = create_engine('sqlite:///' + db_path) # echo=True: show operate echo
    
    # establish a session
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    return session
    

if __name__ == '__main__':
    save_to_path(list_info=__DEMO_DATA__, db_path=__DB_PATH__)
    session = load_from_path(db_path=__DB_PATH__)
