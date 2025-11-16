# -*- coding: utf-8 -*-
"""
요트 정보 챗봇 - 향상된 버전
yacht_specifications.json을 사용하여 상세한 요트 정보 제공
"""
import json
import argparse
import re
from pathlib import Path


def find_json_path():
    """JSON 파일 경로를 찾습니다. (우선순위: yacht_specifications.json > YachtList01.json)"""
    script_dir = Path(__file__).resolve().parent
    
    # 새로운 상세 데이터 우선
    candidates_new = [
        script_dir / "data" / "yacht_specifications.json",
        script_dir / "yacht_specifications.json",
    ]
    
    # 기존 데이터 (fallback)
    candidates_old = [
        script_dir / "YachtList01.json",
        Path("YachtList01.json"),
    ]
    
    # 새 데이터 먼저 시도
    for p in candidates_new:
        try:
            if p.exists():
                return p.resolve(), 'new'
        except Exception:
            continue
    
    # 기존 데이터로 fallback
    for p in candidates_old:
        try:
            if p.exists():
                return p.resolve(), 'old'
        except Exception:
            continue
    
    return None, None


json_path, data_version = find_json_path()
if json_path is None:
    raise FileNotFoundError(
        "요트 데이터 JSON 파일을 찾을 수 없습니다.\n"
        "다음 중 하나를 이 스크립트와 동일한 폴더에 놓으세요:\n"
        "- data/yacht_specifications.json (권장)\n"
        "- YachtList01.json"
    )

with open(json_path, 'r', encoding='utf-8') as f:
    yacht_data = json.load(f)

print(f"✅ 데이터 로드 완료: {json_path.name} ({'상세 버전' if data_version == 'new' else '기본 버전'})")


def normalize_text(s: str) -> str:
    """소문자 변환, 구두점 제거, 연속 공백 정리"""
    if not isinstance(s, str):
        return ''
    s_lower = s.lower()
    # 구두점 제거: 한글/영숫자/공백은 유지
    s_clean = re.sub(r"[^\w\s가-힣]+", " ", s_lower, flags=re.UNICODE)
    # 여러 공백을 단일 공백으로
    s_clean = re.sub(r"\s+", " ", s_clean).strip()
    return s_clean


def get_yacht_by_name(question: str, yachts_list: list) -> dict:
    """질문에서 요트 이름을 찾아 매칭되는 요트 정보 반환"""
    question_norm = normalize_text(question)
    
    for yacht in yachts_list:
        # 새 버전과 구 버전 모두 지원
        model_name = yacht.get('name') or yacht.get('model_name', '')
        model_norm = normalize_text(model_name)
        
        if not model_norm:
            continue
        
        # 완전 매칭 또는 부분 단어 매칭
        if model_norm in question_norm or any(part in question_norm for part in model_norm.split()):
            return yacht
    
    return None


def format_dimensions_response(yacht: dict, data_version: str) -> str:
    """요트의 치수 정보를 포맷팅"""
    if data_version == 'new':
        # 새로운 yacht_specifications.json 형식
        model_name = yacht.get('name', 'Unknown')
        dim = yacht.get('dimensions', {})
        
        response = f"'{model_name}'의 크기 정보는 아래와 같습니다:\n\n"
        response += f"📏 **기본 치수**\n"
        
        if 'loa' in dim:
            loa = dim['loa']
            response += f"- LOA (전장): {loa.get('display', loa.get('value', '?'))} {loa.get('unit', '')}\n"
        
        if 'lwl' in dim:
            lwl = dim['lwl']
            response += f"- LWL (수선장): {lwl.get('display', lwl.get('value', '?'))} {lwl.get('unit', '')}\n"
        
        if 'beam' in dim:
            beam = dim['beam']
            response += f"- Beam (폭): {beam.get('display', beam.get('value', '?'))} {beam.get('unit', '')}\n"
        
        if 'draft' in dim:
            draft = dim['draft']
            response += f"- Draft (흘수): {draft.get('display', draft.get('value', '?'))} {draft.get('unit', '')}\n"
        
        if 'displacement' in dim:
            disp = dim['displacement']
            response += f"- Displacement (배수량): {disp.get('display', disp.get('value', '?'))} {disp.get('unit', '')}\n"
        
        if 'mastHeight' in dim:
            mast = dim['mastHeight']
            response += f"- Mast Height (마스트 높이): {mast.get('display', mast.get('value', '?'))} {mast.get('unit', '')}\n"
        
        return response.strip()
    
    else:
        # 기존 YachtList01.json 형식
        model_name = yacht.get('model_name', 'Unknown')
        dim = yacht.get('dimensions', {})
        
        response = f"'{model_name}'의 크기 정보는 아래와 같습니다:\n"
        response += f"- LOA(전장): {dim.get('LOA_m', '?')} m ({dim.get('LOA_ft', '?')} ft)\n"
        response += f"- LWL(수선간장): {dim.get('LWL_m', '?')} m ({dim.get('LWL_ft', '?')} ft)\n"
        response += f"- Beam(폭): {dim.get('Beam_m', '?')} m ({dim.get('Beam_ft', '?')} ft)\n"
        response += f"- Draft(흘수): {dim.get('Draft_m', '?')} m ({dim.get('Draft_ft', '?')} ft)"
        
        return response


def format_full_info_response(yacht: dict, data_version: str) -> str:
    """요트의 전체 정보를 포맷팅 (새 버전만 지원)"""
    if data_version != 'new':
        return format_dimensions_response(yacht, data_version)
    
    model_name = yacht.get('name', 'Unknown')
    response = f"🛥️ **{model_name}** - 상세 정보\n\n"
    
    # 기본 정보
    if yacht.get('manufacturer'):
        response += f"제조사: {yacht['manufacturer']}\n"
    if yacht.get('type'):
        response += f"타입: {yacht['type']}\n"
    if yacht.get('designer'):
        response += f"디자이너: {yacht['designer']}\n"
    if yacht.get('year'):
        response += f"제작년도: {yacht['year']}\n"
    response += "\n"
    
    # 치수
    dim = yacht.get('dimensions', {})
    if dim:
        response += f"📏 **치수**\n"
        if 'loa' in dim:
            response += f"- LOA: {dim['loa'].get('display', '?')}\n"
        if 'beam' in dim:
            response += f"- Beam (폭): {dim['beam'].get('display', '?')}\n"
        if 'draft' in dim:
            response += f"- Draft (흘수): {dim['draft'].get('display', '?')}\n"
        if 'displacement' in dim:
            response += f"- Displacement (배수량): {dim['displacement'].get('display', '?')}\n"
        if 'mastHeight' in dim:
            response += f"- Mast Height: {dim['mastHeight'].get('display', '?')}\n"
        response += "\n"
    
    # 돛 면적
    sail = yacht.get('sailArea', {})
    if sail:
        response += f"⛵ **돛 면적**\n"
        if 'main' in sail:
            response += f"- Main: {sail['main'].get('value', '?')} {sail['main'].get('unit', '')}\n"
        if 'jib' in sail:
            response += f"- Jib: {sail['jib'].get('value', '?')} {sail['jib'].get('unit', '')}\n"
        if 'spinnaker' in sail:
            response += f"- Spinnaker: {sail['spinnaker'].get('value', '?')} {sail['spinnaker'].get('unit', '')}\n"
        if 'total' in sail:
            response += f"- Total: {sail['total'].get('display', '?')}\n"
        response += "\n"
    
    # 엔진
    engine = yacht.get('engine', {})
    if engine:
        response += f"🔧 **엔진**\n"
        response += f"- Type: {engine.get('type', '?')}\n"
        response += f"- Power: {engine.get('power', '?')}\n"
        if engine.get('model'):
            response += f"- Model: {engine.get('model')}\n"
        response += "\n"
    
    # 탱크
    tanks = yacht.get('tanks', {})
    if tanks:
        response += f"⛽ **탱크**\n"
        if 'fuel' in tanks:
            response += f"- Fuel: {tanks['fuel'].get('value', '?')} {tanks['fuel'].get('unit', '')}\n"
        if 'water' in tanks:
            response += f"- Water: {tanks['water'].get('value', '?')} {tanks['water'].get('unit', '')}\n"
        response += "\n"
    
    # 숙박
    accom = yacht.get('accommodation', {})
    if accom:
        response += f"🛏️ **숙박 시설**\n"
        if 'cabins' in accom:
            response += f"- Cabins (선실): {accom.get('cabins')}\n"
        if 'berths' in accom:
            response += f"- Berths (침대): {accom.get('berths')}\n"
        if 'heads' in accom:
            response += f"- Heads (화장실): {accom.get('heads')}\n"
        if 'crew' in accom:
            response += f"- Crew: {accom.get('crew')}\n"
        response += "\n"
    
    return response.strip()


def get_yacht_info_by_question(question: str) -> str:
    """질문에 맞는 요트 정보 반환"""
    # 키워드 체크
    dimension_keywords = ['크기', '길이', '전장', 'lwl', 'loa', 'beam', '폭', 'draft', '흘수', '치수', '높이', '마스트']
    full_info_keywords = ['정보', '스펙', '사양', '상세', '전체', '모든', 'spec', 'info']
    
    question_norm = normalize_text(question)
    
    # 요트 목록 가져오기
    if data_version == 'new':
        yachts_list = yacht_data.get('yachts', [])
    else:
        yachts_list = yacht_data.get('yachts', [])
    
    # 요트 찾기
    yacht = get_yacht_by_name(question, yachts_list)
    
    if not yacht:
        return "해당 요트 정보를 찾을 수 없습니다. '--list' 옵션으로 모델 목록을 확인해주세요."
    
    # 전체 정보 요청인지 치수만 요청인지 판단
    if any(k in question_norm for k in full_info_keywords):
        return format_full_info_response(yacht, data_version)
    elif any(k in question_norm for k in dimension_keywords):
        return format_dimensions_response(yacht, data_version)
    else:
        # 기본은 치수 정보
        return format_dimensions_response(yacht, data_version)


def list_models(limit=50):
    """요트 모델 목록 출력"""
    if data_version == 'new':
        yachts_list = yacht_data.get('yachts', [])
        models = [f"{y.get('name', '?')} ({y.get('type', '?')})" for y in yachts_list]
    else:
        yachts_list = yacht_data.get('yachts', [])
        models = [y.get('model_name', '(이름없음)') for y in yachts_list]
    
    print(f"\n📋 총 {len(models)}개의 요트 모델:\n")
    for i, m in enumerate(models[:limit], start=1):
        print(f"  {i}. {m}")
    
    if len(models) > limit:
        print(f"\n...and {len(models)-limit} more models")


def show_info():
    """JSON 파일 정보 출력"""
    print(f"\n📊 요트 데이터 정보")
    print(f"=" * 50)
    print(f"JSON 경로: {json_path}")
    print(f"데이터 버전: {data_version} ({'상세 버전' if data_version == 'new' else '기본 버전'})")
    
    if data_version == 'new':
        yachts_list = yacht_data.get('yachts', [])
        print(f"총 요트 개수: {len(yachts_list)}")
        print(f"데이터 버전: {yacht_data.get('version', '?')}")
        print(f"마지막 업데이트: {yacht_data.get('lastUpdated', '?')}")
        
        categories = yacht_data.get('categories', {})
        if categories:
            print(f"\n📂 카테고리:")
            for cat, yachts in categories.items():
                print(f"  - {cat}: {len(yachts)}개")
    else:
        yachts_list = yacht_data.get('yachts', [])
        print(f"총 요트 개수: {len(yachts_list)}")
    
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="요트 정보 챗봇 (로컬 실행)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python chatbot.py                          # 대화형 모드
  python chatbot.py -q "Laser 크기"          # 단일 질문
  python chatbot.py -q "FarEast 28 정보"     # 상세 정보
  python chatbot.py --list                   # 모델 목록
  python chatbot.py --info                   # 데이터 정보
        """
    )
    parser.add_argument('--question', '-q', help="질문을 한 번만 던지고 종료합니다.")
    parser.add_argument('--list', '-l', action='store_true', help="모델 목록을 출력합니다.")
    parser.add_argument('--info', action='store_true', help="JSON 경로와 요트 개수 정보를 출력합니다.")
    args = parser.parse_args()

    if args.info:
        show_info()
        return

    if args.list:
        list_models()
        return

    if args.question:
        ans = get_yacht_info_by_question(args.question)
        print(f"\n{ans}\n")
        return

    # 대화형 모드
    print("\n" + "=" * 60)
    print("🛥️  요트 정보 챗봇 - 향상된 버전")
    print("=" * 60)
    print("질문 예시:")
    print("  - 'Laser 크기'")
    print("  - 'FarEast 28 정보'")
    print("  - 'Beneteau Oceanis 46.1 스펙'")
    print("\n'종료' 또는 'exit'를 입력하면 종료됩니다.")
    print("=" * 60 + "\n")
    
    while True:
        try:
            user_input = input("💬 질문: ").strip()
            if user_input.lower() in ['종료', 'exit', 'quit', 'q']:
                print("\n👋 챗봇을 종료합니다.\n")
                break
            
            if not user_input:
                continue
            
            answer = get_yacht_info_by_question(user_input)
            print(f"\n🤖 챗봇:\n{answer}\n")
            print("-" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 챗봇을 종료합니다.\n")
            break
        except Exception as e:
            print(f"\n⚠️  오류 발생: {e}\n")


if __name__ == '__main__':
    main()
