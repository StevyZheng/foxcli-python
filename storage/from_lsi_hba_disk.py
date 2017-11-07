# coding = utf-8
from libs.common import try_catch
from storage.disk import DiskAttr
from libs.common import Common
from setting import data_disk_model
import json


class SASChip:
	id = 0
	name = ""


class DiskFromLsiHBA:
	sas_chip_list = []
	disk_list = []
	disk_dict = {}

	@try_catch
	def __init__(self):
		re = Common.exe_shell("sas3ircu list|grep -P  'SAS[0-3]{2}08'").splitlines()
		sas_chip = SASChip()
		for i in re:
			sas_chip.id = Common.exe_shell("echo %s|awk '{print$1}'" % i).strip()
			sas_chip.name = Common.exe_shell("echo %s|awk '{print$2}'" % i).strip()
			self.sas_chip_list.append(sas_chip)
		disk_str_list = Common.exe_shell("lsscsi|grep %s" % data_disk_model).splitlines()
		for i in disk_str_list:
			disk_tmp = DiskAttr(i.split()[5])
			self.disk_list.append(disk_tmp)

	@try_catch
	def initialize(self):
		re = Common.exe_shell("sas3ircu list|grep -P  'SAS[0-3]{2}08'").splitlines()
		sas_chip = SASChip()
		for i in re:
			sas_chip.id = Common.exe_shell("echo %s|awk '{print$1}'" % i).strip()
			sas_chip.name = Common.exe_shell("echo %s|awk '{print$2}'" % i).strip()
			self.sas_chip_list.append(sas_chip)
		disk_str_list = Common.exe_shell("lsscsi|grep %s" % data_disk_model).splitlines()
		for i in disk_str_list:
			i.split()
			disk_tmp = DiskAttr(i[5])
			self.disk_list.append(disk_tmp)

	@try_catch
	def disk_list_to_dict(self):
		for disk_tmp in self.disk_list:
			self.disk_dict[disk_tmp.device_name] = disk_tmp.attr_to_dict()

	@try_catch
	def dict_to_json(self):
		self.disk_list_to_dict()
		json_str = json.dumps(self.disk_dict, indent=1)
		assert isinstance(json_str, str)
		return json_str
