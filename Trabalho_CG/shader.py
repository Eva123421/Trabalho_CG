from OpenGL.GL import *
import OpenGL.GL.shaders as gls


class Shader:
    def __init__(self, vertexShaderFileName, fragmentShaderFileName):
        with open(vertexShaderFileName,'r') as file:
            vsSource = file.read()
        with open(fragmentShaderFileName,'r') as file:
            fsSource = file.read()

        # criação e compilação dos vertex e fragment shader
        vsId = gls.compileShader(vsSource, GL_VERTEX_SHADER)
        fsId = gls.compileShader(fsSource, GL_FRAGMENT_SHADER)
        # linkagem dos shader em um shader program
        self.shaderId = gls.compileProgram(vsId, fsId) 

    def bind(self):
        glUseProgram(self.shaderId)
    def unbind(self):
        glUseProgram(0)    
    def setUniform(self, name, x, y=None, z=None, w=None):
        name_loc = glGetUniformLocation(self.shaderId, name)
        if y == None: glUniform1f(name_loc, x)
        elif z == None: glUniform2f(name_loc, x, y)
        elif w == None: glUniform3f(name_loc,x, y, z)
        else: glUniform4f(name_loc, x, y, z, w)
    def setMatrix(self,name, matrix):
        name_loc = glGetUniformLocation(self.shaderId, name)
        glUniformMatrix4fv(name_loc, 1, GL_FALSE, matrix)