from __future__ import division
from model.Individual import Individual, IndividualTask
from config import constant
import copy
from util.CrowdingDistanceAlgorithm import CrowdingDistanceAlgorithm
from util.ParetoAlgorithm import ParetoAlgorithm


class MOHEFTAlgorithm(object):
    def __init__(self, workflow, rel_restraint, lambda_list):
        self.name = "MOHEFT"
        self.workflow = workflow
        self.rel_restraint = rel_restraint

        self.individual = Individual(self, 0, workflow, lambda_list)
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
    def individual_select_by_reliability(individual_list, rel_restraint):
        new_individual_list = []

        for individual in individual_list:
            if individual.reliability >= rel_restraint:
                new_individual_list.append(individual)

        return new_individual_list

    @staticmethod
    def sort_result_by_rel(result):
        return sorted(result, key=lambda individual: individual.calc_rel(), reverse=True)

    def process(self, max_rel_individual, max_rel):
        k = constant.PARETO_RESULT_NUM

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
                        last_task = individual_temp.individual_task_list[
                            len(individual_temp.individual_task_list) - 1].task
                        if last_task.reliability >= round(max_rel_individual.get_individual_task_by_id(
                                last_task.task_id).task.reliability * self.rel_restraint / max_rel, 8):
                            to_select_list.append(individual_temp)
                            individual_id += 1
            else:
                for i in range(0, 15):
                    individual_temp = copy.deepcopy(self.individual)
                    individual_temp.individual_id = individual_id
                    individual_temp.individual_task_list = [task_temp_list[i]]

                    individual_temp.schedule()
                    last_task = individual_temp.individual_task_list[len(individual_temp.individual_task_list) - 1].task
                    if last_task.reliability >= round(max_rel_individual.get_individual_task_by_id(
                            last_task.task_id).task.reliability * self.rel_restraint / max_rel, 8):
                        to_select_list.append(individual_temp)
                        individual_id += 1

            to_select_list = ParetoAlgorithm.get_pareto_result(to_select_list)
            crowding_distance_algorithm = CrowdingDistanceAlgorithm()
            result = crowding_distance_algorithm.individual_select_by_crowding_distance(to_select_list, k)

        self.pareto_result = ParetoAlgorithm.get_pareto_result(self.individual_select_by_reliability(result, self.rel_restraint))
