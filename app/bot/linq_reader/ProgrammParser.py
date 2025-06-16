from datetime import datetime

class ProgrammParser:
    
    @staticmethod
    def parseProgramm(json_data): # TODO: добавить настройки для парсинга
        milestones = []
        phases = {} # (ProgrammParser.getPlannedDate(row['parentPlanDateStart']), ProgrammParser.getPlannedDate(row['parentPlanDateEnd']), [])

        for row in reversed(json_data):
            milestone = {
                'phase': len(phases),
                'date': f"{row['systemStartDate'][5:7]}.{row['systemStartDate'][0:4]}",
                'status': row['status'],
                'nameProject': row['nameProject'],
                'systemEndDate': ProgrammParser.getDataFormat(row['systemEndDate']),
                'ownerName': row['ownerName'],
                'id': row["projectId"]
            }
            # sort
            if row['parentProject'] in phases:
                phases[row['parentProject']][2] += [milestone]
            else:
                phases[row['parentProject']] = [ProgrammParser.getPlannedDate(row['parentPlanDateStart']), ProgrammParser.getPlannedDate(row['parentPlanDateEnd']), [milestone]]
            milestones.append(milestone)

        for key, value in phases.items():
            value[2].sort(key=ProgrammParser.getDataFromMilestone)

        return milestones, phases

    @staticmethod
    def getDataFromMilestone(milestone):
        return datetime.strptime(milestone["systemEndDate"], "%d.%m.%Y")

    @staticmethod
    def getDataFormat(data):
        date_object = datetime.strptime(data.split('.')[0], "%Y-%m-%dT%H:%M:%S")
        return date_object.strftime("%d.%m.%Y")

    @staticmethod
    def getPlannedDate(str):
        date_format = "%Y-%m-%d"
        return datetime.strptime(str[0:10], date_format)