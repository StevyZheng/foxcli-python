# coding = utf-8
from storage.from_lsi_hba_disk import DiskFromLsiHBA


smart = DiskFromLsiHBA()
print(smart.dict_to_json())
