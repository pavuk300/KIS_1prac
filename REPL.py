from sys import argv
from os import path


def startup():
	if len(argv) != 3:
		print("invalid set of arguments")
		exit()
	if "C:\\" not in argv[1]:
		argv[1] = path.dirname(__file__) + "\\" + argv[1]
	if "C:\\" not in argv[2]:
		argv[2] = path.dirname(__file__) + "\\" + argv[2]
	if not (path.exists(argv[1]) or path.exists(argv[2])):
		print("invalid set of arguments")
		exit()
	print("\nVfs location -> " + argv[1])
	print("Startup script -> " + argv[2], end="\n\n")


def cd(argc):  # функция, вызываемая по команде cd
	return "cd " + " ".join([i.strip('"') for i in argc])


def ls(argc):  # функция, вызываемая по команде ls
	return "ls " + " ".join([i.strip('"') for i in argc])


class UnixEmulator:
	dir = "VFS"

	commands = {  # словарь команд и соответсвующих функций функций
		"cd": cd,
		"ls": ls,
		"exit": exit
	}

	def init_command(self, com, argc):
		if com in self.commands:  # если команда имеется в словаре commands, запускаем соответствующую функцию

			# если в списке argc имеются аргументы данные без кавычек -> выводим ошибку
			if [i for i in argc if i[0] != '"' or i[-1] != '"']:
				return [com + ": invalid arguments", False]
			return [self.commands[com](argc), True]
		else:
			return [com + ": no such command", False]  # иначе выводим ошибку

	def startup_script(self):
		out = ""
		print("Startup script:\n")
		with open(argv[2]) as f:
			for i in f:
				com, *argc = i.split()
				buf = self.init_command(com, argc)
				if not buf[1]:
					print("The script terminated with an error\n")
					return
				out += buf[0] + "\n"
		print(out)

	def main_loop(self):
		startup()
		self.startup_script()
		while True:
			print(self.dir + " >", end=" ")  # вывод приглашения к вводу
			com, *argc = input().split()  # ввод команды и аргрументов
			print(self.init_command(com, argc)[0])


UnixEmulator().main_loop()
