import json

# registered_yachts.json 로드
with open('data/registered_yachts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 필터링: swan-41 제거, swan-48 중복 제거 (첫 번째만 유지)
yachts = data.get('yachts', [])
cleaned_yachts = []
swan48_added = False

for yacht in yachts:
    yacht_id = yacht.get('id')
    
    # swan-41 제외
    if yacht_id == 'swan-41':
        print(f"❌ 제거: swan-41 (48 owners manual로 잘못 등록됨)")
        continue
    
    # swan-48 첫 번째만 유지
    if yacht_id == 'swan-48':
        if not swan48_added:
            cleaned_yachts.append(yacht)
            swan48_added = True
            print(f"✅ 유지: swan-48 (첫 번째)")
        else:
            print(f"❌ 제거: swan-48 중복")
        continue
    
    # 나머지 추가
    cleaned_yachts.append(yacht)
    print(f"✅ 유지: {yacht_id}")

# 업데이트
data['yachts'] = cleaned_yachts
data['totalYachts'] = len(cleaned_yachts)
data['lastUpdated'] = '2025-12-01'

# 저장
with open('data/registered_yachts.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✅ 완료: {len(cleaned_yachts)}개 요트 남음")
