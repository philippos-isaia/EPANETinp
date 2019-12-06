import json
#!/usr/bin/python
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
          'RULES': ['value'],
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
          'BACKDROP': ['DIMENSIONS', 'UNITS', 'FILE', 'OFFSET']}

# TODO Work on CONTROLS, RULES, ENERGY, REACTIONS, TIMES, REPORT, OPTIONS, LABELS, BACKDROP

# Step 1 - Open output JSON file
json_file = open('Water_bin.json')
EpanetOutput = json.load(json_file)

# Step 2 - Open initial input file
initial_input_file = open('Virtual_City_WaterNetwork.inp')

# Step 3 - Read Input file and split it to lists
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
        elif category == 'BACKDROP':
            try:
                uneditedmeasurements.pop(0)
            except:
                pass
            for details in uneditedmeasurements:
                result = [x.strip() for x in details.split('\t')]
                data = {}
                try:
                    data[result[0]] = '\t\t'.join(result[1:])
                except:
                    pass
                placetosave.append(data)
        elif category == 'PATTERNS':
            try:
                uneditedmeasurements.pop(1)
            except:
                pass
            try:
                uneditedmeasurements.pop(0)
            except:
                pass
            for details in uneditedmeasurements:
                result = [x.strip() for x in details.split('\t')]
                data = {}
                try:
                    data[ids[0]] = result[0]
                except:
                    pass
                try:
                    data[ids[1]] = '\t\t'.join(result[1:])
                except:
                    pass
                placetosave.append(data)
        else:
            try:
                uneditedmeasurements.pop(1)
            except:
                pass
            try:
                uneditedmeasurements.pop(0)
            except:
                pass
            for details in uneditedmeasurements:
                result = [x.strip() for x in details.split('\t')]
                data = {}
                for x in range(0, len(ids)):
                    textid = ids[x]
                    try:
                        data[textid] = result[x]
                    except:
                        data[textid] = ''
                placetosave.append(data)


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
    elif val[0] == '[JUNCTIONS]':
        addtodata(fields['JUNCTIONS'], val, inp_junctions, 'JUNCTIONS')
    elif val[0] == '[RESERVOIRS]':
        addtodata(fields['RESERVOIRS'], val, inp_reservoirs, 'RESERVOIRS')
    elif val[0] == '[TANKS]':
        addtodata(fields['TANKS'], val, inp_tanks, 'TANKS')
    elif val[0] == '[PIPES]':
        addtodata(fields['PIPES'], val, inp_pipes, 'PIPES')
    elif val[0] == '[PUMPS]':
        addtodata(fields['PUMPS'], val, inp_pumps, 'PUMPS')
    elif val[0] == '[VALVES]':
        addtodata(fields['VALVES'], val, inp_valves, 'VALVES')
    elif val[0] == '[TAGS]':
        addtodata(fields['TAGS'], val, inp_tags, 'TAGS')
    elif val[0] == '[DEMANDS]':
        addtodata(fields['DEMANDS'], val, inp_demands, 'DEMANDS')
    elif val[0] == '[STATUS]':
        addtodata(fields['STATUS'], val, inp_status, 'STATUS')
    elif val[0] == '[PATTERNS]':
        addtodata(fields['PATTERNS'], val, inp_patterns, 'PATTERNS')
    elif val[0] == '[CURVES]':
        addtodata(fields['CURVES'], val, inp_curves, 'CURVES')
    elif val[0] == '[CONTROLS]':
        addtodata(fields['CONTROLS'], val, inp_controls, 'CONTROLS')
    elif val[0] == '[RULES]':
        addtodata(fields['RULES'], val, inp_rules, 'RULES')
    elif val[0] == '[ENERGY]':
        addtodata(fields['ENERGY'], val, inp_energy, 'ENERGY')
    elif val[0] == '[EMITTERS]':
        addtodata(fields['EMITTERS'], val, inp_emitters, 'EMITTERS')
    elif val[0] == '[QUALITY]':
        addtodata(fields['QUALITY'], val, inp_quality, 'QUALITY')
    elif val[0] == '[SOURCES]':
        addtodata(fields['SOURCES'], val, inp_sources, 'SOURCES')
    elif val[0] == '[REACTIONS]':
        addtodata(fields['REACTIONS'], val, inp_reactions, 'REACTIONS')
    elif val[0] == '[MIXING]':
        addtodata(fields['MIXING'], val, inp_mixing, 'MIXING')
    elif val[0] == '[TIMES]':
        addtodata(fields['TIMES'], val, inp_times, 'TIMES')
    elif val[0] == '[REPORT]':
        addtodata(fields['REPORT'], val, inp_report, 'REPORT')
    elif val[0] == '[OPTIONS]':
        addtodata(fields['OPTIONS'], val, inp_options, 'OPTIONS')
    elif val[0] == '[COORDINATES]':
        addtodata(fields['COORDINATES'], val, inp_coordinates, 'COORDINATES')
    elif val[0] == '[VERTICES]':
        addtodata(fields['VERTICES'], val, inp_vertices, 'VERTICES')
    elif val[0] == '[LABELS]':
        addtodata(fields['LABELS'], val, inp_labels, 'LABELS')
    elif val[0] == '[BACKDROP]':
        addtodata(fields['BACKDROP'], val, inp_backdrop, 'BACKDROP')

def addDataToDatabase(tablename, tablefields, fieldsdata):
    # Add information to database
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    for value in fieldsdata:
        final_query = "INSERT INTO "+str(tablename)+"("+','.join(map(str, tablefields))+") VALUES ("
        empty_fields=[]
        for x in range(0,len(tablefields)):
            empty_fields.append('%s')
        final_query = final_query + ','.join(map(str, empty_fields)) + ");"
        data = tuple(value.values())
        cur.execute(final_query, data)
    # close communication with the PostgreSQL database server
    cur.close()
    # commit the changes
    conn.commit()

addDataToDatabase("JUNCTIONS", ["ID", "Elev", "Demand", "Pattern"], inp_junctions)
addDataToDatabase("RESERVOIRS", ["ID", "Head", "Pattern"], inp_reservoirs)
addDataToDatabase("TANKS", ["ID", "Elevation", "InitLevel", "MinLevel", "MaxLevel", "Diameter", "MinVol", "VolCurve"], inp_tanks)
addDataToDatabase("PIPES", ["ID", "Node1", "Node2", "Length", "Diameter", "Roughness", "MinorLoss", "Status"], inp_pipes)
addDataToDatabase("JUNCTIONS", ["ID", "Elev", "Demand", "Pattern"], inp_junctions)
addDataToDatabase("PUMPS", ["ID", "Node1", "Node2", "Parameters"], inp_pumps)
addDataToDatabase("VALVES", ["ID", "Node1", "Node2", "Diameter", "Type", "Setting", "MinorLoss"], inp_valves)
addDataToDatabase("DEMANDS", ["Junction", "Demand", "Pattern", "Category"], inp_demands)
addDataToDatabase("STATUS", ["ID", "StatusSetting"], inp_status)
addDataToDatabase("PATTERNS", ["ID", "Multipliers"], inp_patterns)
addDataToDatabase("CURVES", ["ID", "XValue", "YValue"], inp_curves)
addDataToDatabase("ENERGY", ["field", "value"], inp_energy)
addDataToDatabase("TIMES", ["field", "value"], inp_times)
addDataToDatabase("REPORT", ["field", "value"], inp_report)
addDataToDatabase("OPTIONS", ["field", "value"], inp_options)
addDataToDatabase("EMITTERS", ["Junction", "Coefficient"], inp_emitters)
addDataToDatabase("SOURCES", ["Node", "Type", "Quality", "Pattern"], inp_sources)
addDataToDatabase("REACTIONS", ["Type", "Coefficient"], inp_reactions)
addDataToDatabase("MIXING", ["Tank", "Model", "Volume"], inp_mixing)
addDataToDatabase("COORDINATES", ["Node", "XCoord", "YCoord"], inp_coordinates)
addDataToDatabase("VERTICES", ["Link", "XCoord", "YCoord"], inp_vertices)
addDataToDatabase("LABELS", ["XCoord", "YCoord", "Label", "Anchor"], inp_labels)

def writeTheTitles(file,title):
    file.write("\n")
    file.write(str(title)+"\n")
    file.write(";")


def writeTheValuesUnderTitles(file,infovariable,title):
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
    try:
        for it in infovariable:
            for k, v in it.items():
                file.write(k + '\t' + v + '\n')
    except:
        pass


def newinputfilecreation(filename):
    f = open(filename, "w+")
    f.write("[TITLE]" + "\n")
    f.write(inp_title[0]['title'] + "\n")
    writeTheValuesUnderTitles(f,inp_junctions, "[JUNCTIONS]")
    writeTheValuesUnderTitles(f, inp_reservoirs, "[RESERVOIRS]")
    writeTheValuesUnderTitles(f, inp_tanks, "[TANKS]")
    writeTheValuesUnderTitles(f, inp_pipes, "[PIPES]")
    writeTheValuesUnderTitles(f, inp_pumps, "[PUMPS]")
    writeTheValuesUnderTitles(f, inp_valves, "[VALVES]")
    writeTheValuesUnderTitles(f, inp_tags, "[TAGS]")
    writeTheValuesUnderTitles(f, inp_demands, "[DEMANDS]")
    writeTheValuesUnderTitles(f, inp_status, "[STATUS]")
    writeTheValuesUnderTitles(f, inp_patterns, "[PATTERNS]")
    writeTheValuesUnderTitles(f, inp_curves, "[CURVES]")
    writeTheValuesUnderTitles(f, inp_controls, "[CONTROLS]")
    writeTheValuesUnderTitles(f, inp_rules, "[RULES]")
    writeTheValuesUnderTitlesNoFields(f, inp_energy, "[ENERGY]")
    writeTheValuesUnderTitles(f, inp_emitters, "[EMITTERS]")
    writeTheValuesUnderTitles(f, inp_quality, "[QUALITY]")
    writeTheValuesUnderTitles(f, inp_sources, "[SOURCES]")
    writeTheValuesUnderTitlesNoFields(f, inp_reactions, "[REACTIONS]")
    writeTheValuesUnderTitles(f, inp_mixing, "[MIXING]")
    writeTheValuesUnderTitlesNoFields(f, inp_times, "[TIMES]")
    writeTheValuesUnderTitlesNoFields(f, inp_report, "[REPORT]")
    writeTheValuesUnderTitlesNoFields(f, inp_options, "[OPTIONS]")
    writeTheValuesUnderTitles(f, inp_coordinates, "[COORDINATES]")
    writeTheValuesUnderTitles(f, inp_vertices, "[VERTICES]")
    writeTheValuesUnderTitles(f, inp_labels, "[LABELS]")
    writeTheValuesUnderTitlesNoFields(f, inp_backdrop, "[BACKDROP]")
    f.write("\n")
    f.write("[END]" + "\n")
    f.close()


newinputfilecreation('newepanetinput.inp')