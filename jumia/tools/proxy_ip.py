from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Proxy_ip(Base):
    # 表的名字:
    __tablename__ = 'proxy_ip'

    # 表的结构:
    id = Column(int(20), primary_key=True,autoincrement=1)
    ip = Column(String(20))
    port=Column(String(20))


class Getxiciip(object):
    def __init__(self):
        engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/test')
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

    def insert_ip(self,ip,port,session):
        new_ip=Proxy_ip(ip,port)
        session.add(new_ip)
        session.commit()
        session.close()

    def get_proxy_ip(self,session,tablename):
        new_ip=session.query(tablename)
        session.close()
        return new_ip

    def delete_proxy_ip(self,session,tablename,ip):
        delete_ip=session.delete(tablename).fitler(ip=ip)
        session.commit()
        session.close()


