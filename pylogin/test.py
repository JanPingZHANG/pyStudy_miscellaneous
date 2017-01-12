import base64

username = '18252431988'
su = base64.b64encode(username.encode('utf-8')).decode('utf-8')
print 'the username is: ',su
password = 'z5827468'
sp = base64.b64encode(password.encode('utf-8')).decode('utf-8')
print 'the password is: ',sp
