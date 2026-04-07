from crm_manager import CRMManager

crm = CRMManager()
sheet = crm._get_sheet("Leads")

values = sheet.get_all_values()
print("=== 最初の 3 行（全カラム） ===")
for i, row in enumerate(values[:3]):
    print(f"Row {i+1}:")
    for j, cell in enumerate(row[:12]):
        print(f"  Col {j+1}: {cell}")
    print()
