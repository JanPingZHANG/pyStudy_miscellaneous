from orm import Model,StringField,IntegerField

class User(Model):
	__table__='users'
	
	id = IntegerField(primary_key=True)
	name = StringField()

if __name__=='__main__':
	#test
	print(User.id)
