import matplotlib.pyplot as plt
import matplotlib
import matplotlib.patches as patches
from datetime import datetime
import matplotlib.lines as mlines
import textwrap
from io import BytesIO


# print(matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf'))



class GeneratorGant:
    def __init__(self, quarters_per_year=4, months_per_quarter=3):
        self.quarters_per_year = quarters_per_year
        self.months_per_quarter = months_per_quarter
        self.setDataVeh()
        self.active_status = set()

    @staticmethod
    def wrap_text(text, width=15):
        """Перенос текста для отображения"""
        return "\n".join(textwrap.wrap(text, width=width, break_long_words=False))

    @staticmethod
    def get_data_from_milestone(milestone):
        return datetime.strptime(milestone['date'], '%m.%Y')

    @staticmethod
    def get_quarter_and_year(date_str):
        """Определение года и квартала по дате"""
        date = datetime.strptime(date_str, '%m.%Y')
        year = date.year
        month = date.month
        quarter = (month - 1) // 3 + 1
        return year, quarter, date
    
    @staticmethod
    def get_quarter_from_date(date):
        """Определение года и квартала по дате"""
        year = date.year
        month = date.month
        quarter = (month - 1) // 3 + 1
        return year, quarter

    def generate(self, phase_boundaries, milestones):
        """
        Генерация диаграммы Ганта.

        :param phases: Список фаз (названия фаз).
        :param milestones: Список вех в формате:
            [{'phase': 0, 'date': "08.2024", 'status': "complete", 'ownerName': 'ownername', 'systemEndDate': '12.12.24', 'nameProject': 'name'}, ...]
        :return: Буфер изображения в формате BytesIO.
        """

        # plt.rc('text', usetex=True)

        self.active_status = set()
        matplotlib.rcParams['font.family'] = ['cursive', 'monospace']
        phases = [self.wrap_text(phase, 17) for phase in phase_boundaries.keys()]
        milestones = [milestone | {'color': self.colors_veh[milestone['status']]} for milestone in milestones] # TODO: (есть заметка в базе знаний обсидиан)рефактор чтобы за одно проход в одну строчку
        
        # Распределение вех по кварталам
        self.min_date = datetime(3000, 1, 1, 0,0,0)
        self.max_date = datetime(1000, 1, 1, 0,0,0)
        milestones_by_quarter_by_phase = {}
        for milestone in milestones:
            year, quarter, date = self.get_quarter_and_year(milestone['date'])
            self.min_date = min(self.min_date, date)
            self.max_date = max(self.max_date, date)
            phase = milestone['phase']
            self.active_status.add(milestone['status'])
            if (year, quarter, phase) not in milestones_by_quarter_by_phase:
                milestones_by_quarter_by_phase[(year, quarter, phase)] = []
            milestones_by_quarter_by_phase[(year, quarter, phase)].append(milestone)

        year, quarter = self.get_quarter_from_date(self.min_date)
        self.offset_from_beginning = (quarter - 1)*3
        print(self.offset_from_beginning)

        total_months = (self.max_date.year - self.min_date.year) * 12 + (self.max_date.month - self.min_date.month) + 1


        # Настройка графика
         # Расчёт вертикального масштаба для фаз
        phase_offsets = [0] * len(phases)  # Смещение для каждой фазы
        for (year, quarter, phase), milestones in milestones_by_quarter_by_phase.items():
            if (phase == 3):
                pass
            sum_labels = sum((len(self.getLabelVeh(milestone=m).split("\n")) + 1) for m in milestones)
            phase_offsets[phase] = max(phase_offsets[phase], sum_labels * 0.22) # Учитываем текстовые строки

        phase_offsets = [ max(offset, 1) for offset in phase_offsets]

        # Общий размер по вертикали
        total_height = sum(phase_offsets)

        phase_ycords = []
        buf = 0
        for i, phase in enumerate(phases):
            buf += phase_offsets[i] + 0.5
            phase_ycords.append(buf)
            

        # Настройка графика
        fig, ax = plt.subplots(figsize=(24, max(8, total_height)))


        cord_start_data = self.getXCordByDate(self.min_date)
        cord_end_data = self.getXCordByDate(self.max_date)
        # Рисуем фазы
        phase_names = list(phase_boundaries.keys())
        for i, (phase_name, (start_date, end_date, milestones)) in enumerate(phase_boundaries.items()):
            start_date_cut = max(start_date, self.min_date)
            end_date_cut = min(end_date, self.max_date)
            # start_offset = (start_date.year - min_date.year) * 12 + (start_date.month - min_date.month)
            year, quarter_start= self.get_quarter_from_date(start_date_cut)
            # start_offset = (year - self.min_date.year) * self.quarters_per_year * self.months_per_quarter + (quarter - 1) * self.months_per_quarter+1.5 # нужен костыль, что если первый год, то эту хуйню не прибавляем типа * 
            start_offset = self.getXCordByDate(start_date_cut)
            # end_offset = (end_date.year - min_date.year) * 12 + (end_date.month - min_date.month) + 1
            
            year, quarter_end= self.get_quarter_from_date(end_date_cut)
            # end_offset = (year - self.min_date.year) * self.quarters_per_year * self.months_per_quarter + (quarter - 1) * self.months_per_quarter+1.5
            end_offset = self.getXCordByDate(end_date_cut)
            
            if (quarter_start == quarter_end):
                start_offset -= 1.5
                end_offset += 1.5
            else:
                if (start_date < self.min_date):
                    start_offset -= 1.5
                if (end_date > self.max_date):
                    end_offset += 1.5

            
            ax.hlines(
                y=phase_ycords[i],
                xmin=start_offset,
                xmax=end_offset,
                color='#4F8AD8',
                linewidth=4,
            )

            ax.hlines(
                y=phase_ycords[i] + 0.4,
                xmin=cord_start_data - 1.5,
                xmax=cord_end_data + 1.5,
                color='#464646',
                linestyle='dashed',
                alpha=0.5,
                linewidth=0.7,
            )

        # Рисуем вехи
        for (year, quarter, phase), milestones in milestones_by_quarter_by_phase.items():
            x_position = self.getXCordByDate(date=datetime(year=year, month=quarter*3 - 1, day=1)) # TODO может тут добавить получение квартала для миндате
            temp = ""
            for offset, milestone in enumerate(milestones):
                # # x_position = quarter_start + self.months_per_quarter / 2 - offset * 0.3
                # x_position = self.getXCordByDate(self.get_data_from_milestone(milestone)) - offset * 0.3
                ax.scatter(
                    x_position - offset * 0.3,
                    phase_ycords[phase],
                    color=milestone['color'],
                    s=300,
                    marker='D',
                    edgecolor='black',
                    linewidth=1.2,
                    zorder=5
                )
                temp = "\n\n".join([temp, self.getLabelVeh(milestone)])
            
            text = ax.text(
                x_position - 0.2,
                phase_ycords[phase] - 0.3, # TODO: подумать как лучше сделать смещение вниз, чтобы текст можно было настроить
                temp[2:],
                ha='left',
                va='top',
                fontsize=8,
                color='black',
            )
            # text = ax.text(
            #     x_position - 0.2,
            #     phase_ycords[phase] - 2, # TODO: подумать как лучше сделать смещение вниз, чтобы текст можно было настроить
            #     'testr4srt2008 $\\mathbf{Swing-State Counties}$',
            #     ha='left',
            #     va='top',
            #     fontsize=8,
            #     color='black',
            #     # transform=ax.transAxes
            #     # usetex=False
            # )
            
            # ax.annotate("world!", xycoords=text, xy=(0, 0), verticalalignment="bottom", color="blue", family="serif")  # пользовательские свойства

        # Рисуем шапку с годами и кварталами
        print ("mindate: ", self.min_date)
        print ("maxdate: ", self.max_date)
        total_years = self.max_date.year - self.min_date.year + 1

        # Первый год
        year, min_data_quarter = self.get_quarter_from_date(self.min_date)

        year_start = 0
        year_end = year_start + self.quarters_per_year * self.months_per_quarter - self.offset_from_beginning
        ax.text((year_start + year_end) / 2, phase_ycords[-1] + 1, f'{self.min_date.year + 0}', ha='center', fontsize=12, fontweight='bold')
        for quarter_idx in range(4 - min_data_quarter + 1):
                quarter_start = year_start + quarter_idx * self.months_per_quarter
                ax.text(quarter_start + self.months_per_quarter / 2, phase_ycords[-1] + 0.5, f'Q{min_data_quarter + quarter_idx}', ha='center', fontsize=10)
        
        # Все года
        for year_idx in range(1, total_years - 1):
            year_start = year_idx * self.quarters_per_year * self.months_per_quarter - self.offset_from_beginning
            year_end = year_start + self.quarters_per_year * self.months_per_quarter

            # Год
            ax.text((year_start + year_end) / 2, phase_ycords[-1] + 1, f'{self.min_date.year + year_idx}', ha='center', fontsize=12, fontweight='bold')

            # Кварталы
            for quarter_idx in range(self.quarters_per_year):
                quarter_start = year_start + quarter_idx * self.months_per_quarter 
                ax.text(quarter_start + self.months_per_quarter / 2, phase_ycords[-1] + 0.5, f'Q{quarter_idx + 1}', ha='center', fontsize=10)
                
        
        # Последний гоод
        year, max_data_quarter = self.get_quarter_from_date(self.max_date)

        year_start = (total_years - 1) * self.quarters_per_year * self.months_per_quarter - self.offset_from_beginning
        year_end = year_start + self.quarters_per_year * self.months_per_quarter
        ax.text((year_start + year_end) / 2, phase_ycords[-1] + 1, f'{self.min_date.year + total_years-1}', ha='center', fontsize=12, fontweight='bold')
        for quarter_idx in range(0, max_data_quarter):
                quarter_start = year_start + quarter_idx * self.months_per_quarter
                ax.text(quarter_start + self.months_per_quarter / 2, phase_ycords[-1] + 0.5, f'Q{quarter_idx + 1}', ha='center', fontsize=10)

        # Добавляем голубую полосу для текущего квартала
        current_date = datetime.now()
        current_year, current_quarter = current_date.year, (current_date.month - 1) // 3 + 1
        if self.min_date.year <= current_year <= self.max_date.year:
            current_quarter_start = self.getXCordByDate(current_date) - 1.5
            ax.add_patch(
                patches.Rectangle(
                    (current_quarter_start, -1),
                    self.months_per_quarter,
                    phase_ycords[-1] + 2,
                    color='lightblue',
                    alpha=0.3,
                    zorder=0
                )
            )

        # Настройка осей
        ax.set_yticks(phase_ycords)
        ax.set_yticklabels(phases)
        # TODO убрал ax.set_xticks(range(0, total_years * self.quarters_per_year * self.months_per_quarter + 1 - self.offset_from_beginning, self.months_per_quarter))
        ax.set_xticks([])
        ax.set_xticklabels([])

        # Удаление рамки графика
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Удаление сетки по оси Y
        ax.grid(axis='x', linestyle='--', alpha=0.7)

        
        handles = []

        for status, color in self.colors_veh.items():
            if status in self.active_status:
                handles.append(mlines.Line2D([], [], color=color, marker='D', linestyle='None',
                            markersize=10, label=self.names_veh[status]))
        # # TODO: переделать сразу с именами Добавляем легенду
        # complete = mlines.Line2D([], [], color='#63D16F', marker='D', linestyle='None',
        #                   markersize=10, label='Готово')
        # in_progress = mlines.Line2D([], [], color='#CCF3FF', marker='D', linestyle='None',
        #                         markersize=10, label='В работе')
        # freeze = mlines.Line2D([], [], color='#FFFFFF', marker='D', linestyle='None',
        #                         markersize=10, label='Не начат')


        plt.legend(handles=handles, loc='lower right', bbox_to_anchor=(0.02, 0.03), title='Статус вех', facecolor='lightgray')

        # Сохранение в буфер
        buffer = BytesIO()
        plt.tight_layout()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close(fig)

        return buffer

    def updatePeriod(self):
                pass # TODO: вытягивать из parentSystemEndDate 


#  quarter_start = (year - min_date.year) * self.quarters_per_year * self.months_per_quarter + (quarter - 1) * self.months_per_quarter # TODO может тут добавить получение квартала для миндате
#             temp = ""
#             for offset, milestone in enumerate(milestones):
#                 # x_position = quarter_start + self.months_per_quarter / 2 - offset * 0.3
    def getXCordByDate(self, date):
        year, quarter = self.get_quarter_from_date(date)
        x = (year - self.min_date.year) * self.quarters_per_year * self.months_per_quarter + (quarter - 1) * self.months_per_quarter+1.5 - self.offset_from_beginning
        return x
    
    def getLabelVeh(self, milestone):
        return "\n".join([
            ' ' + chr(111) + ' ' + self.wrap_text(milestone['nameProject']),
            'к $\\mathbf{' + milestone['systemEndDate'] + '}$',
            self.wrap_text(milestone['ownerName']),
        ])

    def setDataVeh(self, colors_veh = None, names_veh = None):
        """
        Задание цветов вехам
        {
        'status': 'color',
        ...
        }
        """
        if (colors_veh == None or names_veh == None):
            self.colors_veh = {
                'Complete': '#63d16f',
                'InWork': "#4f8ad8",
                'Freeze': '#CCF3FF',
                'Cancelled': '#f2f2f2',
                'NotStarted': '#ffffff',
                'Ready': '#f6b40e'
            }
            self.names_veh = {
                'Complete': 'Завершён',
                'InWork': "В работе",
                'Freeze': 'Отложен',
                'Cancelled': 'Отменён',
                'NotStarted': 'Не начат',
                'Ready': 'На проверке'
            }
            return
        self.colors_veh = colors_veh
        self.names_veh = names_veh
