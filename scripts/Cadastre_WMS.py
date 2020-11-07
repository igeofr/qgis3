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
import unicodedata
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterField,
                       QgsRasterLayer,
                       QgsProcessingContext, 
                       QgsProcessingFeedback, 
                       QgsProject,
                       QgsProcessingOutputMultipleLayers)
from qgis import processing


class ExampleProcessingAlgorithm(QgsProcessingAlgorithm):
    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    INPUT = 'INPUT'
    INSEE_CODE = 'INSEE_CODE'
    COMMUNE_NAME = 'COMMUNE_NAME'
    EPSG_CODE = 'EPSG_CODE'
    OUTPUT_LAYERS = 'OUTPUT_LAYERS'

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
        return 'Cadastre FR - WMS'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Cadastre FR - WMS')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Cadastre FR')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'cadastre'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("EN : This script adds the WMS cadastral maps of communes from a vector file of communes. \nURL  : http://inspire.cadastre.gouv.fr/scpc/[INSEE_code].wms? \nVariable : [INSEE_code] \nMore information at this address : https://www.cadastre.gouv.fr/scpc/pdf/Guide_WMS_fr.pdf \n==================\nFR : Le script permet d'ajouter le cadastre WMS de plusieurs communes à partir d'un fichier vectoriel de communes. \nURL : http://inspire.cadastre.gouv.fr/scpc/[INSEE_code].wms? \nVariable : [INSEE_code] \nPlus d'informations à cette adresse : https://www.cadastre.gouv.fr/scpc/pdf/Guide_WMS_fr.pdf")

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
            QgsProcessingParameterField(
                self.INSEE_CODE,
                'Code INSEE',
                '',
                self.INPUT
                )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.COMMUNE_NAME,
                'Nom',
                '',
                self.INPUT
                )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                name=self.EPSG_CODE,
                description=self.tr('Code EPSG'),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=2154
            )
        )
        self.addOutput(
            QgsProcessingOutputMultipleLayers(
                self.OUTPUT_LAYERS,
                self.tr('Output layers')
            )
        )

    def processAlgorithm(self, parameters, context,  feedback):
        """
        Here is where the processing itself takes place.
        """

        source = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        field_insee = self.parameterAsString(parameters,  self.INSEE_CODE, context)
        field_commune = self.parameterAsString(parameters,  self.COMMUNE_NAME, context)
        value_epsg = self.parameterAsString(parameters, self.EPSG_CODE, context)

        if value_epsg == '2154' or value_epsg == '3942' or value_epsg == '3943' or value_epsg == '3944' or value_epsg == '3945' or value_epsg == '3946' or value_epsg == '3947' or value_epsg == '3948' or value_epsg == '3949' or value_epsg == '3950' or value_epsg == '32630' or value_epsg == ' 32631' or value_epsg == '32632' or value_epsg == '3857' or value_epsg == '4326' or value_epsg == '4258' or value_epsg == '32620' or value_epsg == '2970' or value_epsg == '2972' or value_epsg == '2973' or value_epsg == '2975' or value_epsg == '32622' or value_epsg == '32740' or value_epsg == '32738' or value_epsg == '4471' or value_epsg == '32621' :
            
            feedback.pushInfo('EPSG code' + value_epsg)
            tab = []

            for f in source.getFeatures():

                col_select=f[field_insee],(''.join((c for c in unicodedata.normalize('NFD', f[field_commune]) if unicodedata.category(c) != 'Mn')))
                            
                # Insere chaque ligne du CSV dans le tableau
                tab.append(col_select)

                #Permet la suppression des doublons et le tri
                Lt=sorted(set(tab))
                
                print (Lt)
                
            for c_insee, n_couche in Lt  :

                urlWithParams ="url=http://inspire.cadastre.gouv.fr/scpc/"+c_insee+".wms?contextualWMSLegend=0&crs=EPSG:"+value_epsg+"&dpiMode=7&featureCount=10&format=image/png&layers=AMORCES_CAD&layers=LIEUDIT&layers=CP.CadastralParcel&layers=SUBFISCAL&layers=CLOTURE&layers=DETAIL_TOPO&layers=HYDRO&layers=VOIE_COMMUNICATION&layers=BU.Building&layers=BORNE_REPERE&styles=&styles=&styles=&styles=&styles=&styles=&styles=&styles=&styles=&styles=&maxHeight=1024&maxWidth=1280"
                rlayer = QgsRasterLayer(urlWithParams,'Cadastre_'+n_couche+'_'+c_insee, 'wms')
                feedback.pushInfo('Category :'+ n_couche +' - '+c_insee)
                feedback.pushInfo('Validity of WMS : %s' % rlayer.isValid())
                if not rlayer.isValid():
                    print('Cadastre_'+n_couche+'_'+c_insee + ' failed to load!')
                    feedback.pushInfo('WMS INVALID : Cadastre_'+n_couche+'_'+c_insee)
                else:
                    #Source : https://gis.stackexchange.com/questions/342802/loading-openstreetmap-in-pyqgis
                    output_layers = []
                    output_layers.append(rlayer)
                    context.temporaryLayerStore().addMapLayer(rlayer)
                    context.addLayerToLoadOnCompletion(
                        rlayer.id(),
                        QgsProcessingContext.LayerDetails(
                            'Cadastre_'+n_couche+'_'+c_insee,
                            context.project(),
                            self.OUTPUT_LAYERS
                        )
                    )
        else :
            feedback.pushInfo('Error EPSG code')
                
                
        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        # At the end of the processAlgorithmn
        # Add the layer to the project
        return {}