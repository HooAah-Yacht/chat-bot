import json
import argparse
import re
from pathlib import Path


def find_json_path():
    # 스크립트 파일이 있는 디렉터리를 우선으로 사용합니다.
    script_dir = Path(__file__).resolve().parent
    candidates = [
        script_dir / "YachtList01.json",
        Path("YachtList01.json"),
        script_dir / "front" / "YachtList01.json",
        Path(r"c:\\Users\\user\\Documents\\요트앱\\front\\YachtList01.json"),
    ]

    for p in candidates:
        try:
            if p.exists():
                return p.resolve()
        except Exception:
            continue
    return None


json_path = find_json_path()
if json_path is None:
    raise FileNotFoundError(
        "YachtList01.json 파일을 찾을 수 없습니다. 'YachtList01.json'을 이 스크립트와 동일한 폴더에 놓거나 경로를 확인하세요."
    )

with open(json_path, 'r', encoding='utf-8') as f:
    yacht_data = json.load(f)


def get_yacht_dimensions_by_question(question):
    # 키워드 존재 여부(소문자 비교)
    keywords = ['크기', '길이', '전장', 'lwl', 'loa', 'beam', '폭', 'draft', '흘수']

    def normalize_text(s: str) -> str:
        """소문자 변환, 구두점 제거, 연속 공백 정리"""
        if not isinstance(s, str):
            return ''
        s_lower = s.lower()
        # 구두점(문자, 기호) 제거: 단, 한글/영숫자/공백은 유지
        s_clean = re.sub(r"[^\w\s가-힣]+", " ", s_lower, flags=re.UNICODE)
        # 여러 공백을 단일 공백으로
        s_clean = re.sub(r"\s+", " ", s_clean).strip()
        return s_clean

    question_norm = normalize_text(question)
    if not any(k in question_norm for k in keywords):
        return None

    for yacht in yacht_data.get('yachts', []):
        model_name_raw = yacht.get('model_name', '')
        model_norm = normalize_text(model_name_raw)
        if not model_norm:
            continue

        # 완전 매칭 또는 부분 단어 매칭
        if model_norm in question_norm or any(part in question_norm for part in model_norm.split()):
            dim = yacht.get('dimensions', {})
            reply = (
                f"'{model_name_raw}'의 크기 정보는 아래와 같습니다:\n"
                f"- LOA(전장): {dim.get('LOA_m', '?')} m ({dim.get('LOA_ft', '?')} ft)\n"
                f"- LWL(수선간장): {dim.get('LWL_m', '?')} m ({dim.get('LWL_ft', '?')} ft)\n"
                f"- Beam(폭): {dim.get('Beam_m', '?')} m ({dim.get('Beam_ft', '?')} ft)\n"
                f"- Draft(흘수): {dim.get('Draft_m', '?')} m ({dim.get('Draft_ft', '?')} ft)"
            )
            return reply

    return "해당 요트 정보를 찾을 수 없습니다. 모델명을 정확히 입력해주세요."


def list_models(limit=20):
    models = [y.get('model_name', '(이름없음)') for y in yacht_data.get('yachts', [])]
    for i, m in enumerate(models[:limit], start=1):
        print(f"{i}. {m}")
    if len(models) > limit:
        print(f"...and {len(models)-limit} more models")


def main():
    parser = argparse.ArgumentParser(description="요트 챗봇 (로컬 실행)")
    parser.add_argument('--question', '-q', help="질문을 한 번만 던지고 종료합니다.")
    parser.add_argument('--list', '-l', action='store_true', help="모델 목록을 출력합니다.")
    parser.add_argument('--info', action='store_true', help="JSON 경로와 요트 개수 정보를 출력합니다.")
    args = parser.parse_args()

    if args.info:
        print(f"사용된 JSON 경로: {json_path}")
        print(f"총 요트 개수: {len(yacht_data.get('yachts', []))}")
        return

    if args.list:
        list_models()
        return

    if args.question:
        ans = get_yacht_dimensions_by_question(args.question)
        print(ans or "해당 질문에 맞는 응답을 준비하지 못했습니다.")
        return

    # 대화형 모드
    print("요트 상태 질문 챗봇입니다. '종료'를 입력하면 종료됩니다.")
    while True:
        user_input = input("질문을 입력하세요: ").strip()
        if user_input == '종료':
            print("챗봇을 종료합니다.")
            break
        answer = get_yacht_dimensions_by_question(user_input)
        print("챗봇:", answer or "해당 질문에 맞는 응답을 준비하지 못했습니다.")


if __name__ == '__main__':
    main()
