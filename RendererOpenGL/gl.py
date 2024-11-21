import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from camera import Camera
from skybox import Skybox

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        glClearColor(0.2, 0.2, 0.2, 1)

        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

        self.camera = Camera(self.width, self.height)
        self.time = 0
        self.value = 0
        self.pointLight = glm.vec3(0, 0, 0)
        self.scene = []
        self.active_shaders = None

        self.skybox = None

    def CreateSkybox(self, textureList, vShader, fShader):
        self.skybox = Skybox(textureList, vShader, fShader)

    def FilledMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def WireframeMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def GetCurrentShaderProgram(self):
        return self.active_shaders

    def SetShaders(self, vShader, fShader):
        if vShader is not None and fShader is not None:
            self.active_shaders = compileProgram(compileShader(vShader, GL_VERTEX_SHADER),
                                                 compileShader(fShader, GL_FRAGMENT_SHADER))
        else:
            self.active_shaders = None

    def Render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if self.skybox is not None:
            self.skybox.Render(self.camera.GetViewMatrix(), self.camera.GetProjectionMatrix())

        for obj in self.scene:
            obj.Render(self)
