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
        # os._exit(1)
        return

    tp = layer.getTypeVectorLayer().name
    # print tp
    
    selection = layer.getSelection()
    # print selection.getCount()
    ## обработка события нет выбранных объектов
    for f in selection:
        ## обработка сохранения файла с помощью saveFileDialog()
        # fname = 'D:\\' + f.Name_short + '.csv'
        filePath = saveFileDialog('Save CSV file',)
       
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

