from datetime import date
from polarlib.polar.news_corpus_collector import *


OUTPUT_DIR = "Olympics_jan_june"  

if __name__ == "__main__":
  
    master_keywords=[
            "olympics",
            "olympic",
    ]
    
    corpus_collector = NewsCorpusCollector(
        output_dir = OUTPUT_DIR,
        from_date = date(year=2024, month=1, day=1),
        to_date = date(year=2024, month=5, day=23),
        keywords = master_keywords
    )

    corpus_collector.collect_archives()
    corpus_collector.collect_articles() 
    corpus_collector.pre_process_articles()


