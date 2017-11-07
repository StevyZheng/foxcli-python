# coding = utf-8
from storage.from_lsi_hba_disk import DiskFromLsiHBA
from storage.phy import Phy

phy = Phy()
hba = DiskFromLsiHBA()
phy.collect_phy_info()
hba.disk_list_to_dict()

print(hba.disk_list)
print(phy.dict_to_json())
