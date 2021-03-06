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
        workflow = RandomWorkflow()
        workflow.create(constant.TASK_NUM)
        # workflow = ClassicWorkflow()
        # workflow.create(2)
        workflow.print()

        # for lambda_list in [[0, 0.003, 0.002], [0.001, 0, 0.002], [0.001, 0.003, 0]]:
        for lambda_list in [[0.001, 0.003, 0.002]]:

            minRelAlgorithm = MinRelAlgorithm(workflow, lambda_list)
            min_rel = minRelAlgorithm.rel
            print("最小可靠度是: %s" % min_rel)

            maxRelAlgorithm = MaxRelAlgorithm(workflow, lambda_list)
            max_rel = maxRelAlgorithm.rel
            print("最大可靠度是: %s" % max_rel)

            for percentage in [0.2, 0.4, 0.6, 0.8]:
            # for percentage in [0.5]:
                rel_restraint = min_rel + percentage * (max_rel - min_rel)
                print("可靠度下限是: %s" % rel_restraint)

                print("Random")
                # RANDOM算法
                randomAlgorithm = RandomAlgorithm(workflow, rel_restraint, lambda_list)
                random_result_sort_by_makespan = sort_result_by_makespan(randomAlgorithm.pareto_result)
                FileUtil.dump_result_to_file(random_result_sort_by_makespan, randomAlgorithm.name, workflow.name,
                                             percentage)

                print("mows")
                # MOWS算法
                mowsDtmAlgorithm = GeneticAlgorithm(workflow, rel_restraint, lambda_list)
                mowsDtmAlgorithm.process()
                mows_dtm_result_sort_by_makespan = sort_result_by_makespan(mowsDtmAlgorithm.pareto_result)
                FileUtil.dump_result_to_file(mows_dtm_result_sort_by_makespan, mowsDtmAlgorithm.name, workflow.name,
                                             percentage)

                print("Moheft")
                # MOHEFT算法
                moheftAlgorithm = MOHEFTAlgorithm(workflow, rel_restraint, lambda_list)
                moheftAlgorithm.process(maxRelAlgorithm.individual, max_rel)
                moheft_result_sort_by_makespan = sort_result_by_makespan(moheftAlgorithm.pareto_result)
                FileUtil.dump_result_to_file(moheft_result_sort_by_makespan, moheftAlgorithm.name, workflow.name,
                                             percentage)
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
                    "%s_%s_%s_%s_%s" % (
                        workflow.name, randomAlgorithm.name, mowsDtmAlgorithm.name, moheftAlgorithm.name, percentage)
                )

                # if len(mowsDtmAlgorithm.pareto_result) >= 10:
                #     break
