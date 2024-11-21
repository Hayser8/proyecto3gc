import re


class Obj(object):
	def __init__(self, filename):
		# Asumiendo que el archivo es un formato .obj
		with open(filename, "r") as file:
			lines = file.read().splitlines()
			
		self.vertices = []
		self.texcoords = []
		self.normals = []
		self.faces = []
		
		for line in lines:
			# Si la linea no cuenta con un prefijo y un valor,
			# seguimos a la siguiente la linea

			# Este comando elimina espacios en blanco innecesarios
			# al final de un texto
			line = line.rstrip()

			try:
				prefix, value = line.split(" ", 1)
			except:
				continue
			
			# Dependiendo del prefijo, parseamos y guardamos
			# la informacion en el contenedor correcto
			
			if prefix == "v": # Vertices
				vertice = list(map(float, filter(None, value.split(' '))))
				self.vertices.append(vertice)
				
			elif prefix == "vt": # Coordenadas de textura
				vts = list(map(float, filter(None, value.split(' ')) ))
				self.texcoords.append([vts[0],vts[1]])
				
			elif prefix == "vn": # Normales
				norm = list(map(float, filter(None, value.split(' ')) ))
				self.normals.append(norm)
				
			elif prefix == "f": # Caras
				self.faces.append([list(map(int, filter(None, re.split(r'/|//', face)))) for face in value.split(' ')])
				# face = []
				# verts = value.split(" ")
				# for vert in verts:
				# 	vert = list(map(int, vert.split("/")))
				# 	face.append(vert)
				# self.faces.append(face)