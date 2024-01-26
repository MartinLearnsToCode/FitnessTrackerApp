from kivymd.uix.screen import MDScreen

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.spinner import Spinner, SpinnerOption
from kivymd.uix.datatables import MDDataTable

# sort import out!!!


class MainMenu(MDScreen):
	dialog = None
	def show_alert_dialog(self):
		if not self.dialog:
			self.dialog = MDDialog(
				title="Set saved",
				text= "Set-Data has been saved!",
				buttons=[
					MDRectangleFlatButton(
						text="Okay",
						theme_text_color="Custom",
						on_release = self.close_dialog,
						pos_hint={"center_x": 0.5, "center_y": 0.5}
					),
				],
			)
		self.dialog.open()
	def close_dialog(self, obj):
		self.dialog.dismiss()



class WeightScreen(MDScreen):
	def extractData(self, exercise, reps, weight):
		app = MDApp.get_running_app()
		reps = int(reps.strip())
		weight = float(weight.strip().replace(',', '.')) if weight != '' else ''
		generel_data = app.gather_general_data()
		data = {
			"set_id" : generel_data[0],
			"date" : generel_data[1],
			"time" : generel_data[2],
			"session" : generel_data[3],
			"set_per_exercise" :"",
			"set_per_session" : "",
			"category" : "weight",
			"exercise" : exercise,
			"reps" : reps,
			"weight" : weight,
			"cardio_style" : None,
			"minutes" : None,
			"Notes" : None
		}
		print("WeightScreen.extractData print:")
		print(data)
		return data




class CardioScreen(MDScreen):
	def extractData(self, exercise, min, style):
		app = MDApp.get_running_app()
		min = float(min.strip().replace(',', '.')) if min != '' else ''
		generel_data = app.gather_general_data()
		data = {
			"set_id" : generel_data[0],
			"date" : generel_data[1],
			"time" : generel_data[2],
			"session" : generel_data[3],
			"set_per_exercise" :"",
			"set_per_session" : "",
			"category" : "cardio",
			"exercise" : exercise,
			"reps" : None,
			"weight" : None,
			"cardio_style" : style,
			"minutes" : min,
			"Notes" : None
		}
		print("WeightScreen.extractData print:")
		print(data)
		return data

class WellnessScreen(MDScreen):
	def extractData(self, activity, min):
		app = MDApp.get_running_app()
		min = float(min.strip().replace(',', '.')) if min != '' else ''
		generel_data = app.gather_general_data()
		data = {
			"set_id" : generel_data[0],
			"date" : generel_data[1],
			"time" : generel_data[2],
			"session" : generel_data[3],
			"set_per_exercise" :"",
			"set_per_session" : "",
			"category" : "wellness",
			"exercise" : activity,
			"reps" : None,
			"weight" : None,
			"cardio_style" : None,
			"minutes" : min,
			"Notes" : None
		}
		print("WeightScreen.extractData print:")
		print(data)
		return data

class ContentNavigationDrawer(MDBoxLayout):
	pass

class TrainScreen(MDBoxLayout):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	pass

class TrainingsPlanScreen(MDBoxLayout):
	pass

class SettingsScreen(MDBoxLayout):
	pass

class DesignTrainingsPlanScreen(MDBoxLayout):
	pass

class ShowDataScreen(MDBoxLayout):
	pass



class SelectExerciseScreen(MDBoxLayout):
	pass

class CustomSpinnerOption(SpinnerOption):
    pass

"""
sadly: infinite loop. dont know why...

class LimitInput(MDTextField):
    def on_text(self, instance, value):
        # Unbind the on_text event temporarily to avoid infinite loop
        self.unbind(on_text=self.on_text)

        # Truncate the text to the first 5 characters
        if len(self.text) > 5:
            self.text = self.text[:4]

        # Rebind the on_text event
        self.bind(on_text=self.on_text)"""
