#!/usr/bin/python3

import subprocess
import os
import sys
import time

project_root = "/usr/src/app"

class bcolors:

    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def run():

	requirements_file = os.path.join(project_root, "requirements.txt")
	manage_file = os.path.join(project_root, "manage.py")

	if not os.path.isfile(requirements_file):
		print("{} App folder does not have the requirements.txt file, you can create it by executing: {}".format(bcolors.WARNING, bcolors.ENDC))
		print("{} pip freeze > requirements.txt {}".format(bcolors.WARNING, bcolors.ENDC))
		sys.exit(os.EX_OSFILE)

	freee_command = ["pip", "freeze", "-r", requirements_file]
	result = subprocess.run(freee_command, 
		stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	if result.returncode != 0:
		print("{0} {1} {2}".format(bcolors.FAIL, result.stderr.decode(), bcolors.ENDC))
		sys.exit(result.returncode)

	if result.stderr:

		uninstalled = result.stderr.decode().strip().split("\n")
		"""
		WARNING: Requirement file [/usr/src/app/requirements.txt] contains request==2019.4.13, but package 'request' is not installed
		I use split to that message, position 67 is where start package name
		"""
		uninstalled = [x.split(",")[0][67:] for x in uninstalled]

		for package in uninstalled:
			if len(package.split("==")) == 1:
				print("{0} WARNING: {1} package does not specify version {2}".format(bcolors.WARNING, package, bcolors.ENDC))

		print("Installing dependencies")
		subprocess.call(["pip", "install", "-r", requirements_file])


	print("{0} All dependencies are installed {1}".format(bcolors.OKGREEN, bcolors.ENDC))


	if not os.path.isfile(manage_file):
		print("{} There is not django project. {}".format(bcolors.WARNING, bcolors.ENDC))
		project_name = os.getenv("PROJECT_NAME", default="project")
		print("{0} Creating django project. Running  django-admin startproject {1} . {2}".format(bcolors.WARNING, project_name, bcolors.ENDC))
		create_django_command = ["django-admin", "startproject", project_name, "."]
		django_result = subprocess.run(create_django_command, 
			stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		if django_result.stderr:
			print("{0} {1} {2}".format(bcolors.FAIL, django_result.stderr.decode(), bcolors.ENDC))
			sys.exit(django_result.returncode)

		print("{} Successfully created project {}".format(bcolors.OKGREEN, bcolors.ENDC))

	exec_command(sys.argv)


def exec_command(args: []):
	#['docker-entrypoint.py', 'python', '/usr/src/app/manage.py', 'runserver']
	# I delete firts element and check if the second element is manage.py and third element is runsever
	del args[0]
	if args:
		if ((args[1] == 'manage.py' or args[1] == os.path.join(project_root, 'manage.py')) 
			and args[2] == 'runserver'):

			while True:
				try:
					subprocess.run(args, check=True )

				except subprocess.CalledProcessError as e:
					if e.returncode == 1:
						time.sleep(2)
					else:
						print("{0} Error executing: {1} {2}".format(bcolors.FAIL, " ".join(e.cmd), bcolors.ENDC))
						return
		else:
			subprocess.run(args)


if __name__ == "__main__":
	run()
