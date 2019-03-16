#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

# ORM related imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from orm_defs import Base, NGram


class MgramExtractorCleanup():
    
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
        
# main method
    def cleanup(self,max_days):
        now = datetime.now()
        delta = datetime.today() - timedelta(days=max_days)
        ngrams_to_remove = self.get_session().query(NGram).filter(NGram.date < delta).delete()
        self.commit()
        

########################################
def main():


    cleanup = MgramExtractorCleanup('sqlite:///database.db')
    cleanup.cleanup(7)

    return

########################################
main()
