#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

###############################################
# N-gram mapping
class NGram(Base):
    __tablename__ = 'n_grams'
    id = Column(Integer, primary_key=True)
    _hash = Column(String, unique=True)
    n_gram = Column(String)
    count = Column(Integer)
    lang_id = Column(Integer)
    date = Column(DateTime, default=func.now())
    
    def __init__(self, _hash, n_gram, count, lang_id, date):
        self._hash = _hash
        self.n_gram = n_gram
        self.count = count
        self.lang_id = lang_id
        self.date = date

    def __repr__(self):
        return "<NGram('%s','%d', '%d', '%s')>" % (self._hash, self.count, self.lang_id, self.date)
    
###############################################
# Article-Mgram association mapping
article_mgram_assoc = Table("article_mgram_assoc", 
                            Base.metadata,
                            Column('article_id', Integer, ForeignKey('articles.id')),
                            Column('mgram_id', Integer, ForeignKey('m_grams.id'))
                            )
    
###############################################
# M-gram mapping
class MGram(Base):
    __tablename__ = 'm_grams'
    id = Column(Integer, primary_key=True)
    m_gram = Column(String)
    date = Column(DateTime, default=func.now())
    count = Column(Integer)
    lang_id = Column(Integer)
    
    articles = relationship("Article",
                          secondary=article_mgram_assoc,
                          back_populates="mgrams")
    
    #article = relationship(Article, backref=backref('mgrams'))
    
    def __init__(self, m_gram, date, count, lang_id):
        self.m_gram = m_gram
        self.date = date
        self.count = count
        self.lang_id = lang_id

    def __repr__(self):
        return "<MGram('%s','%s', '%d', '%d')>" % (self.m_gram, self.date, self.count, self.lang_id)
    
###############################################
# Article mapping
class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=func.now())
    lang_id = Column(Integer)
    total_docs = Column(Integer)
    relevant_docs = Column(Integer)
    #m_gram_ids = Column(String)
    mgrams = relationship("MGram",
                          secondary=article_mgram_assoc,
                          lazy='dynamic',
                          back_populates="articles")
       
    def __init__(self, date, lang_id, total_docs, relevant_docs):
        self.date = date
        self.lang_id = lang_id
        self.total_docs = total_docs
        self.relevant_docs = relevant_docs

    def __repr__(self):
        return "<Article('%s','%d', '%d', '%d')>" % (self.date, self.lang_id, self.total_docs, self.relevant_docs)
    
###############################################
# Article texts mapping
class ArticleText(Base):
    __tablename__ = 'article_texts'
    doc_id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey('articles.id'))
    url = Column(String)
    text = Column(String)
    prob_d = Column(String)
    prob_t = Column(String)
    
    # Use cascade='delete,all' to propagate the deletion of all article texts with article
    article = relationship(
        Article,
        backref=backref('article_texts',
                         uselist=True,
                         cascade='delete,all'))
    
    def __init__(self, article, url, text, prob_d, prob_t):
        self.article = article
        self.url = url
        self.text = text
        self.prob_d = prob_d
        self.prob_t = prob_t

    def __repr__(self):
        return "<ArticleText('%d','%s', '%s', '%s')>" % (self.request_id, self.url, self.prob_d, self.prob_t)
  


#
