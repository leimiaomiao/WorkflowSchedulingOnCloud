from util.GeneticAlgorithm import GeneticAlgorithm
from util.MOHEFTAlgorithm import MOHEFTAlgorithm
from util.EvaluationMetric import EvaluationMetric
from util.RandomAlgorithm import RandomAlgorithm
from util.MinRelAlgorithm import MinRelAlgorithm
from util.MaxRelAlgorithm import MaxRelAlgorithm
from util.FileUtil import FileUtil
from model.workflow.ClassicWorkflow import ClassicWorkflow
from model.workflow.RandomWorkflow import RandomWorkflow
from config import constant


def sort_result_by_makespan(result):
    return sorted(result, key=lambda individual: individual.makespan)


if __name__ == "__main__":
    if True:
        # 初始化一个工作流
        # workflow = RandomWorkflow()
        # workflow.create(constant.TASK_NUM)
        workflow = ClassicWorkflow()
        workflow.create(1)
        workflow.print()

        minRelAlgorithm = MinRelAlgorithm(workflow)
        min_rel = minRelAlgorithm.rel
        print(min_rel)

        maxRelAlgorithm = MaxRelAlgorithm(workflow)
        max_rel = maxRelAlgorithm.rel
        print(max_rel)

        rel_restraint = min_rel + constant.PERCENTAGE * (max_rel - min_rel)

        # RANDOM算法
        randomAlgorithm = RandomAlgorithm(workflow, rel_restraint)
        random_result_sort_by_makespan = sort_result_by_makespan(randomAlgorithm.pareto_result)
        FileUtil.dump_result_to_file(random_result_sort_by_makespan, randomAlgorithm.name, workflow.name)

        # MOHEFT算法
        moheftAlgorithm = MOHEFTAlgorithm(workflow, rel_restraint)
        moheftAlgorithm.process()
        moheft_result_sort_by_makespan = sort_result_by_makespan(moheftAlgorithm.pareto_result)
        FileUtil.dump_result_to_file(moheft_result_sort_by_makespan, moheftAlgorithm.name, workflow.name)

        # MOWS-DTM算法
        mowsDtmAlgorithm = GeneticAlgorithm(workflow, rel_restraint)
        mowsDtmAlgorithm.process()
        mows_dtm_result_sort_by_makespan = sort_result_by_makespan(mowsDtmAlgorithm.pareto_result)
        FileUtil.dump_result_to_file(mows_dtm_result_sort_by_makespan, mowsDtmAlgorithm.name, workflow.name)

        metric_result = list()

        # Q-metric
        evaluation = EvaluationMetric()
        metric_result.append(evaluation.q_metric(randomAlgorithm.pareto_result, moheftAlgorithm.pareto_result))
        metric_result.append(evaluation.q_metric(randomAlgorithm.pareto_result, mowsDtmAlgorithm.pareto_result))
        metric_result.append(evaluation.q_metric(moheftAlgorithm.pareto_result, mowsDtmAlgorithm.pareto_result))

        # FS-metric
        metric_result.append(evaluation.fs_metric(randomAlgorithm.pareto_result))
        metric_result.append(evaluation.fs_metric(moheftAlgorithm.pareto_result))
        metric_result.append(evaluation.fs_metric(mowsDtmAlgorithm.pareto_result))

        # S-metric
        metric_result.append(evaluation.s_metric(randomAlgorithm.pareto_result))
        metric_result.append(evaluation.s_metric(moheftAlgorithm.pareto_result))
        metric_result.append(evaluation.s_metric(mowsDtmAlgorithm.pareto_result))

        FileUtil.dump_metric_result_to_file(
            metric_result,
            "%s_%s_%s_%s" % (workflow.name, randomAlgorithm.name, mowsDtmAlgorithm.name, moheftAlgorithm.name)
        )

        # if len(mowsDtmAlgorithm.pareto_result) >= 10:
        #     break
