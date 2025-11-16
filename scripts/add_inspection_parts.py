# -*- coding: utf-8 -*-
"""
이미지 정비 자료 기반 실질적인 부품 점검 항목 추가
"""
import json
from pathlib import Path

def create_comprehensive_parts_data():
    """이미지 기반 실제 점검 항목 데이터"""
    
    # 1. 선체(Hull) 상태 점검
    hull_parts = [
        {
            "id": "hull-001",
            "partNumber": "HULL-INSPECT-001",
            "name": "Hull Damage Inspection",
            "nameKo": "선체 손상 점검",
            "category": "hull",
            "inspectionItems": [
                "외관 손상, 삼투, 겔코트 크랙",
                "도장 상태 (선저도색 Antifouling Paint)",
                "선저 전해부식 (Electrolysis) 점검"
            ],
            "checkInterval": "매년 / 항해 후",
            "repairMethod": "크랙 보수, 겔코트 수리, 선저도색",
            "material": "Fiberglass, Gelcoat",
            "corrosionRisk": "높음 - 해수 접촉",
            "maintenanceLevel": "전문가",
            "estimatedCost": "$500-2000"
        },
        {
            "id": "hull-002",
            "partNumber": "KEEL-001",
            "name": "Keel",
            "nameKo": "킬 / 선저",
            "category": "hull",
            "inspectionItems": [
                "킬 볼트 체결 상태",
                "킬-선체 연결부 누수",
                "킬 표면 부식"
            ],
            "checkInterval": "1년",
            "material": "Lead/Iron",
            "corrosionRisk": "매우 높음",
            "maintenanceLevel": "전문가",
            "estimatedCost": "$1000-5000"
        },
        {
            "id": "hull-003",
            "partNumber": "RUDDER-001",
            "name": "Rudder",
            "nameKo": "러더 / 키",
            "category": "hull",
            "inspectionItems": [
                "러더 베어링 마모",
                "러더 스톡 부식",
                "러더 블레이드 손상"
            ],
            "checkInterval": "6개월",
            "repairMethod": "베어링 교체, 부식 연마, 도색",
            "corrosionRisk": "높음",
            "maintenanceLevel": "전문가"
        }
    ]
    
    # 2. 리깅(Rigging) 점검
    rigging_parts = [
        {
            "id": "rig-001",
            "partNumber": "STAND-RIG-001",
            "name": "Standing Rigging - Stays & Shrouds",
            "nameKo": "고정 리깅 - 스테이/슈라우드",
            "category": "rigging",
            "inspectionItems": [
                "스테이 부식 점검 (스테인리스 강)",
                "터nбуकल 장력 확인",
                "마스트 헤드 핀/스프레더 부근 균열",
                "턴버클 코터 핀 확인"
            ],
            "checkInterval": "6개월 / 폭풍 후",
            "material": "Stainless Steel 316",
            "corrosionRisk": "중간 - 스테인리스 부식 (Crevice Corrosion)",
            "failureConsequence": "매우 심각 - 마스트 붕괴",
            "repairMethod": "와이어 교체, 터nбуकल 조정",
            "estimatedCost": "$2000-8000",
            "maintenanceLevel": "전문가"
        },
        {
            "id": "rig-002",
            "partNumber": "RUN-RIG-001",
            "name": "Running Rigging - Halyards & Sheets",
            "nameKo": "가변 리깅 - 할야드/시트",
            "category": "rigging",
            "inspectionItems": [
                "할야드 마모 점검",
                "시트 로프 끝부분 손상",
                "블록 내부 스웰 확인"
            ],
            "checkInterval": "3개월",
            "material": "Polyester / Dyneema",
            "repairMethod": "로프 교체",
            "estimatedCost": "$200-1000"
        },
        {
            "id": "rig-003",
            "partNumber": "MAST-001",
            "name": "Mast",
            "nameKo": "마스트",
            "category": "rigging",
            "inspectionItems": [
                "마스트 알루미늄 부식",
                "마스트 스텝 볼트 체결",
                "전기 배선 상태"
            ],
            "checkInterval": "1년",
            "material": "Aluminum Alloy",
            "corrosionRisk": "중간",
            "maintenanceLevel": "전문가"
        }
    ]
    
    # 3. 세일(Sail) 관리
    sail_parts = [
        {
            "id": "sail-001",
            "partNumber": "MAIN-SAIL-001",
            "name": "Mainsail",
            "nameKo": "메인세일",
            "category": "sails",
            "inspectionItems": [
                "봉제선 손상, 자외선 손상 여부",
                "UV 커버 찢김",
                "스티치 풀림",
                "패치부 마모"
            ],
            "checkInterval": "3개월 / 레이스 후",
            "repairMethod": "봉제 보수, 패치 추가",
            "material": "Dacron / Mylar / Laminate",
            "estimatedCost": "$500-3000 (교체 시)"
        },
        {
            "id": "sail-002",
            "partNumber": "GENOA-001",
            "name": "Genoa / Jib",
            "nameKo": "제노아 / 집",
            "category": "sails",
            "inspectionItems": [
                "리치 라인 장력",
                "클루 부분 봉제선",
                "UV 스트립 상태"
            ],
            "checkInterval": "3개월",
            "repairMethod": "봉제 보수"
        }
    ]
    
    # 4. 엔진 및 추진 시스템 (이미지 기반 10개 항목)
    engine_parts = [
        {
            "id": "eng-001",
            "partNumber": "ENG-OIL-001",
            "name": "Engine Oil",
            "nameKo": "엔진오일",
            "category": "engine",
            "inspectionItems": [
                "오일 색 (검은 컬러 → 교체)",
                "점도 확인",
                "레벨 게이지 확인"
            ],
            "checkInterval": "100~150시간 운항 / 1년",
            "repairMethod": "오일필터와 동시에 교체",
            "material": "Mineral/Synthetic Oil",
            "estimatedCost": "$50-150"
        },
        {
            "id": "eng-002",
            "partNumber": "GEAR-OIL-001",
            "name": "Gear Oil / Saildrive Oil",
            "nameKo": "기어오일 / 세일드라이브 오일",
            "category": "engine",
            "inspectionItems": [
                "색이 유백 ( )색이면 수분 혼입 → 가스킷 교체",
                "드레인에 마그넷에 금속분 확인"
            ],
            "checkInterval": "1년 / 200시간",
            "repairMethod": "드레인 가스켓 교체 필수",
            "estimatedCost": "$80-200"
        },
        {
            "id": "eng-003",
            "partNumber": "IMPELLER-001",
            "name": "Impeller",
            "nameKo": "임펠러",
            "category": "engine",
            "inspectionItems": [
                "냉각수 흐름",
                "고무 블레이드 마모·변형·균열 여부"
            ],
            "checkInterval": "매 시즌 (1년)",
            "repairMethod": "예비품 항상 보유",
            "corrosionRisk": "낮음 - 고무",
            "estimatedCost": "$30-80"
        },
        {
            "id": "eng-004",
            "partNumber": "V-BELT-001",
            "name": "V-Belt / Serpentine Belt",
            "nameKo": "V벨트 / 서펀타인 벨트",
            "category": "engine",
            "inspectionItems": [
                "장력 확인",
                "마모·균열 확인"
            ],
            "checkInterval": "1~2년",
            "repairMethod": "예비벨트 보관 권장",
            "estimatedCost": "$20-50"
        },
        {
            "id": "eng-005",
            "partNumber": "FUEL-FILTER-001",
            "name": "Fuel Filter",
            "nameKo": "연료필터",
            "category": "engine",
            "inspectionItems": [
                "필터 색·슬러지·수분 여부 확인"
            ],
            "checkInterval": "200시간 / 매년",
            "repairMethod": "워터 세퍼레이터 동시 확인",
            "estimatedCost": "$15-40"
        },
        {
            "id": "eng-006",
            "partNumber": "OIL-FILTER-001",
            "name": "Oil Filter",
            "nameKo": "오일필터",
            "category": "engine",
            "inspectionItems": [
                "엔진오일 교체 시 동시 교체"
            ],
            "checkInterval": "오일 교체 주기 동일",
            "repairMethod": "필터캔 가스켓 확인",
            "estimatedCost": "$10-30"
        },
        {
            "id": "eng-007",
            "partNumber": "AIR-FILTER-001",
            "name": "Air Filter",
            "nameKo": "에어필터",
            "category": "engine",
            "inspectionItems": [
                "먼지, 염분, 오일오염 여부"
            ],
            "checkInterval": "매 시즌 / 필요 시",
            "repairMethod": "세척형 또는 교체형",
            "estimatedCost": "$20-60"
        },
        {
            "id": "eng-008",
            "partNumber": "COOLANT-001",
            "name": "Coolant",
            "nameKo": "냉각수",
            "category": "engine",
            "inspectionItems": [
                "부동액 농도, 색, 누수 확인"
            ],
            "checkInterval": "2년 / 500시간",
            "repairMethod": "해수펌프와 별개 시스템",
            "estimatedCost": "$30-80"
        },
        {
            "id": "eng-009",
            "partNumber": "ALTERNATOR-001",
            "name": "Alternator",
            "nameKo": "배터리 충전계",
            "category": "engine",
            "inspectionItems": [
                "충전전압(13.8~14.2V), 벨트 슬립 여부"
            ],
            "checkInterval": "6개월",
            "repairMethod": "전기식 부식 방지 중요",
            "estimatedCost": "$200-500"
        },
        {
            "id": "eng-010",
            "partNumber": "EXHAUST-001",
            "name": "Exhaust System",
            "nameKo": "배기라인",
            "category": "engine",
            "inspectionItems": [
                "소음 결함·누수·스름 여부"
            ],
            "checkInterval": "1년",
            "repairMethod": "머플러·호스·클램프 점검",
            "corrosionRisk": "매우 높음 - 염수 접촉",
            "estimatedCost": "$200-800"
        }
    ]
    
    # 5. 전기 시스템
    electrical_parts = [
        {
            "id": "elec-001",
            "partNumber": "BATTERY-001",
            "name": "Batteries",
            "nameKo": "배터리",
            "category": "electrical",
            "inspectionItems": [
                "전압 체크",
                "단자 부식",
                "방수상태"
            ],
            "checkInterval": "3개월",
            "corrosionRisk": "높음 - 전해부식",
            "estimatedCost": "$200-800"
        }
    ]
    
    # 6. 조타장치(Steering) - 이미지 기반 10개 항목
    steering_parts = [
        {
            "id": "steer-001",
            "partNumber": "HELM-WHEEL-001",
            "name": "Helm Wheel",
            "nameKo": "조타휠",
            "category": "steering",
            "inspectionItems": [
                "스포크, 허브, 샤프트 결합",
                "유격, 부식, 스플라인 마모"
            ],
            "checkInterval": "6개월 / 항해 후",
            "repairMethod": "볼트 재체결, 스플라인 그리스",
            "estimatedCost": "$200-1000"
        },
        {
            "id": "steer-002",
            "partNumber": "CHAIN-CABLE-001",
            "name": "Chain & Cable",
            "nameKo": "체인 및 케이블",
            "category": "steering",
            "inspectionItems": [
                "텐션, 운활, 와이어 마모",
                "장력 동일한지, 녹/갈라짐 확인"
            ],
            "checkInterval": "6개월",
            "corrosionRisk": "중간",
            "repairMethod": "와이어 재설정/교체",
            "estimatedCost": "$300-800"
        },
        {
            "id": "steer-003",
            "partNumber": "QUADRANT-001",
            "name": "Quadrant",
            "nameKo": "쿼드런트",
            "category": "steering",
            "inspectionItems": [
                "케이블 고정, 볼트 풀림",
                "조타 전체 범위에서 이상음 여부"
            ],
            "checkInterval": "6개월",
            "maintenanceLevel": "전문가",
            "estimatedCost": "$400-1200"
        },
        {
            "id": "steer-004",
            "partNumber": "RUDDER-STOCK-001",
            "name": "Rudder Stock",
            "nameKo": "러더축",
            "category": "steering",
            "inspectionItems": [
                "상·하 베어링, 마모, 루즈",
                "러더를 좌우로 흔들며 유격 측정"
            ],
            "checkInterval": "1년 / 육상거치 시",
            "corrosionRisk": "높음",
            "maintenanceLevel": "전문가",
            "estimatedCost": "$500-2000"
        },
        {
            "id": "steer-005",
            "partNumber": "RUDDER-BLADE-001",
            "name": "Rudder Blade",
            "nameKo": "러더 블레이드",
            "category": "steering",
            "inspectionItems": [
                "크랙, 물 흡수, 페인트 상태",
                "탭핑(손가락 두드림)으로 내부공동 확인 매년"
            ],
            "checkInterval": "매년",
            "repairMethod": "수지 주입, 도색",
            "estimatedCost": "$300-1500"
        },
        {
            "id": "steer-006",
            "partNumber": "HYD-PUMP-001",
            "name": "Hydraulic Pump (Hydraulic Type)",
            "nameKo": "유압펌프 (유압식)",
            "category": "steering",
            "inspectionItems": [
                "오일 누유, 밸브 작동",
                "누유 흔적, 핸들 감도 확인"
            ],
            "checkInterval": "1년",
            "maintenanceLevel": "전문가",
            "estimatedCost": "$800-2500"
        },
        {
            "id": "steer-007",
            "partNumber": "HYD-CYLINDER-001",
            "name": "Hydraulic Cylinder",
            "nameKo": "유압 실린더",
            "category": "steering",
            "inspectionItems": [
                "로드 부식, 실 누유",
                "실린더 끝단 오일자국 유무"
            ],
            "checkInterval": "6개월",
            "corrosionRisk": "높음",
            "estimatedCost": "$400-1200"
        },
        {
            "id": "steer-008",
            "partNumber": "TILLER-ARM-001",
            "name": "Tiller Arm (Tiller Type)",
            "nameKo": "틸러 연결부",
            "category": "steering",
            "inspectionItems": [
                "핀, 힌지, 볼트",
                "급속마모, 루즈 여부"
            ],
            "checkInterval": "3개월",
            "repairMethod": "볼트 재체결",
            "estimatedCost": "$50-200"
        },
        {
            "id": "steer-009",
            "partNumber": "END-STOP-001",
            "name": "Stopper / End Stop",
            "nameKo": "조타제한장치",
            "category": "steering",
            "inspectionItems": [
                "작동 한계점에서 고정 여부",
                "좌우 끝단에서 스토퍼 작동 확인"
            ],
            "checkInterval": "1년",
            "estimatedCost": "$100-300"
        },
        {
            "id": "steer-010",
            "partNumber": "AUTOPILOT-LINK-001",
            "name": "Autopilot Connection",
            "nameKo": "오토파일럿 연결부",
            "category": "steering",
            "inspectionItems": [
                "드라이브 유닛, 피드백 센서",
                "연결 핀 풀림, 피드백 작동"
            ],
            "checkInterval": "6개월",
            "maintenanceLevel": "전문가",
            "estimatedCost": "$300-1000"
        }
    ]
    
    # 7. 빌지 및 배수 (이미지 기반 10개 항목)
    bilge_parts = [
        {
            "id": "bilge-001",
            "partNumber": "BILGE-PUMP-AUTO-001",
            "name": "Auto Bilge Pump",
            "nameKo": "자동 펌프 작동 여부",
            "category": "plumbing",
            "inspectionItems": [
                "수동/자동 모두 작동 확인",
                "바튼 또는 수위 상등 테스트"
            ],
            "checkInterval": "매월",
            "repairMethod": "스위치 교체",
            "estimatedCost": "$80-250"
        },
        {
            "id": "bilge-002",
            "partNumber": "FLOAT-SWITCH-001",
            "name": "Float Switch",
            "nameKo": "플로트 스위치",
            "category": "plumbing",
            "inspectionItems": [
                "작동 시 자동 시동 여부 확인",
                "손으로 플로트 들어올려 확인"
            ],
            "checkInterval": "매월",
            "estimatedCost": "$20-60"
        },
        {
            "id": "bilge-003",
            "partNumber": "RELAY-001",
            "name": "Relay",
            "nameKo": "전원/퓨즈/릴레이",
            "category": "plumbing",
            "inspectionItems": [
                "전원 공급 확인, 배선 부식",
                "멀티미터로 전압체크"
            ],
            "checkInterval": "3개월",
            "corrosionRisk": "높음",
            "estimatedCost": "$10-50"
        },
        {
            "id": "bilge-004",
            "partNumber": "HOSE-VALVE-001",
            "name": "Hose & Valve",
            "nameKo": "호스 및 밸브",
            "category": "plumbing",
            "inspectionItems": [
                "누수·역류·끼임 여부",
                "호스 연결부 시각점검"
            ],
            "checkInterval": "6개월",
            "repairMethod": "클램프 재체결",
            "estimatedCost": "$30-100"
        },
        {
            "id": "bilge-005",
            "partNumber": "CHECK-VALVE-001",
            "name": "Check Valve (Non-return Valve)",
            "nameKo": "체크밸브(역류방지)",
            "category": "plumbing",
            "inspectionItems": [
                "밸브 막힘 여부",
                "분리 후 통수확인"
            ],
            "checkInterval": "1년",
            "repairMethod": "청소 또는 교체",
            "estimatedCost": "$25-80"
        },
        {
            "id": "bilge-006",
            "partNumber": "THROUGH-HULL-001",
            "name": "Through-hull",
            "nameKo": "배출구(Through-hull)",
            "category": "plumbing",
            "inspectionItems": [
                "막힘, 조개류 부착 여부",
                "외부에서 시각 점검"
            ],
            "checkInterval": "1년",
            "corrosionRisk": "매우 높음",
            "maintenanceLevel": "전문가",
            "estimatedCost": "$50-200"
        },
        {
            "id": "bilge-007",
            "partNumber": "MANUAL-PUMP-001",
            "name": "Manual Pump",
            "nameKo": "수동펌프 작동",
            "category": "plumbing",
            "inspectionItems": [
                "손잡이, 밸브, 다이아프램 상태",
                "물통으로 테스트"
            ],
            "checkInterval": "6개월",
            "estimatedCost": "$80-200"
        },
        {
            "id": "bilge-008",
            "partNumber": "BILGE-CLEAN-001",
            "name": "Bilge Cleaning",
            "nameKo": "빌지 클리닝",
            "category": "plumbing",
            "inspectionItems": [
                "염분, 오일, 쓰레기 제거",
                "세척·건조"
            ],
            "checkInterval": "3개월",
            "repairMethod": "흡수패드 사용",
            "estimatedCost": "$0-50 (자가)"
        },
        {
            "id": "bilge-009",
            "partNumber": "BATTERY-CHECK-001",
            "name": "Battery Voltage Check",
            "nameKo": "배터리 연결 상태",
            "category": "plumbing",
            "inspectionItems": [
                "부식, 느슨한 터미널 확인",
                "방청제 도포"
            ],
            "checkInterval": "6개월",
            "corrosionRisk": "높음",
            "estimatedCost": "$10-30"
        },
        {
            "id": "bilge-010",
            "partNumber": "SPARE-PUMP-001",
            "name": "Spare Pump",
            "nameKo": "예비 펌프 확인",
            "category": "plumbing",
            "inspectionItems": [
                "예비품 보유, 휴대용 작동 확인",
                "테스트 구동"
            ],
            "checkInterval": "1년",
            "estimatedCost": "$100-300"
        }
    ]
    
    # 8. 안전장비
    safety_parts = [
        {
            "id": "safe-001",
            "partNumber": "LIFEJACKET-001",
            "name": "Life Jackets",
            "nameKo": "구명조끼",
            "category": "safety",
            "inspectionItems": [
                "플레어, 소화기, EPIRB, 소화기",
                "유효기간, 작동여부, 배치상태"
            ],
            "checkInterval": "매년 / 출항 전",
            "repairMethod": "유효기간 점검",
            "estimatedCost": "$50-300"
        },
        {
            "id": "safe-002",
            "partNumber": "LIFERAFT-001",
            "name": "Life Raft",
            "nameKo": "구명보트",
            "category": "safety",
            "inspectionItems": [
                "항해 규정에 맞춘 장비 인증 갱신"
            ],
            "checkInterval": "매년",
            "maintenanceLevel": "전문가",
            "estimatedCost": "$300-1000 (점검)"
        }
    ]
    
    # 9. 데크 및 하드웨어 (이미지 기반 10개 항목)
    deck_parts = [
        {
            "id": "deck-001",
            "partNumber": "WINCH-001",
            "name": "Winch",
            "nameKo": "윈치",
            "category": "winches",
            "inspectionItems": [
                "기어, 드럼, 라쳇, 스프링",
                "회전 부드러움, 잠음, 윤활상태"
            ],
            "checkInterval": "6개월 / 레이스 후",
            "repairMethod": "분해·청소·그리스",
            "corrosionRisk": "높음",
            "estimatedCost": "$200-800"
        },
        {
            "id": "deck-002",
            "partNumber": "BLOCK-001",
            "name": "Block",
            "nameKo": "블록",
            "category": "blocks",
            "inspectionItems": [
                "풀리, 베어링, 사클",
                "회전저항, 균열, 부식"
            ],
            "checkInterval": "6개월",
            "repairMethod": "교체",
            "estimatedCost": "$50-300"
        },
        {
            "id": "deck-003",
            "partNumber": "CLEAT-001",
            "name": "Cleat",
            "nameKo": "클리트 / 잼클리트",
            "category": "deck",
            "inspectionItems": [
                "고정력, 볼트풀림, 마모",
                "로프 슬립여부"
            ],
            "checkInterval": "1년",
            "estimatedCost": "$30-150"
        },
        {
            "id": "deck-004",
            "partNumber": "TRACK-CAR-001",
            "name": "Track & Car",
            "nameKo": "트랙 / 카",
            "category": "deck",
            "inspectionItems": [
                "트랙 볼트, 이동저항",
                "슬라이드 자유이동 여부"
            ],
            "checkInterval": "6개월",
            "repairMethod": "윤활, 볼트 재체결",
            "estimatedCost": "$100-500"
        },
        {
            "id": "deck-005",
            "partNumber": "SHACKLE-PIN-001",
            "name": "Shackle & Pin",
            "nameKo": "사클 / 핀류",
            "category": "deck",
            "inspectionItems": [
                "부식, 변형, 스냅링 손상",
                "손으로 개폐 테스트"
            ],
            "checkInterval": "6개월",
            "corrosionRisk": "높음",
            "estimatedCost": "$10-80"
        },
        {
            "id": "deck-006",
            "partNumber": "STANCHION-001",
            "name": "Stanchion / Pulpit",
            "nameKo": "스탠션 / 풀핏",
            "category": "deck",
            "inspectionItems": [
                "용접부 균열, 볼트풀림",
                "흔들림 여부, 녹"
            ],
            "checkInterval": "1년",
            "corrosionRisk": "매우 높음",
            "maintenanceLevel": "전문가",
            "estimatedCost": "$200-1000"
        },
        {
            "id": "deck-007",
            "partNumber": "DECK-SEAL-001",
            "name": "Deck Sealing / Caulking",
            "nameKo": "데크 실링 / 코킹",
            "category": "deck",
            "inspectionItems": [
                "방수실리콘 균열, 누수",
                "비 후 누수흔적 확인"
            ],
            "checkInterval": "1년",
            "repairMethod": "실리콘 재시공",
            "estimatedCost": "$50-300"
        },
        {
            "id": "deck-008",
            "partNumber": "ROPE-LINE-001",
            "name": "Lines (Rope)",
            "nameKo": "로프류",
            "category": "deck",
            "inspectionItems": [
                "외피마모, 걸이번형",
                "하중부(윈치 접촉구) 확인"
            ],
            "checkInterval": "3개월",
            "repairMethod": "교체",
            "estimatedCost": "$50-300"
        },
        {
            "id": "deck-009",
            "partNumber": "CANVAS-001",
            "name": "Canvas / Cover",
            "nameKo": "캔버스 / 커버류",
            "category": "deck",
            "inspectionItems": [
                "UV 손상, 봉제선",
                "찢김 균열, 버클/지퍼 점검"
            ],
            "checkInterval": "6개월",
            "repairMethod": "봉제 수선",
            "estimatedCost": "$100-500"
        },
        {
            "id": "deck-010",
            "partNumber": "METAL-FITTING-001",
            "name": "Metal Fittings",
            "nameKo": "금속 피팅류",
            "category": "deck",
            "inspectionItems": [
                "전해부식, 색변화",
                "연결 볼트 해체·청소"
            ],
            "checkInterval": "1년",
            "corrosionRisk": "매우 높음",
            "estimatedCost": "$50-300"
        }
    ]
    
    # 10. 통합 체크리스트
    comprehensive_checklist = {
        "hull": {
            "category": "선체 (Hull)",
            "subcategories": [
                {
                    "name": "외관 손상, 삼투, 겔코트",
                    "interval": "매년 / 항해 후",
                    "checkPoints": [
                        "외관 손상, 삼투 방울 여부, 도장 상태"
                    ]
                }
            ]
        },
        "rigging": {
            "category": "리깅 (Rigging)",
            "subcategories": [
                {
                    "name": "스테이, 슈라우드, 턴버클",
                    "interval": "6개월 / 폭풍 후",
                    "checkPoints": [
                        "부식, 장력 이상, 균열, 마모"
                    ]
                }
            ]
        },
        "sails": {
            "category": "세일 (Sail)",
            "subcategories": [
                {
                    "name": "스티치, UV 커버, 패치",
                    "interval": "3개월 / 레이스 후",
                    "checkPoints": [
                        "봉제선, 자외선 손상, 찢김"
                    ]
                }
            ]
        },
        "engine": {
            "category": "엔진 / 추진",
            "subcategories": [
                {
                    "name": "오일, 임펠러, 벨트, 프로펠러",
                    "interval": "매월 / 운항 50h",
                    "checkPoints": [
                        "오일 상태, 냉각수 순환, 진동"
                    ]
                }
            ]
        },
        "electrical": {
            "category": "전기 시스템",
            "subcategories": [
                {
                    "name": "배터리, 충전기, 배선, 방청",
                    "interval": "3개월",
                    "checkPoints": [
                        "전압 체크, 단자 부식, 방수상태"
                    ]
                }
            ]
        },
        "steering": {
            "category": "조타장치 (Steering)",
            "subcategories": [
                {
                    "name": "러더축, 케이블, 윤활",
                    "interval": "6개월",
                    "checkPoints": [
                        "유격, 운활상태, 부식"
                    ]
                }
            ]
        },
        "bilge": {
            "category": "빌지 / 배수",
            "subcategories": [
                {
                    "name": "빌지펌프, 호스, 누수",
                    "interval": "매월",
                    "checkPoints": [
                        "펌프 작동, 호스 연결, 냉새"
                    ]
                }
            ]
        },
        "safety": {
            "category": "안전장비",
            "subcategories": [
                {
                    "name": "구명조끼, 플레어, EPIRB, 소화기",
                    "interval": "매년 / 출항 전",
                    "checkPoints": [
                        "유효기간, 작동여부, 배치상태"
                    ]
                }
            ]
        },
        "deck": {
            "category": "데크 / 하드웨어",
            "subcategories": [
                {
                    "name": "윈치, 블록, 라인, 클리트",
                    "interval": "3개월",
                    "checkPoints": [
                        "마모, 운활, 라인 상태"
                    ]
                }
            ]
        },
        "interior": {
            "category": "내부 설비 / 방수",
            "subcategories": [
                {
                    "name": "해수밸브, 화장실, 배관",
                    "interval": "6개월",
                    "checkPoints": [
                        "누수, 밸브 작동, 곰팡이"
                    ]
                }
            ]
        }
    }
    
    return {
        "hull": hull_parts,
        "rigging": rigging_parts,
        "sails": sail_parts,
        "engine": engine_parts,
        "electrical": electrical_parts,
        "steering": steering_parts,
        "bilge": bilge_parts,
        "safety": safety_parts,
        "deck": deck_parts,
        "comprehensive_checklist": comprehensive_checklist
    }


def update_yacht_parts_database():
    """yacht_parts_database.json에 실제 부품 정보 추가"""
    
    script_dir = Path(__file__).parent
    db_file = script_dir / "yacht_parts_database.json"
    
    # 기존 DB 로드
    with open(db_file, 'r', encoding='utf-8') as f:
        database = json.load(f)
    
    # 새로운 부품 데이터
    parts_data = create_comprehensive_parts_data()
    
    print("=" * 70)
    print("요트 부품 데이터베이스 업데이트 - 실제 점검 항목 추가")
    print("=" * 70)
    
    # 각 요트에 실제 부품 정보 추가
    for yacht in database.get("yachts", []):
        yacht_name = yacht.get("name")
        print(f"\n업데이트 중: {yacht_name}")
        
        # 기존 parts 구조 유지하면서 상세 정보 추가
        if "parts" not in yacht:
            yacht["parts"] = {}
        
        # 1. Hull 부품 추가
        yacht["parts"]["hull"] = parts_data["hull"]
        print(f"  - Hull: {len(parts_data['hull'])}개 점검 항목")
        
        # 2. Rigging 부품 추가
        yacht["parts"]["rigging"] = parts_data["rigging"]
        print(f"  - Rigging: {len(parts_data['rigging'])}개 점검 항목")
        
        # 3. Sails 부품 추가
        yacht["parts"]["sails"] = parts_data["sails"]
        print(f"  - Sails: {len(parts_data['sails'])}개 점검 항목")
        
        # 4. Engine 부품 추가 (10개 항목)
        yacht["parts"]["engine"] = parts_data["engine"]
        print(f"  - Engine: {len(parts_data['engine'])}개 점검 항목")
        
        # 5. Electrical 부품 추가
        yacht["parts"]["electrical"] = parts_data["electrical"]
        print(f"  - Electrical: {len(parts_data['electrical'])}개 점검 항목")
        
        # 6. Steering 부품 추가 (10개 항목)
        yacht["parts"]["steering"] = parts_data["steering"]
        print(f"  - Steering: {len(parts_data['steering'])}개 점검 항목")
        
        # 7. Bilge/Plumbing 부품 추가 (10개 항목)
        yacht["parts"]["plumbing"] = parts_data["bilge"]
        print(f"  - Bilge/Plumbing: {len(parts_data['bilge'])}개 점검 항목")
        
        # 8. Safety 부품 추가
        yacht["parts"]["safety"] = parts_data["safety"]
        print(f"  - Safety: {len(parts_data['safety'])}개 점검 항목")
        
        # 9. Deck/Winches/Blocks 부품 추가 (10개 항목)
        yacht["parts"]["deck"] = parts_data["deck"]
        print(f"  - Deck Hardware: {len(parts_data['deck'])}개 점검 항목")
        
        # 통합 체크리스트 추가
        yacht["maintenanceChecklist"] = parts_data["comprehensive_checklist"]
    
    # 저장
    with open(db_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 70)
    print("Update Complete!")
    print("=" * 70)
    
    # 통계
    total_parts = 0
    for category in parts_data.values():
        if isinstance(category, list):
            total_parts += len(category)
    
    print(f"\n📊 통계:")
    print(f"  - 총 요트: {len(database['yachts'])}개")
    print(f"  - 카테고리별 부품 항목:")
    print(f"    • Hull: {len(parts_data['hull'])}개")
    print(f"    • Rigging: {len(parts_data['rigging'])}개")
    print(f"    • Sails: {len(parts_data['sails'])}개")
    print(f"    • Engine: {len(parts_data['engine'])}개 ⭐")
    print(f"    • Electrical: {len(parts_data['electrical'])}개")
    print(f"    • Steering: {len(parts_data['steering'])}개 ⭐")
    print(f"    • Bilge/Plumbing: {len(parts_data['bilge'])}개 ⭐")
    print(f"    • Safety: {len(parts_data['safety'])}개")
    print(f"    • Deck Hardware: {len(parts_data['deck'])}개 ⭐")
    print(f"\n  ⭐ = 이미지 기반 10개 상세 항목")
    print(f"\n💾 저장: {db_file}")


if __name__ == "__main__":
    update_yacht_parts_database()

