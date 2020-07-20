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

	package_json_file = os.path.join(project_root, "package.json")

	if not os.path.isfile(package_json_file):
		print("{} App folder does not have package.json file. {}".format(bcolors.WARNING, bcolors.ENDC))
		project_name = os.getenv("PROJECT_NAME")

		if not project_name:
			sys.exit(os.EX_OSFILE)

		create_angular_command = ["ng", "new", "--directory", project_root, "--defaults", "true", project_name]
		angular_result = subprocess.run(create_angular_command, 
			stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		if angular_result.stderr:
			print("{0} {1} {2}".format(bcolors.FAIL, angular_result.stderr.decode(), bcolors.ENDC))
			sys.exit(angular_result.returncode)
		else:
			print("{0} Project created {1}".format(bcolors.OKGREEN, bcolors.ENDC))

	else:

		print("Installing dependencies")
		subprocess.call(["npm", "install", "--prefix", project_root])

		print("{0} All dependencies are installed {1}".format(bcolors.OKGREEN, bcolors.ENDC))

	exec_command(sys.argv)


def exec_command(args: []):
	#['docker-entrypoint.py', 'ng', 'serve']
	# I delete firts element and check if the second element is manage.py and third element is runsever
	del args[0]
	if args:
		subprocess.run(args)


if __name__ == "__main__":
		run()