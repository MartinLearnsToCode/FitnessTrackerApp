import kivy
from kivymd.app import MDApp
import sqlite3
from datetime import datetime
from kivy.lang import Builder
#from GUI.ui_classes import show_alert_dialog
#from kivy.core.window import Window
import os

# from kivy import platform
#from android.permissions import request_permissions, Permission
from GUI.ui_classes import MainMenu, WeightScreen, CardioScreen, WellnessScreen




Builder.load_file('GUI/weightscreen.kv')
Builder.load_file('GUI/cardioscreen.kv')
Builder.load_file('GUI/wellnessscreen.kv')
Builder.load_file('GUI/gui.kv')




#request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
#android.permissions = WRITE_EXTERNAL_STORAGE



class MainApp(MDApp):
	def build(self):
		self.db_file_name = "training_diary.db"

		self.folder = '/storage/emulated/0'
		self.db_path = os.path.join(self.folder, self.db_file_name)

		#create db if not exist
		conn = sqlite3.connect(f"{self.db_path}")
		cursor = conn.cursor()
		cursor.execute(f'''
			CREATE TABLE IF NOT EXISTS set_table (
				set_id INTEGER PRIMARY KEY,
				date TEXT,
				time TEXT,
				session INTEGER,
				set_per_exercise INTEGER,
				set_per_session INTEGER,
				category TEXT,
				exercise TEXT,
				reps INTEGER,
				weight REAL,
				cardio_style TEXT,
				minutes REAL,
				notes TEXT
			)
		''')
		conn.commit()
		conn.close()


		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "BlueGray"
		#Window.size = (350, 700)
		self.main_menu = MainMenu() 
		
		return MainMenu()

	# need to be done from an API, stored in DB etc.
	weight_exercises = ['Hyperextensions', 'PullUps', 'Lat Machine', 'ChestPress', 'Rowing Machine', 'AbsPress Machine', 'BackPress Machine', 'Crunch', 'ShoulderPress Machine', 'Triceps Machine', 'Hammer Curls', 'PushUps',]
	cardio_exercises = ['CrossTrainer', 'SteppMill', 'Treadmill', 'Rowing', 'Roadbike']
	wellnessscreen_activites = ['Massage Chair', 'Sauna', 'Massage']
	

	def save_data(self, category='weight', value1=None, value2=None, value3=None):
		if category == 'weight':
			my_dict = WeightScreen.extractData(self, value1, value2, value3)
		elif category == 'cardio':
			my_dict = CardioScreen.extractData(self, value1, value2, value3)
		elif category == 'wellness':
			my_dict = WellnessScreen.extractData(self, value1, value2)
		else:
			return print("category is wrong, save_data() abort!")

		database_name = f"{self.db_path}"
		# Connect to the database or create it if it doesn't exist
		conn = sqlite3.connect(database_name)
		cursor = conn.cursor()

		print("Data to be inserted:")
		print(my_dict)
		# Insert data into the table
		cursor.execute('''
			INSERT INTO set_table (
				set_id, date, time, session, set_per_exercise, set_per_session, category,
				exercise, reps, weight, cardio_style, minutes, notes
			) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
		''', (
			my_dict.get('set_id'),
			my_dict.get('date'),
			my_dict.get('time'),
			my_dict.get('session'),
			my_dict.get('set_per_exercise'),
			my_dict.get('set_per_session'),
			my_dict.get('category'),
			my_dict.get('exercise'),
			my_dict.get('reps'),
			my_dict.get('weight'),
			my_dict.get('cardio_style'),
			my_dict.get('minutes'),
			my_dict.get('notes')
		))
	
		# Commit the changes
		conn.commit()
		conn.close()

	def gather_general_data(self):
		Set = 1  # Initialize Set with a default value
		current_date = datetime.now().strftime("%Y/%m/%d")
		current_time = datetime.now().strftime("%H:%M:%S")
		session = 1
		#set_per_exercise = 1
		#set_per_session = 1
		try:
			# Connect to the SQLite database
			conn = sqlite3.connect(f"{self.db_path}")
			cursor = conn.cursor()

			# Execute a query to count the number of rows in the set_table
			cursor.execute("SELECT COUNT(*) FROM set_table")
			row_count = cursor.fetchone()[0]

			# Check if there are any rows
			if row_count > 0:
				print("There are rows in the set_table.")
				# Get the highest set_id from the database
				cursor.execute("SELECT MAX(set_id) FROM set_table")
				highest_set_id = cursor.fetchone()[0]

				# Set variable "Set" to the highest set_id + 1
				Set = highest_set_id + 1 if highest_set_id is not None else 1

				# Get the highest session from the database
				cursor.execute("SELECT date FROM set_table WHERE set_id = (SELECT MAX(set_id) FROM set_table)")
				highest_session_date = cursor.fetchone()[0]
				
				# Check if the highest session date is the same as the current date
				if highest_session_date is not None and current_date == highest_session_date:
					# Set variable "session" to the highest session if the date is the same
					cursor.execute("SELECT session FROM set_table WHERE set_id = (SELECT MAX(set_id) FROM set_table)")
					session = cursor.fetchone()[0]
				else:
					cursor.execute("SELECT session FROM set_table WHERE set_id = (SELECT MAX(set_id) FROM set_table)")
					session = cursor.fetchone()[0]
					session = session + 1 if session is not None else 1
			else:
				print("The set_table is empty.")
		except sqlite3.Error as e:
			print(f"SQLite error: {e}")

		finally:
			# Close the connection in the finally block to ensure it's always closed
			if conn:
				conn.close()
			# Print or use the variables as needed
		print("MainApp.gather_general_data print out:")
		print("Set:", Set)
		print("Current Date:", current_date)
		print("Session:", session)
		print("Current Time:", current_time)
		return [Set, current_date, current_time, session]
	
	def get_stats_session(self):
		conn = sqlite3.connect(f"{self.db_path}")
		cur = conn.cursor()

		# Execute the query to get the maximum session, fetch result
		cur.execute("SELECT MAX(session) FROM set_table")
		session = cur.fetchone()[0]

		cur.execute("SELECT date FROM set_table WHERE set_id = (SELECT MAX(set_id) FROM set_table)")
		date = cur.fetchone()[0]

		cur.execute(f"SELECT set_id, category, exercise, reps, weight, minutes, cardio_style FROM set_table WHERE session = {session}")
		session_sets = cur.fetchall()

		print(f"Max Session: {session}")
		print(f"Max date: {date}")
		print(f"All sets of current session: {session_sets}")

		conn.close()

if __name__ == '__main__':
    MainApp().run()
