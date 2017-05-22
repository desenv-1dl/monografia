# -*- coding: utf-8 -*-

#imports system
import os
import sys

#imports PyQt4
from PyQt4.QtGui import QMessageBox, QFileDialog
from PyQt4.QtCore import pyqtSlot
from PyQt4 import QtGui, uic, QtCore
from shutil import copyfile


#imports functions of class Monografia
from monografia import Monografia
#import resources_rc

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'interfaceMonografia.ui'))

class GerarMonografia(QtGui.QDialog, FORM_CLASS): 
    def __init__(self, parent = None):         
        super(GerarMonografia, self).__init__(parent)
        self.setupUi(self)
        self.progressBar.setRange(0,1)
        self.pdfHtmlButton.setEnabled(False)
        self.csvButton.setEnabled(False)
        self.showCurrentProject()
        self.monografia = Monografia()
        
        
    @pyqtSlot(bool)
    def on_loadImageButton_clicked(self):
	if self.monografia.getProjectCurrent():
		path = unicode(QFileDialog.getOpenFileName(self, 'Selecionar Imagem', '',"Imagem png (*.png)")).encode('utf-8')
		os.remove(os.path.join(self.monografia.getProjectCurrent(), 'html', '.dl.png'))
		copyfile( path, os.path.join(self.monografia.getProjectCurrent(), 'html', '.dl.png'))
	else:
		self.messageErro(u'Aviso:', u'Não há projetos em uso !', u'Crie um projeto ou abra um e tente novamente.')
	    
    @pyqtSlot(bool)
    def on_createCsvButton_clicked(self):
        path = unicode(QFileDialog.getSaveFileName(self, 'Salvar arquivo CSV', '')).encode('utf-8')
        copyfile(os.path.join(os.path.dirname(__file__), 'templates', 'templateCsv.csv'), os.path.join(path+'.csv'))
        
    @pyqtSlot(bool)
    def on_newProjectButton_clicked(self):
        projectPath = unicode(QFileDialog.getSaveFileName(self, 'Criar projeto', '')).encode('utf-8')
        if (projectPath != '') and (projectPath != None):
            self.csvButton.setEnabled(True)
            self.monografia.criarProjeto(projectPath)
            nameProject = projectPath.split('/')[-1]
            self.showCurrentProject(nameProject, True)
           
    @pyqtSlot(bool)
    def on_openProjectButton_clicked(self):
        projectPath = unicode(QFileDialog.getExistingDirectory(self, 'Abrir projeto', '')).encode('utf-8')
        if (projectPath != '') and (projectPath != None):
            ok = self.monografia.testProject(projectPath)
            if (ok) :         
                self.csvButton.setEnabled(True)
                self.monografia.abrirProjeto(projectPath)
                nameProject = projectPath.split('/')[-1]
                self.showCurrentProject(nameProject, True)                
            else:
                self.messageErro(u'Erro no projeto:', u'O projeto está corrompido!', u'Crie um projeto e tente novamente.')
        
    @pyqtSlot(bool)
    def on_csvButton_clicked(self):
        csvPath = unicode(QFileDialog.getOpenFileName(self, 'Selecionar CSV', '',"Arquivo csv (*.csv)")).encode('utf-8')
        if csvPath != '':
            self.monografia.carregarCsv(csvPath)
            if len(self.monografia.csvList) > 0:
                
                self.pdfHtmlButton.setEnabled(True)
            else:
                self.messageErro(u'Erro em arquivo csv:', u'Arquivo csv sem dados para processamento!', u'Insira dados no csv e tente abrir novamente.' )
                
    @pyqtSlot(bool)
    def on_pdfHtmlButton_clicked(self):
        self.progressBar.setRange(0,0)
        thread = QtCore.QThread(self)
        worker = self.monografia
        worker.moveToThread(thread)
        worker.finished.connect(self.taskFinished)
        thread.started.connect(worker.createHtmlPdf)
        thread.start()
        self.thread = thread
        self.worker = worker
        
    
    def taskFinished(self, tipo):
#         self.worker.deleteLater()
#         self.thread.quit()
#         self.thread.wait()
#         self.thread.deleteLater()
#         self.thread = None
#         self.worker = None
        self.progressBar.setRange(0,1)
        self.progressBar.setValue(0)
        self.pdfHtmlButton.setEnabled(False)
        
    def messageErro(self, tipo, text, details):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)        
        msg.setText(tipo)
        msg.setInformativeText(text)
        msg.setWindowTitle("Erro")
        msg.setDetailedText(details)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()
           
    def showCurrentProject(self, name=None, active=False):
        if active:
            self.textLabel.setVisible(True)
            self.projectLabel.setVisible(True)
            self.projectLabel.setText(str(name))
        else:
            self.textLabel.setVisible(False)
            self.projectLabel.setVisible(False) 
           
        
if __name__ == '__main__':
    a = QtGui.QApplication(sys.argv) 
    app = GerarMonografia()
    app.show() 
    sys.exit(a.exec_())
