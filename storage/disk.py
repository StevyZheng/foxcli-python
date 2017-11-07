# coding = utf-8
from libs.common import try_catch
from libs.common import Common
import re


class Smart:
	device_name = ""
	attr_multi_list = []
	attr_list = []
	type = "SATA"

	@try_catch
	def __init__(self, device_name=""):
		self.device_name = device_name
		smart_tmp = Common.exe_shell("smartctl -a %s" % device_name)
		search_sata = re.search(r'SATA', smart_tmp, re.M)
		search_nvme = re.search(r'NVM', smart_tmp, re.M)
		search_sas = re.search(r'SAS', smart_tmp, re.M)
		if search_sata:
			self.type = "SATA"
			attr_tmp_list = re.findall(r'.*  0x.*-*', smart_tmp)
			#attr_tmp_list = Common.exe_shell("smartctl -A %s|grep -P '0x'" % self.device_name).splitlines()
			for i in attr_tmp_list:
				tmp = i.strip().split()
				self.attr_list.append(tmp[1].strip())
				self.attr_multi_list.append(tmp[:10])
		if search_nvme:
			self.type = "NVME"
		if search_sas:
			self.type = "SAS"

	@try_catch
	def smart_to_dict(self):
		dictb = {}
		if "SATA" in self.type:
			for i in self.attr_multi_list:
				in_dict = {
					"ID": i[0],
					"FLAG": i[2],
					"VALUE": i[3],
					"WORST": i[4],
					"THRESH": i[5],
					"TYPE": i[6],
					"UPDATED": i[7],
					"WHEN_FAILED": i[8],
					"RAW_VALUE": i[9]
				}
				dictb[i[1]] = in_dict
		elif "SAS" in self.type:
			pass
		assert isinstance(dictb, dict)
		return dictb


class DiskAttr:
	model = ""
	fw = ""
	sn = ""
	interface = ""
	device_name = ""
	from_chip = ""
	smart = None

	def __init__(self, devicename):
		self.device_name = devicename
		self.smart = Smart(self.device_name)
		smart_str = Common.exe_shell("smartctl -a %s" % self.device_name)
		lsscsi_str = Common.exe_shell("lsscsi|grep -P '%s *$'" % self.device_name)
		self.sn = Common.exe_shell("echo \"%s\"|grep 'Serial Number'|awk '{print$3}'" % smart_str).strip()
		self.model = Common.exe_shell("echo \"%s\"|awk '{print$4}'" % lsscsi_str).strip()
		self.fw = Common.exe_shell("echo \"%s\"|awk '{print$5}'" % lsscsi_str).strip()
		self.interface = Common.exe_shell("echo \"%s\"|awk '{print$3}'" % lsscsi_str).strip()

	@try_catch
	def attr_to_dict(self):
		dicta = {
			'model': self.model,
			'from_chip': self.from_chip,
			'fw': self.fw,
			'interface': self.interface,
			'sn': self.sn,
			'smart': self.smart.smart_to_dict()
		}
		assert isinstance(dicta, dict)
		return dicta
