# Name:    poly2csv
# Purpose: Convert a list of X, Y coordinates for selected polygonal features to CSV file
# Author:  Serguei Mikhailov (@cadastreng)
# Created: 11.04.2014
#-----------------------------------------
import csv

from gvsig import *
from commonsdialog import *


currentViewErrorMessage = "There isn't an active View! Please, open a View and ativate a target layer."
currentLayerErrorMessage = "There isn't an active layer or activated more than one layer! Please, activate a target layer."
getSelectionErrorMessage = "There isn't a selected feature in the active layer! Please, select a feature or some features."
filePathErrorMessage = "Please, enter a name and extesion of CSV file: test.csv, for example."
errorDialogTitle = "Error"


def main():
    
    # prj = currentProject()
    # crs = prj.getProjectionCode()
    
    view = currentView()
    if view is None:
        msgbox(currentViewErrorMessage, errorDialogTitle, WARNING)
        return 

    layer = currentLayer()
    if layer is None:
        msgbox(currentLayerErrorMessage, errorDialogTitle, WARNING)
        return

    tp = layer.getTypeVectorLayer().name
    # print tp
    
    selection = layer.getSelection()
    if selection.getCount()==0:
        msgbox(getSelectionErrorMessage, errorDialogTitle, WARNING)
        return
    
    for f in selection:
        ## обработка сохранения файла с помощью saveFileDialog()
        # fname = 'D:\\' + f.Name_short + '.csv'
        filePath = saveFileDialog('Save CSV file',)
        if not filePath:
            msgbox(filePathErrorMessage, errorDialogTitle, WARNING)
            return
       
        csvFile = open(str(filePath[0]), 'wb')
        coordWriter = csv.writer(csvFile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        
        numVert = f.geometry().getNumVertices()
        # print numVert
        ## обработка отсутствия вертексов если объект выбран через таблицу но имеет нулевую геометрию
        
        gt = f.geometry().getGeometryType().name
        # print gt
        
        for v in range(0,numVert):
            point = f.geometry().getVertex(v)
            ## округлить x y до 2 значащих после запятой - чтобы дополнялись нули!!!
            coordWriter.writerow([str(v+1), str(round(point.getX(), 2)), str(round(point.getY(), 2))])
        csvFile.close()
    return

