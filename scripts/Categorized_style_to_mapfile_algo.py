# -*- coding: utf-8 -*-

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
#import csv
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterFileDestination,
                       QgsProcessingParameterBoolean)
from qgis import processing


class ExampleProcessingAlgorithm(QgsProcessingAlgorithm):
    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    INPUT = 'INPUT'
    BOOLEAN1 = 'BOOLEAN1'
    OUTPUT = 'OUTPUT'

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
        return 'Categorized style to Mapfile'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Categorized style to Mapfile')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Mapfile')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'categorizedstyletomapfile'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Permet d'exporter un style QGIS catégorisé en Mapfile")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Fichier vectoriel'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.BOOLEAN1,
                self.tr('Interrogation WMS'),
                defaultValue=False
            )
        )
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                self.tr('Output layer'),
                'TXT files (*.txt)'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        source = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        txt_file = self.parameterAsFileOutput(parameters, self.OUTPUT, context)
        boolean_value = self.parameterAsBool(parameters, self.BOOLEAN1, context)

        renderer  = source.renderer()

        # Open a file with access mode 'w'
        file_object = open(txt_file, 'w')


        if renderer.type() == 'categorizedSymbol': #Style categorise
            categories = renderer.categories()

            for category in categories: # Recuperation des infos et ecriture dans le txt
                line1 = 'CLASS'
                line2 = '   NAME "'+(category.label())+'"'
                if boolean_value==True :
                    line3 = '       TEMPLATE "../template/getfeatureinfo/{LAYER_NAME}.html"'
                else :
                    line3 =''
                line4 = '       EXPRESSION ("[niv3]" eq "'+category.value()+'"'
                line5 = '       STYLE'
                line6 = '           COLOR '+str(category.symbol().color().red())+' '+str(category.symbol().color().green())+' '+str(category.symbol().color().blue())
                line7 = '           OUTLINECOLOR '+str(category.symbol().symbolLayer(0).strokeColor().red())+' '+str(category.symbol().symbolLayer(0).strokeColor().green())+' '+str(category.symbol().symbolLayer(0).strokeColor().blue())
                line8 = '           WIDTH '+str(category.symbol().symbolLayer(0).strokeWidth())
                line9 = '       END'
                line10 = '  END'
                # Append 'hello' at the end of file
                file_object.write('{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n'.format(line1,line2,line3,line4,line5,line6,line7,line8,line9,line10))
                # Close the file
        file_object.close()
        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return {self.OUTPUT: txt_file}
