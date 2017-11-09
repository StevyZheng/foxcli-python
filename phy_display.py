# coding = utf-8
from storage.phy import Phy

phy = Phy()
phy.collect_phy_info()
print(phy.print_all_errors())
