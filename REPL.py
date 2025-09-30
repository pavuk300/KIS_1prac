from sys import argv
from os import path


dir = "VFS"

def startup(): # Считавыние параметров командной строки и их проверка
	if len(argv) != 3: # Если передан неправильный набор аргументов
		print("invalid set of arguments")
		exit()
	if "C:\\" not in argv[1]: # Если не указан полный путь до VFS
		argv[1] = path.dirname(__file__) + "\\" + argv[1]
	if "C:\\" not in argv[2]: # Если не указан полный путь до стартого скрипта
		argv[2] = path.dirname(__file__) + "\\" + argv[2]
	if not (path.exists(argv[1]) or path.exists(argv[2])): # Если не существует одного из файлов выводим ошибку
		print("invalid set of arguments")
		exit()
	print("\nVfs location -> " + argv[1])
	print("Startup script -> " + argv[2], end="\n\n")


def cd(argc):  # функция, вызываемая по команде cd
	return "cd " + " ".join([i.strip('"') for i in argc])


def ls(argc):  # функция, вызываемая по команде ls
	return "ls " + " ".join([i.strip('"') for i in argc])

def script(p): # функция, вызываемая по команде script
	if p: # Если список аргументов не пустой
		p[0] = p[0].strip('"') # Парсим
		if "C:\\" not in p[0]: # если путь не полный
			p[0] = path.dirname(__file__) + "\\" + p[0]
	if path.exists(p[0]): # Если файл скрипта существует, запускаем его
		init_script(p[0])
		return ""
	else:
		return "script: invalid path"

def init_command(com, argc):
	if com in commands:  # если команда имеется в словаре commands, запускаем соответствующую функцию
		# если в списке argc имеются аргументы данные без кавычек -> выводим ошибку
		if [i for i in argc if i[0] != '"' or i[-1] != '"']:
			return [com + ": invalid arguments", False]
		return [commands[com](argc), True]
	else:
		return [com + ": no such command", False]  # иначе выводим ошибку

def init_script(p): #Запуск скрипта
	out = ""
	with open(p) as f: # Открываем скрипт
		for i in f: # Считываение команд
			com, *argc = i.split()
			buf = init_command(com, argc)
			if not buf[1]: # Если команда вернула ошибку, завершаем скрипт
				print("The script terminated with an error\n")
				return
			out += buf[0] + "\n"
	print(out)



commands = {  # словарь команд и соответсвующих функций функций
	"cd": cd,
	"ls": ls,
	"script": script,
	"exit": exit
}
def main(): # Основная функция
	startup()
	print("Startup script:\n")
	init_script(argv[2])
	while True:
		print(dir + " >", end=" ")  # вывод приглашения к вводу
		com, *argc = input().split()  # ввод команды и аргрументов
		print(init_command(com, argc)[0])


main()