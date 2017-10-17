from model.Task import Task
import copy
import random


class ClassicWorkflow(object):
    def __init__(self):
        self.task_list = []
        self.make_span = None
        self.cost = None
        self.reliability = None
        self.rel_constraint = None

    @property
    def task_list_length(self):
        return len(self.task_list)

    def get_task_by_id(self, _id):
        return self.task_list[_id]

    def print(self):
        for task in self.task_list:
            print(task.pre_task_id_list, task.task_id, task.suc_task_id_list)

    def create(self, workflow_type):
        task_dict = dict()
        file_path = "../../workflow_files/workflow%s/taskFile.txt" % workflow_type
        file = open(file_path, "r")
        line = file.readline()
        while line:
            # 首先去除换行符,真讨厌
            line = line.strip('\n')
            # 以空格分割一行,分割后的每一项都是task_id
            line_split = line.split(" ")

            # 如果当前task任务不在task_key_value中,那么new一个task
            for task_id in line_split:
                if task_id not in task_dict.keys():
                    task = Task(task_id, [], [])
                    task_dict[task_id] = task

            # 记录每一行的第一个task
            task = task_dict[line_split[0]]
            # 删除当前的task_id,那么剩余的line_split中的task都上它的后继
            line_split.pop(0)

            for task_id in line_split:
                task_temp = task_dict[task_id]
                task_temp.pre_task_id_list.append(task.task_id)
                task.suc_task_id_list.append(task_id)

            line = file.readline()

        task_dict = self.sort_dict_by_key(task_dict)
        # 最后按照int类型的key值进行排序
        self.task_list = list(task_dict.values())

    @staticmethod
    def sort_dict_by_key(task_dict):
        # 相当于把dict的key的类型从string转换成int
        new_key_list = []
        old_key_list = []
        new_dict = {}
        for key in task_dict.keys():
            old_key_list.append(key)
            new_key_list.append(int(key))

        key_list_len = len(new_key_list)
        for i in range(key_list_len):
            # 先加后删
            task_dict[new_key_list[i]] = task_dict[old_key_list[i]]
            task_dict.pop(old_key_list[i])

        while len(new_key_list) >= 1:
            # 按照key的值进行排序
            key_min = min(new_key_list)
            new_dict[key_min] = task_dict[key_min]
            new_key_list.remove(key_min)

        task_dict.clear()
        task_dict = new_dict
        return task_dict

    def init_task_order(self):
        # 第一个任务
        first_task = self.get_task_by_id(0)
        first_task_id = first_task.task_id

        # 已排好序的任务列表
        task_list_ordered = list()
        task_list_ordered.append(first_task_id)

        # 未排序的任务列表
        task_list = copy.deepcopy(self.task_list)
        task_list.remove(task_list[0])

        # 待排序的任务列表
        task_list_to_order = list()

        while len(self.task_list) != len(task_list_ordered):
            for task in task_list:
                if task.task_id not in task_list_ordered and task not in task_list_to_order:
                    pre_task_id_list = task.pre_task_id_list

                    available = True
                    for _id in pre_task_id_list:
                        if _id not in task_list_ordered:
                            available = False
                            break

                    if available:
                        task_list_to_order.append(task)

            i = random.randint(0, len(task_list_to_order) - 1)
            task_temp = task_list_to_order[i]
            task_list_ordered.append(task_temp.task_id)
            task_list_to_order.remove(task_temp)
        return task_list_ordered


if __name__ == "__main__":
    classicWorkflow = ClassicWorkflow()
    classicWorkflow.create(3)
    classicWorkflow.print()

    print(classicWorkflow.init_task_order())
