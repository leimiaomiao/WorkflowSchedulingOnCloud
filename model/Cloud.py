class CloudVM(object):
    def __init__(self, provider_name, vm_type):
        self.provider_name = provider_name
        self.type = vm_type
        self.compute_unit, self.cost_hourly = self.read_cloud_file(provider_name, vm_type)

    @staticmethod
    def read_cloud_file(provider_name, vm_type):
        with open("../cloud_files/%s.txt" % provider_name, "r") as file:
            line = file.readline()
            while line:
                line = line.strip('\n')
                line_split = line.split(" ")
                if str(vm_type) == line_split[0]:
                    return float(line_split[1]), float(line_split[2])
                line = file.readline()
        return 0, 0

if __name__ == "__main__":
    cloudVM = CloudVM("microsoft", 2)
    print(cloudVM.compute_unit, cloudVM.cost_hourly)


