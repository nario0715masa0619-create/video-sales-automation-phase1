from crm_manager import CRMManager

crm = CRMManager()
sheet = crm._get_sheet("Leads")

values = sheet.get_all_values()
print("=== Row 2 全カラム ===")
for i, cell in enumerate(values[1]):
    print(f"Col {i+1}: {cell}")
