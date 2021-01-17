import csv

#Variables
CSV_file="/in_semicolon.csv"

Value_field='NIV4_18'

Column_value=0
Column_label=1
Column_red=2
Column_green=3
Column_blue=4

Stroke_Color_red=0
Stroke_Color_green=0
Stroke_Color_blue=0

Outline=True
Outline_width=1
Transparency=1

Save_layer_style_as_default=False

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
layer = iface.activeLayer()

reader = csv.reader(open(CSV_file), delimiter=";")
next(reader)
for row in reader:
    #print (row[0])
    tab = []
    for row in reader:
        #print(color_rgb)
        # Permet de definir les colonnes value, label, rgb
        col_select =row[Column_value], row[Column_label],row[Column_red],row[Column_green],row[Column_blue]
        # Insere chaque ligne du CSV dans le tableau
        tab.append(col_select)

        #Permet la suppression des doublons et le tri
        Lt=sorted(set(tab))
        #print(Lt)

    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        categories = []
        for value, label, color_red, color_green, color_blue in Lt :
            #tab_list = value +' - '+label+' - '+color_red +' - '+ color_green +' - '+ color_blue

            # Largeur de la ligne
            v_width = str(Outline_width)

            #Polygon
            if layer.geometryType() == QgsWkbTypes.PolygonGeometry:
                symbol = QgsSymbol.defaultSymbol(layer.geometryType())
                # Set colour
                symbol.setColor(QColor(int(color_red),int(color_green),int(color_blue)))
                # Set opacity
                symbol.setOpacity(Transparency)
                # Set Stroke
                if Outline == False :
                    symbol.symbolLayer(0).setStrokeStyle(Qt.PenStyle(Qt.NoPen))
                symbol.symbolLayer(0).setStrokeColor(QColor(int(Stroke_Color_red),int(Stroke_Color_green),int(Stroke_Color_blue)))
                symbol.symbolLayer(0).setStrokeWidth(Outline_width)

                category = QgsRendererCategory(value, symbol, label)
                categories.append(category)

            #Line
            if layer.geometryType() == QgsWkbTypes.LineGeometry:
                symbol = QgsSymbol.defaultSymbol(layer.geometryType())
                # Set colour
                symbol.setColor(QColor.fromRgb(int(color_red),int(color_green),int(color_blue)))
                # Set opacity
                symbol.setOpacity(Transparency)
                symbol.setWidth (Outline_width)

                category = QgsRendererCategory(value, symbol, label)
                categories.append(category)

            #Point
            if layer.geometryType() == QgsWkbTypes.PointGeometry:
                symbol = QgsSymbol.defaultSymbol(layer.geometryType())
                # Set colour
                symbol.setColor(QColor.fromRgb(int(color_red),int(color_green),int(color_blue)))
                # Set opacity
                symbol.setOpacity(Transparency)
                # Set Stroke
                if Outline == False :
                    symbol.symbolLayer(0).setStrokeStyle(Qt.PenStyle(Qt.NoPen))
                symbol.symbolLayer(0).setStrokeColor(QColor(int(Stroke_Color_red),int(Stroke_Color_green),int(Stroke_Color_blue)))
                symbol.symbolLayer(0).setStrokeWidth(Outline_width)

                category = QgsRendererCategory(value, symbol, label)
                categories.append(category)

    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        expression = Value_field
        # Set the categorized renderer
        renderer = QgsCategorizedSymbolRenderer(expression, categories)
        layer.setRenderer(renderer)
        # Refresh layer
        layer.triggerRepaint()

        # Creation des fichiers de style
        if Save_layer_style_as_default :
            # QML
            layer.saveDefaultStyle()
