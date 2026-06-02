from passlib.context import CryptContext

"""
	pip3 install "passlib[bcrypt]==1.7.4"
	
	用户密码
"""

#创建上下文
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 加密
def crypt(password_text: str):
	return crypt_context.hash(password_text)


#校验
def verify(password_text: str, hashed_text: str):
	return crypt_context.verify(password_text, hashed_text)