"""PDF 内容提取脚本"""
import PyPDF2
import json
import re
from pathlib import Path
from typing import List, Dict, Any


def extract_pdf_content(pdf_path: str) -> List[Dict[str, Any]]:
    """
    提取 PDF 内容

    Args:
        pdf_path: PDF 文件路径

    Returns:
        页面内容列表
    """
    content = []

    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        total_pages = len(reader.pages)

        print(f"PDF 总页数: {total_pages}")

        for i in range(total_pages):
            page = reader.pages[i]
            text = page.extract_text()

            if text and len(text.strip()) > 50:
                content.append({
                    'page': i + 1,
                    'text': text.strip()
                })

            # 进度
            if (i + 1) % 100 == 0:
                print(f"  已处理 {i + 1}/{total_pages} 页")

    print(f"共提取 {len(content)} 页有效内容")
    return content


def split_by_chapters(content: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    按章节分段

    Args:
        content: 页面内容列表

    Returns:
        章节列表
    """
    chapters = []
    current_chapter = None
    current_content = []

    # 章节标题模式
    chapter_pattern = re.compile(r'第[一二三四五六七八九十\d]+章\s*(.*)')

    for page in content:
        text = page['text']

        # 检查是否是新章节
        match = chapter_pattern.search(text)
        if match:
            # 保存上一章
            if current_chapter:
                chapters.append({
                    'chapter': current_chapter,
                    'content': '\n'.join(current_content)
                })

            # 开始新章节
            current_chapter = match.group(1).strip()
            current_content = [text]
        else:
            if current_chapter:
                current_content.append(text)

    # 保存最后一章
    if current_chapter:
        chapters.append({
            'chapter': current_chapter,
            'content': '\n'.join(current_content)
        })

    return chapters


def save_knowledge_base(chapters: List[Dict[str, Any]], output_path: str):
    """
    保存到知识库

    Args:
        chapters: 章节列表
        output_path: 输出路径
    """
    knowledge = {
        'source': '云原生 Kubernetes 全栈架构师实战',
        'author': '杜宽',
        'chapters': chapters
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(knowledge, f, ensure_ascii=False, indent=2)

    print(f"已保存到: {output_path}")
    print(f"共 {len(chapters)} 个章节")


if __name__ == '__main__':
    # PDF 路径
    pdf_path = r'C:\Users\75495\WPSDrive\307194589\WPS云盘\我的书库\云原生Kubernetes全栈架构师实战 (杜宽) (Z-Library).pdf'

    # 输出路径
    output_path = 'data/knowledge/books/kubernetes_book_content.json'

    # 提取内容
    print("=" * 60)
    print("开始提取 PDF 内容")
    print("=" * 60)

    content = extract_pdf_content(pdf_path)

    # 按章节分段
    print("\n按章节分段...")
    chapters = split_by_chapters(content)
    print(f"识别到 {len(chapters)} 个章节")

    # 保存
    print("\n保存到知识库...")
    save_knowledge_base(chapters, output_path)

    print("\n完成!")
