from db_configuration.pgdb_config import Base 
from sqlalchemy import Column , String , Integer , DateTime 
from sqlalchemy.orm  import relationship
import uuid 

class UserOtp(Base):
        __tablename__ = "userotp"
        otp_id = Column(Integer  , primary_key=True , autoincrement= True)
        otp_number = Column(String)
        user_id = Column(Integer , nullable= False)
        email = Column(String, nullable=False )
        expired_time = Column(Integer)
        created_time = Column(DateTime)
        update_time = Column(DateTime)

