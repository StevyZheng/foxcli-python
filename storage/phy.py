# coding = utf-8
from libs.common import Common, try_catch
import os, json


class Phy:
	phy_path = "/sys/class/sas_phy"
	phy_name_list = []
	phy_list = []
	phy_info_dict = {}

	@try_catch
	def __init__(self):
		flag = os.path.exists(self.phy_path)
		if not flag:
			print("%s is not exist." % self.phy_path)
			return
		else:
			pass

	@try_catch
	def _list_phy(self):
		self.phy_name_list = os.listdir(self.phy_path)
		for i in self.phy_name_list:
			path = os.path.join(self.phy_path, i)
			self.phy_list.append(path)

	@try_catch
	def _read(self, filepath):
		with open(filepath) as fp:
			re = fp.read()
		return re

	@try_catch
	def collect_phy_info(self):
		self._list_phy()
		for phy_name_i in range(0, len(self.phy_name_list)):
			tmp = os.listdir(self.phy_list[phy_name_i])
			tmp_dict = {}
			for file_t in tmp:
				path_t = os.path.join(self.phy_list[phy_name_i], file_t)
				if os.path.exists(path_t) and os.path.isfile(path_t) and os.access(path_t, os.R_OK):
					if "reset" not in path_t:
						value = self._read(os.path.join(self.phy_list[phy_name_i], file_t)).strip()
						tmp_dict[file_t] = value
			self.phy_info_dict[self.phy_list[phy_name_i]] = tmp_dict

	@try_catch
	def dict_to_json(self):
		self.collect_phy_info()
		json_str = json.dumps(self.phy_info_dict, indent=1)
		assert isinstance(json_str, str)
		return json_str
