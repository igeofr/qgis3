import csv
layer = iface.activeLayer()
renderer  = layer.renderer()

# Open a file with access mode 'a'
file_object = open('/Users/florianboret/test_txt.txt', 'w')


if renderer.type() == 'categorizedSymbol': #Style categorise
    categories = renderer.categories()

    for category in categories: # Recuperation des infos et ecriture dans le csv
        line1 = 'CLASS'
        line2 = '   NAME "'+(category.label())+'"'
        line3 = '       TEMPLATE "../template/getfeatureinfo/{LAYER_NAME}.html"'
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


