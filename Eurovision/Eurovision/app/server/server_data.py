from datetime import datetime

class Server_Room():
	visitor_ids = []
	name = ""

	def __init__(self, name):
		self.name = name

	def get_room_name(self):
		return self.name

	def add_user(self, id):
		self.visitor_ids.append(id)
		print("Adding user {} to room {}. There are now {} users in this room.".format(id, self.name, len(self.visitor_ids)))

	def remove_user(self, id):
		if id in self.visitor_ids:
			self.visitor_ids.remove(id)
			print("Removing user {} from room {}".format(id, self.name))

	def is_user_in_room(self, id):
		if id in self.visitor_ids:
			return True
		return False

class Local_Server_Data():
	start_time = datetime(2019, 5, 11, 20)

	rooms = []
	currently_logged_in_users = []
	
	def __init__(self):
		self.create_test_rooms()

	def create_test_rooms(self):
		self.add_room("Edinburgh")
		self.add_room("London")
		self.add_room("Spain")

	def add_room(self, name):
		self.rooms.append(Server_Room(name))
		print("Creating room {} ".format(name))

	def close_room(self, name):
		for room in self.rooms:
			if room.get_room_name() == name:
				self.rooms.remove(room)
				print("Removing room {} ".format(name))
	
	def get_room(self, name):
		for room in self.rooms:
			if room.get_room_name() == name:
				return room

	def remove_user_from_any_room(self, id):
		for room in self.rooms:
			if room.is_user_in_room(id):
				room.remove_user(id)
				print("Removed user {} from room {}".format(id, room.get_room_name()))

	def is_user_logged_in(self, user_id):
		return user_id in self.currently_logged_in_users

	def set_user_logged_in(self, user_id):
		if self.is_user_logged_in(user_id):
			print("User {} is already logged in".format(user_id))
			return

		self.currently_logged_in_users.append(user_id)
		print("Logging user {} in".format(user_id))

	# more for completeness' sake
	def set_user_logged_out(self, user_id):
		if not self.is_user_logged_in(user_id):
			print("User {} isn't logged in".format(user_id))
			return

		self.currently_logged_in_users.remove(user_id)
		print("Removing user {}".format(user_id))
