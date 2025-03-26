import os

# INSTALLED_APPS_LOCATION = "/home/ganesh/calsci/calsci_itr_3/installed_applications"
# APP_LIST_FILE = "/home/ganesh/calsci/calsci_itr_3/process_modules/app_list.py"

INSTALLED_APPS_LOCATION = "installed_applications"
APP_LIST_FILE =   "process_modules/app_list.py"


def add_app_to_list(app_name):
	with open(APP_LIST_FILE, "r") as app_list_file:
		content = app_list_file.read()
	app_list = eval(content.split('=')[1].strip())
	app_list.extend([app_name])
	with open(APP_LIST_FILE, "w") as f:
		f.write(f"app_list = {app_list} \n")

def create_app_file(app_name):
	app_file_path = f"{INSTALLED_APPS_LOCATION}/{app_name}.py"
	with open(app_file_path, "w") as app_to_install:
		app_to_install.write(f"#{app_name}.py \n")
		app_to_install.write(f"print('this is the {app_name}') \n")

def app_installer(app_name):
	add_app_to_list(app_name)
	create_app_file(app_name)
	print(f"{app_name} created successfully \n")

# app_installer('sample2')
