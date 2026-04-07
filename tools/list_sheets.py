from crm_manager import get_crm

crm = get_crm()
spreadsheet = crm._get_spreadsheet()

print("=== Spreadsheet に存在するシート ===")
for sheet in spreadsheet.worksheets():
    print(f"- {sheet.title}")
