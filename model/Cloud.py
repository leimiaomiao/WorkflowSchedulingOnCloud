class CloudVM(object):
    provider_name_list = ["amazon", "google", "microsoft"]
    lambda_list_default = [0.001, 0.003, 0.002]

    def __init__(self, m, vm_type, lambda_list=lambda_list_default):
        self.m = int(m)
        self.provider_name = self.provider_name_list[self.m - 1]
        self.type = vm_type
        self.compute_unit, self.cost_hourly = self.read_cloud_file(self.provider_name, vm_type)
        self.lambda_list = lambda_list
        self.lambda_m = self.lambda_list[self.m - 1]

    @staticmethod
    def read_cloud_file(provider_name, vm_type):
        with open("cloud_files/%s.txt" % provider_name, "r") as file:
            line = file.readline()
            while line:
                line = line.strip('\n')
                line_split = line.split(" ")
                if str(vm_type) == line_split[0]:
                    return float(line_split[1]), float(line_split[2])
                line = file.readline()
        return 0, 0


if __name__ == "__main__":
    cloudVM = CloudVM(1, 2)
    print(cloudVM.compute_unit, cloudVM.cost_hourly)
