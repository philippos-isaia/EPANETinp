#!/usr/bin/python
import json
import psycopg2
from config import config

# Define EPANET INP Keywords
epanet_keywords = ['[TITLE]', '[JUNCTIONS]', '[RESERVOIRS]', '[TANKS]', '[PIPES]', '[PUMPS]', '[VALVES]', '[EMITTERS]',
                   '[CURVES]', '[PATTERNS]', '[ENERGY]', '[STATUS]', '[CONTROLS]', '[RULES]', '[DEMANDS]',
                   '[QUALITY]', '[REACTIONS]', '[SOURCES]', '[MIXING]',
                   '[OPTIONS]', '[TIMES]', '[REPORT]',
                   '[COORDINATES]', '[VERTICES]', '[LABELS]', '[BACKDROP]', '[TAGS]',
                   '[END]']

# Define EPANET Keywords Fields
fields = {'JUNCTIONS': ['ID', 'Elev', 'Demand', 'Pattern'],
          'RESERVOIRS': ['ID', 'Head', 'Pattern'],
          'TANKS': ['ID', 'Elevation', 'InitLevel', 'MinLevel', 'MaxLevel', 'Diameter', 'MinVol', 'VolCurve'],
          'PIPES': ['ID', 'Node1', 'Node2', 'Length', 'Diameter', 'Roughness', 'MinorLoss', 'Status'],
          'PUMPS': ['ID', 'Node1', 'Node2', 'Parameters'],
          'VALVES': ['ID', 'Node1', 'Node2', 'Diameter', 'Type', 'Setting', 'MinorLoss'],
          'TAGS': ['Object', 'ID', 'Tag'],
          'DEMANDS': ['Junction', 'Demand', 'Pattern', 'Category'],
          'STATUS': ['ID', 'StatusSetting'],
          'PATTERNS': ['ID', 'Multipliers'],
          'CURVES': ['ID', 'XValue', 'YValue'],
          'CONTROLS': ['----'],
          'RULES': ['ruleID', 'Rule'],
          'ENERGY': ['field', 'value'],
          'EMITTERS': ['Junction', 'Coefficient'],
          'QUALITY': ['Node', 'InitQual'],
          'SOURCES': ['Node', 'Type', 'Quality', 'Pattern'],
          'REACTIONS': ['Type', 'Coefficient'],
          'MIXING': ['Tank', 'Model', 'Volume'],
          'TIMES': ['field', 'value'],
          'REPORT': ['field', 'value'],
          'OPTIONS': ['field', 'value'],
          'COORDINATES': ['Node', 'XCoord', 'YCoord'],
          'VERTICES': ['Link', 'XCoord', 'YCoord'],
          'LABELS': ['XCoord', 'YCoord', 'Label', 'Anchor'],
          'BACKDROP': ['field', 'value']}

'''
# Step 1 - Open output JSON file
json_file = open('Water_bin.json')
EpanetOutput = json.load(json_file)
'''


def readinputfile(initial_input_filename):
    initial_input_file = open(initial_input_filename)
    finalresult = []
    currentresult = []
    RecordingMode = False
    for line in initial_input_file:
        if line.strip() in epanet_keywords:
            if len(currentresult) != 0:
                finalresult.append(currentresult)
            currentresult = []
            currentresult.append(line.strip())
        else:
            if len(line.strip()) != 0:
                currentresult.append(line.strip())
    return finalresult


def addtodata(ids, uneditedmeasurements, placetosave, category):
    if len(uneditedmeasurements) > 1:
        if category == 'CURVES' or category == 'REACTIONS' or category == 'ENERGY' or category == 'TIMES' or category == 'REPORT' or category =='OPTIONS':
            for details in uneditedmeasurements:
                if details[0] != '[' and details[0] != ';':
                    result = [x.strip() for x in details.split('\t')]
                    data = {}
                    for x in range(0, len(ids)):
                        textid = ids[x]
                        try:
                            data[textid] = result[x]
                        except:
                            data[textid] = ''
                    placetosave.append(data)
        elif category == 'PATTERNS' or category == 'BACKDROP':
            for details in uneditedmeasurements:
                if details[0] != '[' and details[0] != ';':
                    result = [x.strip() for x in details.split('\t')]
                    data = {}
                    try:
                        data[ids[0]] = result[0]
                    except:
                        pass
                    try:
                        data[ids[1]] = ','.join(result[1:])
                    except:
                        pass
                    placetosave.append(data)
        elif category == 'RULES':
            data=[]
            placetosave1=[]
            for details in uneditedmeasurements:
                if details[0] != '[' and details[0] != ';':
                    if 'RULE' in details:
                        if data:
                            placetosave1.append(data)
                        data=[]
                        data.append(details.strip())
                    else:
                        data.append(details.strip())
            if data:
                placetosave1.append(data)
            for value in placetosave1:
                data={}
                try:
                    data[ids[0]] = value[0]
                except:
                    pass
                try:
                    data[ids[1]] = ' \n '.join(value[1:])
                except:
                    pass
                placetosave.append(data)
        else:
            for details in uneditedmeasurements:
                if details[0] != '[' and details[0] != ';':
                    result = [x.strip() for x in details.split('\t')]
                    result = list(filter(None, result))
                    data = {}
                    for x in range(0, len(ids)):
                        textid = ids[x]
                        try:
                            data[textid] = result[x]
                        except:
                            data[textid] = ''
                    placetosave.append(data)


def addinfotolists(finalresult):
    fullinputs = {}
    inp_title = []
    inp_junctions = []
    inp_reservoirs = []
    inp_tanks = []
    inp_pipes = []
    inp_pumps = []
    inp_valves = []
    inp_tags = []
    inp_demands = []
    inp_status = []
    inp_patterns = []
    inp_curves = []
    inp_controls = []
    inp_rules = []
    inp_energy = []
    inp_emitters = []
    inp_quality = []
    inp_sources = []
    inp_reactions = []
    inp_mixing = []
    inp_times = []
    inp_report = []
    inp_options = []
    inp_coordinates = []
    inp_vertices = []
    inp_labels = []
    inp_backdrop = []

    for val in finalresult:
        if val[0] == '[TITLE]':
            data = {}
            data["title"] = val[1]
            inp_title.append(data)
            fullinputs['TITLE'] = val[1]
        elif val[0] == '[JUNCTIONS]':
            addtodata(fields['JUNCTIONS'], val, inp_junctions, 'JUNCTIONS')
            fullinputs['JUNCTIONS'] = inp_junctions
        elif val[0] == '[RESERVOIRS]':
            addtodata(fields['RESERVOIRS'], val, inp_reservoirs, 'RESERVOIRS')
            fullinputs['RESERVOIRS'] = inp_reservoirs
        elif val[0] == '[TANKS]':
            addtodata(fields['TANKS'], val, inp_tanks, 'TANKS')
            fullinputs['TANKS'] = inp_tanks
        elif val[0] == '[PIPES]':
            addtodata(fields['PIPES'], val, inp_pipes, 'PIPES')
            fullinputs['PIPES'] = inp_pipes
        elif val[0] == '[PUMPS]':
            addtodata(fields['PUMPS'], val, inp_pumps, 'PUMPS')
            fullinputs['PUMPS'] = inp_pumps
        elif val[0] == '[VALVES]':
            addtodata(fields['VALVES'], val, inp_valves, 'VALVES')
            fullinputs['VALVES'] = inp_valves
        elif val[0] == '[TAGS]':
            addtodata(fields['TAGS'], val, inp_tags, 'TAGS')
            fullinputs['TAGS'] = inp_tags
        elif val[0] == '[DEMANDS]':
            addtodata(fields['DEMANDS'], val, inp_demands, 'DEMANDS')
            fullinputs['DEMANDS'] = inp_demands
        elif val[0] == '[STATUS]':
            addtodata(fields['STATUS'], val, inp_status, 'STATUS')
            fullinputs['STATUS'] = inp_status
        elif val[0] == '[PATTERNS]':
            addtodata(fields['PATTERNS'], val, inp_patterns, 'PATTERNS')
            fullinputs['PATTERNS'] = inp_patterns
        elif val[0] == '[CURVES]':
            addtodata(fields['CURVES'], val, inp_curves, 'CURVES')
            fullinputs['CURVES'] = inp_curves
        elif val[0] == '[CONTROLS]':
            addtodata(fields['CONTROLS'], val, inp_controls, 'CONTROLS')
            fullinputs['CONTROLS'] = inp_controls
        elif val[0] == '[RULES]':
            addtodata(fields['RULES'], val, inp_rules, 'RULES')
            fullinputs['RULES'] = inp_rules
        elif val[0] == '[ENERGY]':
            addtodata(fields['ENERGY'], val, inp_energy, 'ENERGY')
            fullinputs['ENERGY'] = inp_energy
        elif val[0] == '[EMITTERS]':
            addtodata(fields['EMITTERS'], val, inp_emitters, 'EMITTERS')
            fullinputs['EMITTERS'] = inp_emitters
        elif val[0] == '[QUALITY]':
            addtodata(fields['QUALITY'], val, inp_quality, 'QUALITY')
            fullinputs['QUALITY'] = inp_quality
        elif val[0] == '[SOURCES]':
            addtodata(fields['SOURCES'], val, inp_sources, 'SOURCES')
            fullinputs['SOURCES'] = inp_sources
        elif val[0] == '[REACTIONS]':
            addtodata(fields['REACTIONS'], val, inp_reactions, 'REACTIONS')
            fullinputs['REACTIONS'] = inp_reactions
        elif val[0] == '[MIXING]':
            addtodata(fields['MIXING'], val, inp_mixing, 'MIXING')
            fullinputs['MIXING'] = inp_mixing
        elif val[0] == '[TIMES]':
            addtodata(fields['TIMES'], val, inp_times, 'TIMES')
            fullinputs['TIMES'] = inp_times
        elif val[0] == '[REPORT]':
            addtodata(fields['REPORT'], val, inp_report, 'REPORT')
            fullinputs['REPORT'] = inp_report
        elif val[0] == '[OPTIONS]':
            addtodata(fields['OPTIONS'], val, inp_options, 'OPTIONS')
            fullinputs['OPTIONS'] = inp_options
        elif val[0] == '[COORDINATES]':
            addtodata(fields['COORDINATES'], val, inp_coordinates, 'COORDINATES')
            fullinputs['COORDINATES'] = inp_coordinates
        elif val[0] == '[VERTICES]':
            addtodata(fields['VERTICES'], val, inp_vertices, 'VERTICES')
            fullinputs['VERTICES'] = inp_vertices
        elif val[0] == '[LABELS]':
            addtodata(fields['LABELS'], val, inp_labels, 'LABELS')
            fullinputs['LABELS'] = inp_labels
        elif val[0] == '[BACKDROP]':
            addtodata(fields['BACKDROP'], val, inp_backdrop, 'BACKDROP')
            fullinputs['BACKDROP'] = inp_backdrop

    return fullinputs


def addDataToDatabase(allfields, fieldsdic):
    # Add information to database
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    for val in allfields:
        for value in fieldsdic[val]:
            final_query = "INSERT INTO " + str(val) + "(" + ','.join(map(str, allfields[val])) + ") VALUES ("
            empty_fields = []
            for x in range(0, len(allfields[val])):
                empty_fields.append('%s')
            final_query = final_query + ','.join(map(str, empty_fields)) + ");"
            data = tuple(value.values())
            cur.execute(final_query, data)
    # close communication with the PostgreSQL database server
    cur.close()
    # commit the changes
    conn.commit()


def writeTheTitles(file,title):
    file.write("\n")
    file.write(str(title)+"\n")
    file.write(";")


def writeTheValuesUnderTitles(file,infovariable,title):
    if title == '[PATTERNS]':
        writeTheTitles(file, title)
        try:
            for value in infovariable[0].keys():
                file.write(value + "\t\t\t\t")
            file.write("\n")
        except:
            pass
        try:
            for entries in infovariable:
                for value in entries.values():
                    if ',' in value:
                        value = value.replace(",", "\t\t")
                    file.write(value + "\t\t")
                file.write("\n")
        except:
            pass
    elif title == '[RULES]':
        writeTheTitles(file, title)
        try:
            file.write("\n")
            for entries in infovariable:
                for value in entries.values():
                    file.write(value + "\n")
                file.write("\n")
        except:
            pass
    else:
        writeTheTitles(file,title)
        try:
            for value in infovariable[0].keys():
                file.write(value + "\t\t\t\t")
            file.write("\n")
        except:
            pass
        try:
            for entries in infovariable:
                for value in entries.values():
                    file.write(value + "\t\t\t\t")
                file.write("\n")
        except:
            pass


def writeTheValuesUnderTitlesNoFields(file, infovariable,title):
    writeTheTitles(file,title)
    if title == '[ENERGY]' or title == '[REACTIONS]' or title == '[TIMES]' or title == '[REPORT]' or title == '[OPTIONS]' or title == '[BACKDROP]':
        file.write('\n')
        try:
            for entries in infovariable:
                for value in entries.values():
                    if title == '[BACKDROP]':
                        value = value.replace(",", "\t\t")
                    file.write(value + '\t')
                file.write("\n")
        except:
            pass
    else:
        try:
            for it in infovariable:
                for k, v in it.items():
                    file.write(k + '\t' + v + '\n')
        except:
            pass


def newinputfilecreation(filename,datadic):
    f = open(filename, "w+")
    f.write("[TITLE]" + "\n")
    f.write(datadic['TITLE'] + "\n")
    writeTheValuesUnderTitles(f, datadic['JUNCTIONS'], "[JUNCTIONS]")
    writeTheValuesUnderTitles(f, datadic['RESERVOIRS'], "[RESERVOIRS]")
    writeTheValuesUnderTitles(f, datadic['TANKS'], "[TANKS]")
    writeTheValuesUnderTitles(f, datadic['PIPES'], "[PIPES]")
    writeTheValuesUnderTitles(f, datadic['PUMPS'], "[PUMPS]")
    writeTheValuesUnderTitles(f, datadic['VALVES'], "[VALVES]")
    writeTheValuesUnderTitles(f, datadic['TAGS'], "[TAGS]")
    writeTheValuesUnderTitles(f, datadic['DEMANDS'], "[DEMANDS]")
    writeTheValuesUnderTitles(f, datadic['STATUS'], "[STATUS]")
    writeTheValuesUnderTitles(f, datadic['PATTERNS'], "[PATTERNS]")
    writeTheValuesUnderTitles(f, datadic['CURVES'], "[CURVES]")
    writeTheValuesUnderTitles(f, datadic['CONTROLS'], "[CONTROLS]")
    writeTheValuesUnderTitles(f, datadic['RULES'], "[RULES]")
    writeTheValuesUnderTitlesNoFields(f, datadic['ENERGY'], "[ENERGY]")
    writeTheValuesUnderTitles(f, datadic['EMITTERS'], "[EMITTERS]")
    writeTheValuesUnderTitles(f, datadic['QUALITY'], "[QUALITY]")
    writeTheValuesUnderTitles(f, datadic['SOURCES'], "[SOURCES]")
    writeTheValuesUnderTitlesNoFields(f, datadic['REACTIONS'], "[REACTIONS]")
    writeTheValuesUnderTitles(f, datadic['MIXING'], "[MIXING]")
    writeTheValuesUnderTitlesNoFields(f, datadic['TIMES'], "[TIMES]")
    writeTheValuesUnderTitlesNoFields(f, datadic['REPORT'], "[REPORT]")
    writeTheValuesUnderTitlesNoFields(f, datadic['OPTIONS'], "[OPTIONS]")
    writeTheValuesUnderTitles(f, datadic['COORDINATES'], "[COORDINATES]")
    writeTheValuesUnderTitles(f, datadic['VERTICES'], "[VERTICES]")
    writeTheValuesUnderTitles(f, datadic['LABELS'], "[LABELS]")
    writeTheValuesUnderTitlesNoFields(f, datadic['BACKDROP'], "[BACKDROP]")
    f.write("\n")
    f.write("[END]" + "\n")
    f.close()


if __name__ == '__main__':
    finalresult = readinputfile('Virtual_City_WaterNetwork.inp')
    fullinputs = addinfotolists(finalresult)

    allfields = {'JUNCTIONS': ["ID", "Elev", "Demand", "Pattern"],
                 "RESERVOIRS": ["ID", "Head", "Pattern"],
                 "TANKS": ["ID", "Elevation", "InitLevel", "MinLevel", "MaxLevel", "Diameter", "MinVol", "VolCurve"],
                 "PIPES": ["ID", "Node1", "Node2", "Length", "Diameter", "Roughness", "MinorLoss", "Status"],
                 "PUMPS": ["ID", "Node1", "Node2", "Parameters"],
                 "VALVES": ["ID", "Node1", "Node2", "Diameter", "Type", "Setting", "MinorLoss"],
                 "DEMANDS": ["Junction", "Demand", "Pattern", "Category"],
                 "STATUS": ["ID", "StatusSetting"],
                 "PATTERNS": ["ID", "Multipliers"],
                 "CURVES": ["ID", "XValue", "YValue"],
                 "CONTROLS": ["control"],
                 "RULES": ["ruleID", "Rule"],
                 "ENERGY": ["field", "value"],
                 "TIMES": ["field", "value"],
                 "REPORT": ["field", "value"],
                 "OPTIONS": ["field", "value"],
                 "EMITTERS": ["Junction", "Coefficient"],
                 "QUALITY": ["Node", "InitQual"],
                 "SOURCES": ["Node", "Type", "Quality", "Pattern"],
                 "REACTIONS": ["Type", "Coefficient"],
                 "MIXING": ["Tank", "Model", "Volume"],
                 "COORDINATES": ["Node", "XCoord", "YCoord"],
                 "VERTICES": ["Link", "XCoord", "YCoord"],
                 "LABELS": ["XCoord", "YCoord", "Label", "Anchor"],
                 "BACKDROP": ["field", "value"],
                 "TAGS": ["Object", "ID", "Tag"]}
    addDataToDatabase(allfields, fullinputs)
    newinputfilecreation('newepanetinput.inp', fullinputs)
