import PyPDF2
import json

# PDF 읽기
pdf_path = "data/yachtpdf/nautor-swan-48-galatea.pdf"
with open(pdf_path, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    
    print(f"총 페이지: {len(reader.pages)}\n")
    print("="*80)
    print("첫 3페이지 내용:")
    print("="*80)
    
    for i in range(min(3, len(reader.pages))):
        print(f"\n--- 페이지 {i+1} ---\n")
        text = reader.pages[i].extract_text()
        print(text[:800])
        print("\n" + "="*80)
