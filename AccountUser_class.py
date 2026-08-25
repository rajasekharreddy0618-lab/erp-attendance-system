import hashlib

class UserAccount:
    def __init__(self,Username,raw_password):
        self.Username=Username
        self.raw_password=raw_password

        self.encode=self.raw_password.encode("utf-8")
        self.password_hash=hashlib.sha256(self.encode).hexdigest()
        self.is_active=True

    def verify_password(self,input_password:str)->bool:
        self.input_password=input_password
        self.pass_encode=self.input_password.encode("utf-8")
        self.input_password=hashlib.sha256(self.pass_encode).hexdigest()

        if self.input_password==self.password_hash:
            return True
        else:
            return False
        
A1=UserAccount("Raju","#ACK2S")

print("Hashed password:",A1.password_hash)

print(A1.verify_password("#ACK2S"))