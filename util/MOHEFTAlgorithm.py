from model.Individual import Individual, IndividualTask
from config import constant
import copy
# from util.CrowdingDistanceAlgorithm import CrowdingDistanceAlgorithm
from util.ParetoAlgorithm import ParetoAlgorithm


class MOHEFTAlgorithm(object):
    def __init__(self, workflow, rel_restraint):
        self.name = "MOHEFT"
        self.workflow = workflow
        self.rel_restraint = rel_restraint

        self.individual = Individual(self, 0, workflow)
        self.pareto_result = list()

    def init_task_list_order_pos(self):
        # 任务排序初始化
        task_list_ordered = self.workflow.task_list

        # 任务位置初始化
        individual_task_list = list()

        for task in task_list_ordered:
            individual_task = IndividualTask()
            individual_task.task = task

            # 执行位置初始化为0
            individual_task.exec_pos = 0
            individual_task_list.append(individual_task)

        return individual_task_list

    @staticmethod
    def individual_select_by_reliability(individual_list, reliability):
        new_individual_list = []
        for individual in individual_list:
            if individual.calc_rel() <= reliability:
                new_individual_list.append(individual)

        return new_individual_list

    def process(self):
        k = constant.RANDOM_TIME

        # 记录当前的pareto列表，元素为一个individual_task的列表
        result = list()
        individual_id = 0

        for individual_task in self.individual.individual_task_list:
            task_temp_list = []
            for i in range(0, 15):
                task_temp = copy.deepcopy(individual_task)
                task_temp.exec_pos = i

                task_temp_list.append(task_temp)

            to_select_list = list()
            if len(result) > 0:
                for individual in result:
                    for i in range(0, 15):
                        individual_temp = copy.deepcopy(individual)
                        individual_temp.individual_id = individual_id
                        individual_temp.individual_task_list.append(task_temp_list[i])

                        individual_temp.schedule()
                        to_select_list.append(individual_temp)
                        individual_id += 1
            else:
                for i in range(0, 15):
                    individual_temp = copy.deepcopy(self.individual)
                    individual_temp.individual_id = individual_id
                    individual_temp.individual_task_list = [task_temp_list[i]]

                    individual_temp.schedule()
                    to_select_list.append(individual_temp)
                    individual_id += 1

            result = self.individual_select_by_reliability(to_select_list, self.rel_restraint)
            # crowding_distance_algorithm = CrowdingDistanceAlgorithm()
            # result = crowding_distance_algorithm.individual_select_by_crowding_distance(to_select_list, k)

        self.pareto_result = ParetoAlgorithm.get_pareto_result(result)

        # print(len(self.pareto_result))
        # for result in self.pareto_result:
        #     result.print()
        #     result.print_results()
        #     print("=============")
