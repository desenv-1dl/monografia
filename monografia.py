# -*- coding: utf-8 -*-

#imports system
import os, sys
import csv
from project import Projeto
#imports library
from PyQt4 import QtCore, QtGui
import pdfkit, shutil
import time
import re
from distutils.dir_util import copy_tree

       
class Monografia(QtCore.QObject, Projeto):
    finished = QtCore.pyqtSignal(int)
    def __init__(self):
        reload(sys)  
        sys.setdefaultencoding('utf8')
        self.csvList = []
        QtCore.QObject.__init__(self)
	Projeto.__init__(self)
	        
    def carregarCsv(self, csvPath):
        with open(csvPath, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for line in reader:
                self.csvList.append(line)
        csvfile.close
            
    def createHtmlPdf(self):
        opt = {
            'page-size': 'A4',
            'margin-top': '0.5cm',
            'margin-right': '0.5cm',
            'margin-bottom': '6.0cm',
            'margin-left': '1.5cm',
            'encoding': "UTF-8",
            'no-outline': None
        } 
        with open (os.path.join(os.path.dirname(__file__), 'templates', 'monografia.html'), 'r') as template:
            htmlTemplate = template.read()  
        paths = []          
        for line in self.csvList:
            data, pontoId = self.setVariables(line)
            html = self.setHtml(data, htmlTemplate) 
            pathHtml = self.createtHtml(html, pontoId)
            self.convertHtmlPdf(pathHtml, pontoId)
        self.finished.emit(1)
                   
    def createtHtml(self, html, pontoId):
        pathHtml = os.path.join(str(self.project), 'html', str(pontoId)+'.html')
        arquivo = open(pathHtml, 'w')
        arquivo.write(html)
        arquivo.close()
        return pathHtml
         
               
    def convertHtmlPdf(self, pathHtml, pontoId):
        opt = {
            'page-size': 'A4',
            'margin-top': '0.5cm',
            'margin-right': '0.0cm',
            'margin-bottom': '5.3cm',
            'margin-left': '2cm',
            'encoding': "UTF-8",
            'no-outline': None
        } 
        try:
            pathPdf = os.path.join(self.project, 'pdf', str(pontoId)+'.pdf')
            pdfkit.from_file(pathHtml, pathPdf, options=opt)
        except:
            pass
           
    def setHtml(self, data, htmlTemplate):
        html = htmlTemplate
        for variable in data:
            html = html.replace(variable, data[variable])
        return html
                       
    def setVariables(self, line):
        pontoId = line['nome-ponto-(ID)']
        data = dict()
        for key in line:
            data['{{'+key+'}}'] = line[key]
        self.setPhotos(data ,pontoId)
        return data, pontoId        
            
    def setPhotos(self, data, pontoId):
        fotos = os.listdir(os.path.join(str(self.project),'fotos'))
        if len(fotos) != 0:
            number = 1
            for foto in fotos:
                if pontoId == foto[:len(pontoId)]:
                    if re.search('[0-9]$', foto[:-4]):
                        data['{{foto'+str(number)+'}}'] = os.path.join(str(self.project),'fotos', foto)
                        number+=1
                    elif re.search('aerea', foto[:-4]):
                        data['{{path-vista-aerea}}'] = os.path.join(str(self.project),'fotos', foto)                    
                    elif re.search('croqui', foto[:-4]):
                        data['{{path-croqui}}'] = os.path.join(str(self.project),'fotos', foto)
                
            
                    
  
           
    
