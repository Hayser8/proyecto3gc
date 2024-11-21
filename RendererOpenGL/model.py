from obj import Obj
from buffer import Buffer
from pygame import image
import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

class Model(object):
    def __init__(self, filename):
        objFile = Obj(filename)
        self.vertices = objFile.vertices
        self.texCoords = objFile.texcoords
        self.normals = objFile.normals
        self.faces = objFile.faces
        self.texture = None
        self.time = 0
        self.buffer = Buffer(self.BuildBuffer())
        self.translation = glm.vec3(0, 0, 0)
        self.rotation = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(1, 1, 1)
        self.shader_program = None  
        self.vertex_shader = None
        self.fragment_shader = None

    def SetShaders(self, vertex_shader_code, fragment_shader_code):
        self.vertex_shader = vertex_shader_code
        self.fragment_shader = fragment_shader_code
        self.shader_program = compileProgram(
            compileShader(self.vertex_shader, GL_VERTEX_SHADER),
            compileShader(self.fragment_shader, GL_FRAGMENT_SHADER)
        )

    def Update(self, delta_time):
        self.time += delta_time

    def GetModelMatrix(self):
        identity = glm.mat4(1)
        translateMat = glm.translate(identity, self.translation)
        pitchMat = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        yawMat = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        rollMat = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))

        rotationMat = pitchMat * yawMat * rollMat
        scaleMat = glm.scale(identity, self.scale)

        return translateMat * rotationMat * scaleMat

    def BuildBuffer(self):
        data = []

        for face in self.faces:
            faceVerts = []

            for i in range(len(face)):
                vert = []

                position = self.vertices[face[i][0] - 1]

                for value in position:
                    vert.append(value)

                if len(face[i]) > 1 and face[i][1] > 0:
                    vts = self.texCoords[face[i][1] - 1]
                else:
                    vts = [0.0, 0.0]

                for value in vts:
                    vert.append(value)

                if len(face[i]) > 2 and face[i][2] > 0:
                    normals = self.normals[face[i][2] - 1]
                else:
                    normals = [0.0, 0.0, 0.0]

                for value in normals:
                    vert.append(value)

                faceVerts.append(vert)

            for value in faceVerts[0]:
                data.append(value)
            for value in faceVerts[1]:
                data.append(value)
            for value in faceVerts[2]:
                data.append(value)

            if len(faceVerts) == 4:
                for value in faceVerts[0]:
                    data.append(value)
                for value in faceVerts[2]:
                    data.append(value)
                for value in faceVerts[3]:
                    data.append(value)

        return data

    def AddTexture(self, textureFilename):
        self.textureSurface = image.load(textureFilename)
        self.textureData = image.tostring(self.textureSurface, "RGB", True)
        self.texture = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D,
                     0,
                     GL_RGB,
                     self.textureSurface.get_width(),
                     self.textureSurface.get_height(),
                     0,
                     GL_RGB,
                     GL_UNSIGNED_BYTE,
                     self.textureData)
        glGenerateMipmap(GL_TEXTURE_2D)

        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def Render(self, renderer):
        if self.shader_program:
            glUseProgram(self.shader_program)
           
            glUniform1f(glGetUniformLocation(self.shader_program, "time"), self.time)
            glUniformMatrix4fv(glGetUniformLocation(self.shader_program, "modelMatrix"), 1, GL_FALSE, glm.value_ptr(self.GetModelMatrix()))
            glUniformMatrix4fv(glGetUniformLocation(self.shader_program, "viewMatrix"), 1, GL_FALSE, glm.value_ptr(renderer.camera.GetViewMatrix()))
            glUniformMatrix4fv(glGetUniformLocation(self.shader_program, "projectionMatrix"), 1, GL_FALSE, glm.value_ptr(renderer.camera.GetProjectionMatrix()))
            
            
            if glGetUniformLocation(self.shader_program, "lightPosition") != -1:
                glUniform3fv(glGetUniformLocation(self.shader_program, "lightPosition"), 1, glm.value_ptr(renderer.pointLight))
            if glGetUniformLocation(self.shader_program, "cameraPosition") != -1:
                glUniform3fv(glGetUniformLocation(self.shader_program, "cameraPosition"), 1, glm.value_ptr(renderer.camera.position))
            
           
            if glGetUniformLocation(self.shader_program, "time") != -1:
                glUniform1f(glGetUniformLocation(self.shader_program, "time"), self.time)
        else:
            glUseProgram(renderer.active_shaders)
            glUniformMatrix4fv(glGetUniformLocation(renderer.active_shaders, "modelMatrix"), 1, GL_FALSE, glm.value_ptr(self.GetModelMatrix()))

        # Enlazar textura
        if self.texture is not None:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            tex_location = glGetUniformLocation(self.shader_program if self.shader_program else renderer.active_shaders, "tex")
            if tex_location != -1:
                glUniform1i(tex_location, 0)

       
        self.buffer.Render()

