from model.Individual import Individual, IndividualTask


class MaxRelAlgorithm(object):
    def __init__(self, workflow):
        # 随机初始化种群
        self.workflow = workflow
        self.name = "MaxRel"

        i = 0
        individual = Individual(self, i, workflow)
        individual.schedule()
        self.rel = individual.calc_rel()

    def init_task_list_order_pos(self):
        # 任务排序初始化
        task_list_ordered = self.workflow.task_list

        # 任务位置初始化
        individual_task_list = list()
        for task in task_list_ordered:
            individual_task = IndividualTask()
            individual_task.task = task
            individual_task.exec_pos = 4
            individual_task_list.append(individual_task)
        return individual_task_list
