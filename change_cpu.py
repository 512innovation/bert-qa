#!/usr/bin/env python
# Copyright 2014 Michael Rice
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Find VMs and change their cpuid.coresPerSocket value
"""

import requests
import time
from pyVmomi import vim
from tools import cli, service_instance, pchelper, tasks

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)

parser = cli.Parser()
parser.add_optional_arguments(cli.Argument.VM_NAME)
args = parser.get_args()
si = service_instance.connect(args)
content = si.RetrieveContent()
updated_vms=[]
while (True):
    vms = pchelper.get_all_obj(content, [vim.VirtualMachine])
    for vm in vms:
        if vm.name.startswith(args.vm_name) and \
            (vm.name not in updated_vms) and \
            (vm.summary.config.numCpu > 64):
            spec = vim.vm.ConfigSpec()
            opt = vim.option.OptionValue()
            spec.extraConfig = []
            opt.key = "cpuid.coresPerSocket"
            opt.value = "4"
            spec.extraConfig.append(opt)
            task = vm.ReconfigVM_Task(spec)
            tasks.wait_for_tasks(si, [task])
            updated_vms.append(vm.name)
            keys_and_vals = vm.config.extraConfig
            for opts in keys_and_vals:
                if opts.key == opt.key:
                    print("{0}: {1} => {2}".format(vm.name, opts.key, \
                        opts.value))
            time.sleep(5)

