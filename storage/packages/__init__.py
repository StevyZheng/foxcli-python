# coding = utf-8
import os
from libs.common import Common
from setting import DIR


def storage_install_packages():
	return Common.install_rpm(os.path.join(DIR, "storage", "packages", "*.rpm"))
