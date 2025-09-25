import os


def cd(argc):  # функция, вызываемая по команде cd
	print("cd " + " ".join([i.strip('"') for i in argc]))


def ls(argc):  # функция, вызываемая по команде ls
	print("ls " + " ".join([i.strip('"') for i in argc]))


class unix_emulator:
	dir = "VFS"

	commands = {  # словарь команд и соответсвующих функций функций
		"cd": cd,
		"ls": ls,
		"exit": exit
	}

	def mainLoop(self):
		while True:
			if not os.path.exists("VFS"):  # Если не существует корневой папки VFS -> создаем ее
				os.mkdir("VFS")
				self.dir = "VFS"
			print(self.dir + " >", end=" ")  # вывод приглашения к вводу
			com, *argc = input().split()  # ввод команды и аргрументов
			if com in self.commands:  # если команда имеется в словаре commands, запускаем соответствующую функцию

				# если в списке argc имеются аргументы данные без кавычек -> выводим ошибку
				if [i for i in argc if i[0] != '"' or i[-1] != '"']:
					print(com + ": invalid arguments")
					continue
				self.commands[com](argc)
			else:
				print(com + ": no such command")  # иначе выводим ошибку


init = unix_emulator()
init.mainLoop()
