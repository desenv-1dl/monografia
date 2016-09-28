# -*- coding: utf-8 -*-
__author__ = "César Soares"
__date__ = "$13/08/2016 00:20:12$"

#imports system
import os
import csv
from project import Projeto
#imports library
import pdfkit, shutil
import time
import re
from distutils.dir_util import copy_tree
        
class Monografia(Projeto):
    
    def __init__(self):
        self.csvList = []
        
    def carregarCsv(self, csvPath):
        with open(csvPath, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for line in reader:
                self.csvList.append(line)
        csvfile.close
            
    def createHtmlPdf(self):
        with open (os.path.join(os.path.dirname(__file__), 'templates', 'monografia.html'), 'r') as template:
            htmlTemplate = template.read()                       
        options = {
            'page-size': 'A4',
            'margin-top': '0.5cm',
            'margin-right': '0.5cm',
            'margin-bottom': '6.0cm',
            'margin-left': '1.5cm',
            'encoding': "UTF-8",
            'no-outline': None
        }          
        for line in self.csvList:
            data, pontoId = self.setVariables(line)
            html = self.setHtml(data, htmlTemplate) 
            self.createHtml(html, pontoId)           
            self.createPdf(pontoId, options)
            
    def createHtml(self, html, pontoId):
        arquivo = open(os.path.join(str(self.project), 'html', pontoId+'.html'), 'w')
        arquivo.write(html)
        arquivo.close()
        
    def createPdf(self, pontoId, opt):
        pdfkit.from_file((os.path.join(str(self.project), 'html', pontoId+'.html')), (os.path.join(str(self.project), 'pdf', pontoId+'.pdf')),options=opt)
   
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
                    if re.search('aerea', foto[:-4]):
                        data['{{path-vista-aerea}}'] = os.path.join(str(self.project),'fotos', foto)                    
                    elif re.search('croqui', foto[:-4]):
                        data['{{path-croqui}}'] = os.path.join(str(self.project),'fotos', foto)
                
            
                    
  
           
    