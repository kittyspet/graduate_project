from ReaderLinq import *
from GeneratorGant import *

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

def getDataFormat(data):
    date_object = datetime.strptime(data.split('.')[0], "%Y-%m-%dT%H:%M:%S")
    return date_object.strftime("%d.%m.%Y")

date_format = "%Y-%m-%d"
def getPlannedDate(str):
    return datetime.strptime(str[0:10], date_format)

def getDataFromMilestone(milestone):
        return datetime.strptime(milestone["systemEndDate"], "%d.%m.%Y")


# def parsingJsonVeh(json_data):
#     milestones = []
#     phases = {}

#     for row in reversed(json_data): # TODO: развернуть при return
#         phases[row['parentProject']] = (getPlannedDate(row['parentPlanDateStart']), getPlannedDate(row['parentPlanDateEnd']))
#         milestones.append({
#             'phase': len(phases) - 1,
#             'date': f"{row['systemStartDate'][5:7]}.{row['systemStartDate'][0:4]}",
#             'status': row['status'],
#             'nameProject': row['nameProject'],
#             'systemEndDate': getDataFormat(row['systemEndDate']),
#             'ownerName': row['ownerName']
#         })

#     return milestones, phases


def parsingJsonVeh(json_data): # TODO: добавить настройки для парсинга
        milestones = []
        phases = {} # (ProgrammParser.getPlannedDate(row['parentPlanDateStart']), ProgrammParser.getPlannedDate(row['parentPlanDateEnd']), [])

        for row in reversed(json_data):
            milestone = {
                 'date': f"{row['systemStartDate'][5:7]}.{row['systemStartDate'][0:4]}",
                'status': row['status'],
                'nameProject': row['nameProject'],
                'systemEndDate': getDataFormat(row['systemEndDate']),
                'ownerName': row['ownerName'],
                'id': row["projectId"]
            }
            if row['parentProject'] in phases:
                phases[row['parentProject']][2] += [milestone]
            else:
                phases[row['parentProject']] = [getPlannedDate(row['parentPlanDateStart']), getPlannedDate(row['parentPlanDateEnd']), [milestone]]

            milestone['phase'] = len(phases) - 1
            # sort
            milestones.append(milestone)

        for key, value in phases.items():
            value[2].sort(key=getDataFromMilestone)

        return milestones, phases

LINQIDSJ = '4f171ba3-ce3a-43c8-9b4a-2030485c42d3' # ssg
LINQIDMC = 'a52d4fa9-2f6c-45b2-9d05-f66700526384' # mc

# LINQID = '4f171ba3-ce3a-43c8-9b4a-2030485c42d3'


reader= ReaderLinq()
generatorGant = GeneratorGant()

dataMC = reader.getResponseJson(idLINQ=LINQIDMC, pageSize=100)
dataSJ = reader.getResponseJson(idLINQ=LINQIDSJ, pageSize=100)

import json

# with open('data2.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)

with open('C:/rtlink/attachment/data_report/dataMC.json', 'w', encoding='utf-8') as file:
    json.dump(dataMC, file, ensure_ascii=False)
with open('C:/rtlink/attachment/data_report/dataSJ.json', 'w', encoding='utf-8') as file:
    json.dump(dataSJ, file, ensure_ascii=False)

milestonesMC, phasesMC = parsingJsonVeh(dataMC)
milestonesSJ, phasesSJ = parsingJsonVeh(dataSJ)

milestones = milestonesMC + milestonesSJ
 
statusMilestoneLinq = 'fa2e78e9-c572-45a9-917d-0e0d8de81f07'
for milestone in milestones:
    with open("C:/rtlink/attachment/data_report/milestones/" + milestone["id"] + '.json', 'w', encoding='utf-8') as f:
       json.dump(reader.getResponseJson(idLINQ=statusMilestoneLinq, pageSize=100, parameters={"projectId": milestone["id"]}), f, ensure_ascii=False)


image_buffer = generatorGant.generate(phase_boundaries=phasesMC, milestones=milestonesMC)

with open('C:/rtlink/attachment/image/MC.png', 'wb') as f:
    f.write(image_buffer.getvalue())

image_buffer = generatorGant.generate(phase_boundaries=phasesSJ, milestones=milestonesSJ)

with open('C:/rtlink/attachment/image/SJ.png', 'wb') as f:
    f.write(image_buffer.getvalue())



