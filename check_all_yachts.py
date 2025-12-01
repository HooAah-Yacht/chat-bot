import json

print("=" * 80)
print("등록된 요트 목록 확인")
print("=" * 80)

# yacht_specifications.json
with open('data/yacht_specifications.json', 'r', encoding='utf-8') as f:
    specs = json.load(f)
    print(f"\n📋 yacht_specifications.json ({specs.get('totalYachts')}개):")
    for i, yacht in enumerate(specs.get('yachts', []), 1):
        name = yacht.get('name', 'Unknown')
        yacht_id = yacht.get('id', 'N/A')
        manual = yacht.get('manual') or yacht.get('manualPDF', 'N/A')
        print(f"  {i:2d}. {name:30s} (ID: {yacht_id:20s}) - {manual}")

# registered_yachts.json
print(f"\n📋 registered_yachts.json:")
with open('data/registered_yachts.json', 'r', encoding='utf-8') as f:
    reg = json.load(f)
    print(f"   Total: {reg.get('totalYachts')}개")
    for i, yacht in enumerate(reg.get('yachts', []), 1):
        yacht_id = yacht.get('id', 'N/A')
        basic = yacht.get('registrationData', {}).get('basicInfo', {})
        name = basic.get('name', 'Unknown')
        pdf = yacht.get('pdfFile', 'N/A')
        print(f"  {i:2d}. {name:30s} (ID: {yacht_id:20s}) - {pdf}")

print("\n" + "=" * 80)
