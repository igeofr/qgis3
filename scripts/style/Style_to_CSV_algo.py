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
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterVectorLayer,
                       #QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFileDestination,
                       QgsFeatureRenderer)
from qgis import processing


class ExampleProcessingAlgorithm(QgsProcessingAlgorithm):
    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    INPUT = 'INPUT'
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
        return 'Style to Csv'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Style to CSV')

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
        return self.tr("Permet d'exporter les couleurs d'un style QGIS")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Fichier vectoriel'),
                [QgsProcessing.TypeVectorAnyGeometry],
            )
        )

        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                self.tr('Output layer'),
                'CSV files (*.csv)',
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        source = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        csv_file = self.parameterAsFileOutput(parameters, self.OUTPUT, context)


        renderer  = source.renderer()

        feedback.pushInfo("Début de l'export")

        with open(csv_file, 'w', newline='', encoding='utf-8') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL,delimiter=';')
            wr.writerow(['Value','Label','Hexa','RGBA','R','G','B','A'])

            if renderer.type() == 'categorizedSymbol': #Style categorise
                feedback.pushInfo("Style categorise")
                categories = renderer.categories()

                for category in categories: # Recuperation des infos et ecriture dans le csv
                    list =[]
                    list.append(category.value()) # Valeur
                    list.append(category.label()) # Label
                    list.append(category.symbol().color().name()) # Couleur hexadecimale
                    list.append(str(category.symbol().color().red())+','+str(category.symbol().color().green())+','+str(category.symbol().color().blue()) +','+str(category.symbol().color().alpha())) # Couleur rgba
                    list.append(str(category.symbol().color().red())) # Couleur red
                    list.append(str(category.symbol().color().green())) # Couleur green
                    list.append(str(category.symbol().color().blue())) # Couleur blue
                    list.append(str(category.symbol().color().alpha())) # Alpha
                    #print (list)
                    wr.writerow(list)
            #==============================================================================
            elif renderer.type() == 'singleSymbol': #Style unique
                feedback.pushInfo("Style unique")
                list =[]
                list.append('singleSymbol') # Valeur
                list.append('singleSymbol') # Label
                list.append(str(renderer.symbol().color().name())) # Couleur hexadecimale
                list.append(str(renderer.symbol().color().red())+','+str(renderer.symbol().color().green())+','+str(renderer.symbol().color().blue()) +','+str(renderer.symbol().color().alpha())) # Couleur rgba
                list.append(str(renderer.symbol().color().red())) # Couleur red
                list.append(str(renderer.symbol().color().green())) # Couleur green
                list.append(str(renderer.symbol().color().blue())) # Couleur blue
                list.append(str(renderer.symbol().color().alpha())) # Alpha
                wr.writerow(list) # On ecrit le tout

            #==============================================================================
            elif renderer.type() == 'graduatedSymbol': #Style gradue
                feedback.pushInfo("Style gradue")
                ranges = renderer.ranges()

                for rng in ranges: # Recuperation des infos et ecriture dans le csv
                    list =[]
                    list.append(str(rng.lowerValue())+"-"+str(rng.upperValue())) # Valeur
                    list.append(rng.label()) # Label
                    list.append(str(rng.symbol().color().name())) # Couleur hexadecimale
                    list.append(str(rng.symbol().color().red())+','+str(rng.symbol().color().green())+','+str(rng.symbol().color().blue()) +','+str(rng.symbol().color().alpha())) # Couleur rgba
                    list.append(str(rng.symbol().color().red())) # Couleur red
                    list.append(str(rng.symbol().color().green())) # Couleur green
                    list.append(str(rng.symbol().color().blue())) # Couleur blue
                    list.append(str(rng.symbol().color().alpha())) #  Alpha
                    wr.writerow(list) # On ecrit le tout

            #==============================================================================
            elif renderer.type() == 'RuleRenderer': #Style par regle
                feedback.pushInfo("Style par regle")
                root_rule = renderer.rootRule().children()

                for rule in root_rule: # Recuperation des infos et ecriture dans le csv
                    list =[]
                    list.append(rule.filterExpression ()) # Valeur
                    list.append(rule.label()) # Label
                    list.append(str(rule.symbol().color().name())) # Couleur hexadecimale
                    list.append(str(rule.symbol().color().red())+','+str(rule.symbol().color().green())+','+str(rule.symbol().color().blue()) +','+str(rule.symbol().color().alpha())) # Couleur rgba
                    list.append(str(rule.symbol().color().red())) # Couleur red
                    list.append(str(rule.symbol().color().green())) # Couleur green
                    list.append(str(rule.symbol().color().blue())) # Couleur blue
                    list.append(str(rule.symbol().color().alpha())) # Alpha
                    wr.writerow(list) # On ecrit le tout

            #==============================================================================
            else : #Style non gere
                list =[]
                list.append('Style non gere') # Valeur
                list.append('Style non gere') # Label
                list.append('Style non gere') # Couleur hexadecimale
                list.append('Style non gere') # Couleur rgba
                list.append('Style non gere')# Couleur red
                list.append('Style non gere') # Couleur green
                list.append('Style non gere') # Couleur blue
                list.append('Style non gere')# Alpha
                wr.writerow(list) # On ecrit le tout

        myfile.close()
        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return {self.OUTPUT: csv_file}
