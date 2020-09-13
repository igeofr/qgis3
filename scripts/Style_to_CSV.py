import csv
layer = iface.activeLayer()
renderer  = layer.renderer()

with open('/Users/florianboret/out_semicolon.csv', 'w', newline='', encoding='utf-8') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL,delimiter=';')
    wr.writerow(['Value','Label','Hexa','RGBA','R','G','B','A'])
    if renderer.type() == 'categorizedSymbol': #Style categorise
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