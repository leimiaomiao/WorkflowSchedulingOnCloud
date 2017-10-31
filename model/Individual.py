from __future__ import division
from config import constant
import math
from model.Cloud import CloudVM


class IndividualTask(object):
    task = None
    exec_pos = None


class Individual(object):
    makespan = 0
    cost = 0
    reliability = 0
    individual_id = 0

    def __init__(self, algorithm, individual_id, workflow):
        self.individual_id = individual_id
        self.workflow = workflow
        self.individual_task_list = algorithm.init_task_list_order_pos()

    def print(self):
        for individual_task in self.individual_task_list:
            print(individual_task.task.task_id, individual_task.exec_pos)

    def print_results(self):
        print(self.individual_id, self.makespan, self.cost, self.reliability)

    def get_individual_task_by_id(self, _id):
        for individual_task in self.individual_task_list:
            if individual_task.task.task_id == _id:
                return individual_task

    # 整个工作流完工时间
    def calc_makespan(self):
        last_task = self.individual_task_list[len(self.individual_task_list) - 1]
        return last_task.task.end_time

    # 整个工作流完工的花费
    def calc_cost(self):
        cost = 0
        for individual_task in self.individual_task_list:
            cost += individual_task.task.cost
        return cost

    # 整个工作流完工的可靠性
    def calc_rel(self):
        rel = 1
        for individual_task in self.individual_task_list:
            rel += individual_task.task.reliability
        return rel

    @staticmethod
    def is_task_ready_to_exec(individual_task, finish_task_id_list):
        if len(individual_task.task.pre_task_id_list) == 0:
            return True

        for task_id in individual_task.task.pre_task_id_list:
            if task_id not in finish_task_id_list:
                return False

        return True

    def update(self, individual_task, cur_time):
        individual_task.task.start_time = cur_time
        individual_task.task.trans_time = self.get_trans_time(individual_task)
        individual_task.task.exec_time, cloud_vm = self.get_exec_time(individual_task)
        individual_task.task.end_time = cur_time + individual_task.task.trans_time + individual_task.task.exec_time
        individual_task.task.span_time = individual_task.task.trans_time + individual_task.task.exec_time + self.get_send_time(
            individual_task)
        individual_task.task.rent_time = individual_task.task.trans_time + individual_task.task.exec_time + self.get_send_time(
            individual_task)

        if cloud_vm.m == 1:
            individual_task.task.cost = math.ceil(individual_task.task.rent_time) * cloud_vm.cost_hourly
        elif cloud_vm.m == 2:
            individual_task.task.cost = individual_task.task.rent_time * cloud_vm.cost_hourly
        else:
            if individual_task.task.rent_time <= 1/6:
                individual_task.task.cost = 1/6 * cloud_vm.cost_hourly
            else:
                individual_task.task.cost = individual_task.task.rent_time * cloud_vm.cost_hourly

        individual_task.task.reliability = math.pow(math.e, -cloud_vm.lambda_m * individual_task.task.rent_time)

    def get_start_time(self, individual_task):
        start_time = 0
        for task_id in individual_task.task.pre_task_id_list:
            pre_task = self.get_individual_task_by_id(task_id).task
            wait_time = pre_task.output / constant.CLOUD_BANDWIDTH / 60 / 60
            time = wait_time + pre_task.end_time
            if time > start_time:
                start_time = time
        return start_time

    def get_trans_time(self, individual_task):
        output = 0
        for task_id in individual_task.task.pre_task_id_list:
            pre_task = self.get_individual_task_by_id(task_id).task
            output += pre_task.output
        return output / constant.CLOUD_BANDWIDTH / 60 / 60

    @staticmethod
    def get_exec_time(individual_task):
        m = int(individual_task.exec_pos / 5) + 1
        vm_type = individual_task.exec_pos % 5 + 1
        cloud_vm = CloudVM(m, vm_type)
        return individual_task.task.work_load / cloud_vm.compute_unit, cloud_vm

    @staticmethod
    def get_send_time(individual_task):
        send_time = individual_task.task.output * len(individual_task.task.suc_task_id_list) / constant.CLOUD_BANDWIDTH / 60 / 60
        return send_time

    def schedule(self):
        # 初始化云端待执行的任务列表
        cloud_task_list = list()
        for i in range(15):
            cloud_task_list.append(list())

        for individual_task in self.individual_task_list:
            cloud_task_list[individual_task.exec_pos].append(individual_task)

        # 已完成任务列表
        finish_task_id_list = list()

        # 任务调度
        while len(finish_task_id_list) < len(self.individual_task_list):
            for cloud_task in self.individual_task_list:
                if cloud_task not in finish_task_id_list and self.is_task_ready_to_exec(cloud_task,
                                                                                        finish_task_id_list):
                    cloud_cur_time = self.get_start_time(cloud_task)
                    self.update(cloud_task, cloud_cur_time)
                    finish_task_id_list.append(cloud_task.task.task_id)

        self.makespan = self.calc_makespan()
        self.cost = self.calc_cost()
        self.reliability = self.calc_rel()
