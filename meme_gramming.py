#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib      # used for hash generation
from datetime import datetime, timedelta
from nltk import ngrams    # used for ngram extraction

# ORM related imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from orm_defs import Base, NGram, MGram, Article, ArticleText


class MgramExtractor():
    
# ORM related vars
    session = None
    engine = None
# ################# 
    
    def __init__(self,db_connection_string):
        self.engine = create_engine(db_connection_string)
        Base.metadata.create_all(self.engine)
        
    def get_session(self):
        if self.session == None:
            self.session = scoped_session(sessionmaker(bind=self.engine))
        return self.session    
        
    def commit(self):
        self.get_session().commit()
        
#####################################
# create new ngram in database or update counter for existing
# returns True if ngram exists, othervise - False 
    def create_or_update_ngram(self, _hash, n_gram, lang_id, date):
        ngram = self.get_session().query(NGram).filter(NGram._hash == _hash).first()
        if ngram:
            ngram.count += 1
            return True
        else:
            ngram = NGram(_hash, n_gram, 1, lang_id, date)
            self.get_session().add(ngram)
            return False
        
        
# main method
    def process(self):
        now = datetime.now()
        
        # get all articles without processed mgram extraction
        #.filter(Article.mgrams.count == 0)
        for article in self.get_session().query(Article).all():
            print "Processing %s" % article
            
            if article.mgrams.filter().count() > 0:
                print "Already extracted, mgram count: %d" % article.mgrams.filter().count()
                continue
            
            for article_text in article.article_texts:
                print "Processing %s" % article_text
                # get n-grams with size of 1-5 
                article_text_split = article_text.text.split()
                for n in range(1,5):
                    n_grams = ngrams(article_text_split, n)
                    for gram in n_grams:
                        gram_str = ' '.join(gram)
                        _hash = hashlib.sha256(gram_str).hexdigest()
                        
                        # save ngram
                        ngram_exists = self.create_or_update_ngram(_hash, gram_str, article.lang_id, now)
                        # save mgram
                        mgram = article.mgrams.filter(MGram.m_gram == gram_str).first()
                        if mgram:
                            mgram.count += 1
                        else:
                            if ngram_exists:
                                mgram = self.get_session().query(MGram).filter(MGram.m_gram == gram_str).order_by(MGram.id.desc()).first()
                                mgram.count += 1
                            else:
                                mgram = MGram(gram_str, now, 1, article.lang_id)
                            article.mgrams.append(mgram)
            self.get_session().commit()
    
########################################
def main():
    extractor = MgramExtractor('sqlite:///database.db')
    extractor.process()

    return

########################################
main()
