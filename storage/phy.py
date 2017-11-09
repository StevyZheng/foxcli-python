# coding = utf-8
from libs.common import try_catch
import os
import json


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
	def print_loss_of_dword_sync_count(self):
		dict_loss_of_dword_sync_count = {}
		for key in self.phy_info_dict:
			dict_loss_of_dword_sync_count[key] = self.phy_info_dict[key]["loss_of_dword_sync_count"]
			print("%s:\n%s" % (key, self.phy_info_dict[key]["loss_of_dword_sync_count"]))
		return dict_loss_of_dword_sync_count

	@try_catch
	def print_invalid_dword_count(self):
		dict_invalid_dword_count = {}
		for key in self.phy_info_dict:
			dict_invalid_dword_count[key] = self.phy_info_dict[key]["invalid_dword_count"]
			print("%s:\n%s" % (key, self.phy_info_dict[key]["invalid_dword_count"]))
		return dict_invalid_dword_count

	@try_catch
	def print_running_disparity_error_count(self):
		dict_running_disparity_error_count = {}
		for key in self.phy_info_dict:
			dict_running_disparity_error_count[key] = self.phy_info_dict[key]["running_disparity_error_count"]
			print("%s:\n%s" % (key, self.phy_info_dict[key]["running_disparity_error_count"]))
		return dict_running_disparity_error_count

	@try_catch
	def print_all_errors(self):
		for key in self.phy_info_dict:
			if self.phy_info_dict[key]['loss_of_dword_sync_count'] != "0" or self.phy_info_dict[key][
				'invalid_dword_count'] != "0" or self.phy_info_dict[key]['running_disparity_error_count'] != "0":
				assert isinstance(key, str)
				print(
					u"{0:s}:\nloss_of_dword_sync_count:{1:s}\ninvalid_dword_count:{2:s}\nrunning_disparity_error_count:{3:s}\n".format(
						key, self.phy_info_dict[key]['loss_of_dword_sync_count'],
						self.phy_info_dict[key]['invalid_dword_count'],
						self.phy_info_dict[key]['running_disparity_error_count']))

	@try_catch
	def dict_to_json(self):
		json_str = json.dumps(self.phy_info_dict, indent=1)
		assert isinstance(json_str, str)
		return json_str
