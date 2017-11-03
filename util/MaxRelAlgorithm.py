from model.Individual import Individual, IndividualTask


class MaxRelAlgorithm(object):
    def __init__(self, workflow, lambda_list):
        # 随机初始化种群
        self.workflow = workflow
        self.name = "MaxRel"

        i = 0
        self.individual = Individual(self, i, workflow, lambda_list)

        self.rel = 0
        for pos in range(0, 15):
            self.individual.individual_task_list = self.init_task_list_order_pos_at(pos)
            self.individual.schedule()

            if self.rel < self.individual.calc_rel():
                self.rel = self.individual.calc_rel()

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

    def init_task_list_order_pos_at(self, pos):
        # 任务排序初始化
        task_list_ordered = self.workflow.task_list

        # 任务位置初始化
        individual_task_list = list()
        for task in task_list_ordered:
            individual_task = IndividualTask()
            individual_task.task = task
            individual_task.exec_pos = pos
            individual_task_list.append(individual_task)
        return individual_task_list
