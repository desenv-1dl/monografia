# -*- coding: utf-8 -*-
#imports system
import os
from shutil import copyfile



class Projeto:
    def __init__(self): 
        self.project = None
 	self.newImage = None   
       
    def criarProjeto(self, newProjectPath):
        os.mkdir(newProjectPath)
        os.mkdir(os.path.join(newProjectPath, 'html'))
        self.createFilesConf(newProjectPath)
        os.mkdir(os.path.join(newProjectPath, 'pdf'))
        os.mkdir(os.path.join(newProjectPath, 'fotos'))       
        self.setProjectCurrent(newProjectPath)
    
    def createFilesConf(self, newProjectPath):
        copyfile(os.path.join(os.path.dirname(__file__), 'templates', '1.png'), os.path.join(newProjectPath, 'html', '.1.jpg'))
        copyfile(os.path.join(os.path.dirname(__file__), 'templates', 'dl.png'), os.path.join(newProjectPath, 'html', '.dl.png'))
        copyfile(os.path.join(os.path.dirname(__file__), 'templates', 'bootstrap.css'), os.path.join(newProjectPath, 'html', '.bootstrap.css'))
        copyfile(os.path.join(os.path.dirname(__file__), 'templates', 'ass.jpg'), os.path.join(newProjectPath, 'html', '.ass.jpg'))
        copyfile(os.path.join(os.path.dirname(__file__), 'templates', 'assEx.jpg'), os.path.join(newProjectPath, 'html', '.assEx.jpg'))
                       
    def abrirProjeto(self, openProjectPath):
        self.setProjectCurrent(openProjectPath)     
    
    def setProjectCurrent(self, project):
        self.project = project

    def getProjectCurrent(self):
        return self.project

    def setPathNewImage(self, p):
	self.newImage = p

    def getPathNewImage(self):
	return self.newImage
    
    def testProject(self, projectPath):
        test1 = os.path.exists(os.path.join(projectPath, 'html'))
        test2 = os.path.exists(os.path.join(projectPath, 'fotos'))
        test3 = os.path.exists(os.path.join(projectPath, 'pdf'))
        if test1 and test2 and test3:
            return True
        else:
            return False 
   
