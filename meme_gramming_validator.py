#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib      # used for hash generation
from datetime import datetime
from nltk import ngrams    # used for ngram extraction

# ORM related imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from orm_defs import Base, NGram, MGram, Article, ArticleText


class MgramExtractorValidator():
    
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
         
# main method
    def validate(self):
        now = datetime.now()
        
        # get all articles without processed mgram extraction
        #.filter(Article.mgrams.count == 0)
        for article in self.get_session().query(Article).all():
            print "Processing %s" % article
            
            for article_text in article.article_texts:
                print "Processing %s" % article_text
                # get n-grams with size of 1-5 
                article_text_split = article_text.text.split()
                for n in range(1,5):
                    n_grams = ngrams(article_text_split, n)
                    for gram in n_grams:
                        gram_str = ' '.join(gram)
                        found = article.mgrams.filter(MGram.m_gram == gram_str).count()
                        if found:
                            #print "Found %s" % gram_str
                            continue
                        print "Not Found: %s" % gram_str
                        
            self.get_session().commit()
        

########################################
def main():


    validator = MgramExtractorValidator('sqlite:///database.db')
    validator.validate()

    return

########################################
main()
