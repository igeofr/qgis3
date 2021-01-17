# -*- coding: utf-8 -*-
# =============================================================================
# Created By : Florian Boret
# Created Date : Septembre 2020
# Date last modified :
# =============================================================================

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""
import csv
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import (QgsProcessing,
                       QgsFeature,
                       QgsVectorLayer,
                       QgsGeometry,
                       QgsField,
                       QgsFields,
                       QgsWkbTypes,
                       QgsSymbol,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterFileDestination,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterField,
                       QgsProcessingParameterString,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFile,
                       QgsRendererCategory,
                       QgsCategorizedSymbolRenderer
                       )
from qgis import processing

class ExampleProcessingAlgorithm(QgsProcessingAlgorithm):
    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    VECTOR_LAYER = 'VECTOR_LAYER'
    VALUE_FIELD = 'VALUE_FIELD'
    FICHIER_CSV = 'FICHIER_CSV'
    C_VALUE = 'C_VALUE'
    C_LABEL = 'C_LABEL'
    C_RGB = 'C_RGB'
    TRANSP = 'TRANSP'
    OUTLINE = 'OUTLINE'
    OUTLINE_W = 'OUTLINE_W'
    S_QML = 'S_QML'


    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ExampleProcessingAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'CSV RGB to categorized style'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('CSV RGB to categorized style')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Style')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'style'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("EN : The script generates a categorized style from a CSV file including color information (RGB).\nMore informations : https://blog.data-wax.com/2015/03/08/generer-un-style-categorise-sur-qgis-a-partir-dun-fichier-csv/\nFR : Le script permet de générer un style catégorisé à partir d'un fichier CSV dans lequel on trouve des informations de couleur (RGB).\nPlus d'informations : https://blog.data-wax.com/2015/03/08/generer-un-style-categorise-sur-qgis-a-partir-dun-fichier-csv/")


    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.VECTOR_LAYER,
                self.tr('Fichier vectoriel'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.VALUE_FIELD,
                'Champ',
                '',
                self.VECTOR_LAYER
                )
            )
        self.addParameter(
            QgsProcessingParameterFile(
                self.FICHIER_CSV,
                self.tr('csv File'),
                0,
                'csv'
                )
            )
        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.C_VALUE,
                description=self.tr('Column value'),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=0
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.C_LABEL,
                description=self.tr('Column label'),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=1
                )
            )
        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.C_RGB,
                description=self.tr('Column RGB'),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=2
                )
            )
        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.TRANSP,
                description=self.tr('Transparency'),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=50,
                optional=False,
                minValue=0,
                maxValue=100
                )
            )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.OUTLINE,
                self.tr('Outline'),
                defaultValue=False
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.OUTLINE_W,
                description=self.tr('Outline width'),
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0.26
                )
            )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.S_QML,
                self.tr('Save layer style as default '),
                defaultValue=False
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layer = self.parameterAsVectorLayer(parameters, self.VECTOR_LAYER, context)
        value_field = self.parameterAsString(parameters,  self.VALUE_FIELD, context)
        csv_file = self.parameterAsFile(parameters, self.FICHIER_CSV, context)
        v_value = self.parameterAsString(parameters, self.C_VALUE, context)
        v_label = self.parameterAsString(parameters, self.C_LABEL, context)
        v_RGB = self.parameterAsString(parameters, self.C_RGB, context)
        v_transp = self.parameterAsString(parameters, self.TRANSP, context)
        v_outline = self.parameterAsBool(parameters, self.OUTLINE, context)
        v_outline_w = self.parameterAsString(parameters, self.OUTLINE_W, context)
        v_qml = self.parameterAsBool(parameters, self.S_QML, context)

        #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        reader = csv.reader(open(csv_file), delimiter=";")
        #next(reader)
        for row in reader:
            tab = []
            for row in reader:
                stringcount = len(row[int(v_RGB)].split(','))

                #Vérifie si l'Alpha est renseigné
                if stringcount== 3 :
                    #Permet d'exploser les valeurs
                    c_red, c_green, c_blue = row[int(v_RGB)].split(',')
                else :
                    c_red, c_green, c_blue, c_alpha = row[int(v_RGB)].split(',')

                # Permet de definir les colonnes value, label, r, g, b
                col_select =row[int(v_value)], row[int(v_label)], c_red, c_green, c_blue
                # Insere chaque ligne du CSV dans le tableau
                tab.append(col_select)

                #Permet la suppression des doublons et le tri
                Lt=sorted(set(tab))

            #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                categories = []
                for value, label, color_red, color_green, color_blue in Lt :
                    tab_list = value +' - '+ label +' - ' +color_red +' - '+ color_green +' - '+ color_blue
                    feedback.pushInfo('Category :'+ tab_list)

                    #Polygon
                    if layer.geometryType() == QgsWkbTypes.PolygonGeometry:
                        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
                        # Set colour
                        symbol.setColor(QColor(int(color_red),int(color_green),int(color_blue)))
                        # Set opacity
                        symbol.setOpacity(int(v_transp)/100)
                        # Set Stroke
                        if v_outline == False :
                            symbol.symbolLayer(0).setStrokeStyle(Qt.PenStyle(Qt.NoPen))
                        symbol.symbolLayer(0).setStrokeColor(QColor(int(0),int(0),int(0)))
                        symbol.symbolLayer(0).setStrokeWidth(float(v_outline_w))

                        category = QgsRendererCategory(value, symbol, label)
                        categories.append(category)

                    #Line
                    if layer.geometryType() == QgsWkbTypes.LineGeometry:
                        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
                        # Set colour
                        symbol.setColor(QColor(int(color_red),int(color_green),int(color_blue)))
                        # Set opacity
                        symbol.setOpacity(int(v_transp)/100)
                        symbol.setWidth (Outline_width)

                        category = QgsRendererCategory(value, symbol, label)
                        categories.append(category)

                    #Point
                    if layer.geometryType() == QgsWkbTypes.PointGeometry:
                        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
                        # Set colour
                        symbol.setColor(QColor(int(color_red),int(color_green),int(color_blue)))
                        # Set opacity
                        symbol.setOpacity(int(v_transp)/100)
                        # Set Stroke
                        if v_outline == False :
                            symbol.symbolLayer(0).setStrokeStyle(Qt.PenStyle(Qt.NoPen))
                        symbol.symbolLayer(0).setStrokeColor(QColor(int(0),int(0),int(0)))
                        symbol.symbolLayer(0).setStrokeWidth(float(v_outline_w))

                        category = QgsRendererCategory(value, symbol, label)
                        categories.append(category)

            #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                expression = value_field
                # Set the categorized renderer
                renderer = QgsCategorizedSymbolRenderer(expression, categories)
                layer.setRenderer(renderer)
                # Refresh layer
                layer.triggerRepaint()

                # Creation des fichiers de style
                if v_qml :
                    # QML
                    layer.saveDefaultStyle()


        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return {}
