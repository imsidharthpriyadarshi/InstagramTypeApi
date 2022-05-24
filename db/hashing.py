from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"],deprecated='auto')
class Hash():
    def bcrypt(password: str):
        
        return pwd_context.hash(password)
    
    
    def verify(simple_pass: str, hashed_pass: str):
        return pwd_context.verify(simple_pass,hashed_pass)
        
        