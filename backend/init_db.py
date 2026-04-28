"""Initialize database with mock data"""
import os
import sys
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from app.database import init_db, SessionLocal
from app.models import Paper, ChineseQuote, Highlight


def populate_mock_data():
    """Populate database with mock papers and quotes"""
    db = SessionLocal()

    # Mock papers
    papers = [
        {
            "title": "深度学习在中文自然语言处理中的应用",
            "authors": "张三, 李四, 王五",
            "abstract": "本论文研究了深度学习技术在中文NLP任务中的应用，包括文本分类、情感分析和机器翻译。我们提出了一个新的架构来处理中文的复杂性。",
            "full_text": """本论文研究了深度学习技术在中文NLP任务中的应用，包括文本分类、情感分析和机器翻译。我们提出了一个新的架构来处理中文的复杂性。

1. 引言
中文自然语言处理（NLP）一直是计算机科学中的一个重要课题。与英文不同，中文具有独特的语言特征。

2. 方法论
我们采用了递归神经网络（RNN）和注意力机制来处理中文序列。

3. 实验结果
实验表明我们的方法在多个基准数据集上取得了最先进的性能。

4. 结论
深度学习为中文NLP的发展提供了新的可能性。""",
            "keywords": "深度学习,中文NLP,神经网络,自然语言处理",
            "source_url": "https://example.com/paper1",
            "publication_date": datetime(2023, 5, 15),
        },
        {
            "title": "传统中文文献与现代数字人文的融合研究",
            "authors": "陈先生, 周女士",
            "abstract": "本研究探讨了如何将古代中文文献与现代数字人文方法相结合，以实现对经典著作的新诠释。",
            "full_text": """本研究探讨了如何将古代中文文献与现代数字人文方法相结合，以实现对经典著作的新诠释。

1. 文献回顾
数字人文是一个新兴领域，将计算方法应用于人文学科。

2. 案例研究
我们选择了《红楼梦》作为案例，进行了文本挖掘和网络分析。

3. 发现
通过数据可视化，我们发现了角色之间的复杂关系网络。

4. 教学应用
这些发现可以用于改进中文文学教学方法。""",
            "keywords": "数字人文,中文文献,文本挖掘,数据可视化",
            "source_url": "https://example.com/paper2",
            "publication_date": datetime(2023, 8, 20),
        },
        {
            "title": "学术写作中的修辞策略：英中对比研究",
            "authors": "刘教授",
            "abstract": "本论文通过对比分析，研究英文和中文学术写作中的修辞差异和相似性。",
            "full_text": """本论文通过对比分析，研究英文和中文学术写作中的修辞差异和相似性。

1. 引言
学术写作的修辞策略在不同语言文化中存在差异。

2. 理论框架
我们采用了系统功能语言学的框架进行分析。

3. 对比分析
英文学术写作倾向于直接表达观点，而中文则更强调语境和背景。

4. 教学启示
这些发现对学术写作教学具有重要意义。""",
            "keywords": "学术写作,修辞策略,对比研究,语言文化",
            "source_url": "https://example.com/paper3",
            "publication_date": datetime(2023, 10, 10),
        },
    ]

    # Check if papers already exist
    existing_count = db.query(Paper).count()
    if existing_count == 0:
        for paper_data in papers:
            paper = Paper(**paper_data)
            db.add(paper)
        db.commit()
        print(f"✓ Added {len(papers)} mock papers to database")

    # Mock Chinese quotes
    quotes = [
        {
            "quote": "学而时习之，不亦说乎",
            "source": "《论语》",
            "author": "孔子",
            "era": "春秋战国",
            "meaning": "学习了知识，经常复习它，不是很快乐吗？强调学习与实践的结合。",
        },
        {
            "quote": "知己知彼，百战不殆",
            "source": "《孙子兵法》",
            "author": "孙武",
            "era": "春秋战国",
            "meaning": "了解自己和敌人，就不会在战争中失利。引申为全面理解问题。",
        },
        {
            "quote": "纸上得来终觉浅，绝知此事要躬行",
            "source": "《冬夜读书示子聿》",
            "author": "陆游",
            "era": "南宋",
            "meaning": "从书本上获得的知识终究很肤浅，要真正理解还需亲身体验。",
        },
        {
            "quote": "读书破万卷，下笔如有神",
            "source": "《奉赠韦左丞丈》",
            "author": "杜甫",
            "era": "唐代",
            "meaning": "阅读大量书籍，写文章就像有神灵相助。强调阅读量对写作的影响。",
        },
        {
            "quote": "君子之学，贵以专",
            "source": "《荀子》",
            "author": "荀子",
            "era": "春秋战国",
            "meaning": "君子的学习，贵在专注。强调学习的专注性和深度。",
        },
    ]

    existing_quotes = db.query(ChineseQuote).count()
    if existing_quotes == 0:
        for quote_data in quotes:
            quote = ChineseQuote(**quote_data)
            db.add(quote)
        db.commit()
        print(f"✓ Added {len(quotes)} mock quotes to database")

    db.close()
    print("✓ Database initialization complete!")


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    populate_mock_data()
