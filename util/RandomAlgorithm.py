from config import constant
from model.Individual import Individual, IndividualTask
import random
from util.ParetoAlgorithm import ParetoAlgorithm


class RandomAlgorithm(object):
    def __init__(self, workflow, rel_restraint, lambda_list):
        # 随机初始化种群
        self.individual_list = list()
        self.workflow = workflow
        self.name = "RANDOM"
        self.rel_restraint = rel_restraint

        i = 0
        while i < constant.RANDOM_TIME:
            individual = Individual(self, i, workflow, lambda_list)
            individual.schedule()
            if individual.reliability >= self.rel_restraint:
                self.individual_list.append(individual)
                i += 1

        self.max_id = len(self.individual_list) - 1

        # 初始化pareto解集
        self.pareto_result = ParetoAlgorithm.get_pareto_result(self.individual_list)

    def init_task_list_order_pos(self):
        # 任务排序初始化
        task_list_ordered = self.workflow.task_list

        # 任务位置初始化
        individual_task_list = list()
        for task in task_list_ordered:
            individual_task = IndividualTask()
            individual_task.task = task

            random_num = random.randrange(0, 150)
            individual_task.exec_pos = int(random_num / 10)

            individual_task_list.append(individual_task)
        return individual_task_list
