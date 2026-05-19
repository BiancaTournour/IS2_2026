import os
#*--------------------------------------------------------------------
#* Design pattern memento, ejemplo
#*-------------------------------------------------------------------
class Memento:
	def __init__(self, file, content):
		
		self.file = file
		self.content = content


class FileWriterUtility:

	def __init__(self, file):

		self.file = file
		self.content = ""

	def write(self, string):
		self.content += string


	def save(self):
		return Memento(self.file, self.content)

	def undo(self, memento):
		self.file = memento.file
		self.content = memento.content


class FileWriterCaretaker:

	def __init__(self):

		# Lista para guardar hasta 4 estados
		self.history = []

	def save(self, writer):

		# Guarda nuevo estado
		self.history.append(writer.save()
					  )

		# Mantener solo los últimos 4 estados
		if len(self.history) > 4:
			self.history.pop(0)

	def undo(self, writer, version):

		"""
		version = 0 -> último estado
		version = 1 -> anterior
		version = 2 -> anterior al anterior
		version = 3 -> el más viejo guardado
		"""

		if version < len(self.history):

			index = -(version + 1)
			memento = self.history[index]

			writer.undo(memento)

		else:
			print("No existe esa versión guardada")

if __name__ == '__main__':

	os.system("cls")

	print("Crea un objeto caretaker")
	caretaker = FileWriterCaretaker()

	print("Crea el objeto writer")
	writer = FileWriterUtility("IS2.txt")


	print("\nEstado 1")
	writer.write("Clase de IS2 en UADER\n")
	print(writer.content)
	caretaker.save(writer)


	print("\nEstado 2")
	writer.write("Material adicional de patrones\n")
	print(writer.content)
	caretaker.save(writer)


	print("\nEstado 3")
	writer.write("Material adicional II\n")
	print(writer.content)
	caretaker.save(writer)


	print("\nEstado 4")
	writer.write("Material adicional III\n")
	print(writer.content)
	caretaker.save(writer)


	print("\nEstado 5")
	writer.write("Material adicional IV\n")
	print(writer.content)
	caretaker.save(writer)


	print("\nUNDO versión 0 (último estado)")
	caretaker.undo(writer, 0)
	print(writer.content)


	print("\nUNDO versión 1")
	caretaker.undo(writer, 1)
	print(writer.content)


	print("\nUNDO versión 2")
	caretaker.undo(writer, 2)
	print(writer.content)


	print("\nUNDO versión 3")
	caretaker.undo(writer, 3)
	print(writer.content)
