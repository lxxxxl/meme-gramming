#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from orm_defs import Base, NGram, MGram, Article, ArticleText


engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)

session = scoped_session(sessionmaker(bind=engine))

article1 = Article(datetime.now(), 3, 1, 1)
session.add(article1)
article2 = Article(datetime.now(), 1, 0, 0)
session.add(article2)

article_text1 = ArticleText(article1, "https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91", "The case() expression accepts a list of conditions to match and the column to return if the condition matches, followed by an else_ if none of the conditions match.", "", "")
session.add(article_text1)
article_text2 = ArticleText(article1, "https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91", "If you have two tables that already have an established relationship, you can automatically use that relationship by just adding the columns we want from each table to the select statement.", "", "")
session.add(article_text2)
article_text3 = ArticleText(article1, "https://docs.sqlalchemy.org/en/latest/orm/collections.html", "The default behavior of relationship() is to fully load the collection of items in, as according to the loading strategy of the relationship. Additionally, the Session by default only knows how to delete objects which are actually present within the session. When a parent instance is marked for deletion and flushed, the Session loads its full list of child items in so that they may either be deleted as well, or have their foreign key value set to null; this is to avoid constraint violations. For large collections of child items, there are several strategies to bypass full loading of child items both at load time as well as deletion time.", "", "")
session.add(article_text3)
article_text4 = ArticleText(article2, "https://docs.sqlalchemy.org/en/latest/orm/collections.html", "Do I need a custom collection implementation. In most cases not at all! The most common use cases for a custom collection is one that validates or marshals incoming values into a new form, such as a string that becomes a class instance, or one which goes a step beyond and represents the data internally in some fashion, presenting a view of that data on the outside of a different form. For the first use case, the orm.validates() decorator is by far the simplest way to intercept incoming values in all cases for the purposes of validation and simple marshaling. See Simple Validators for an example of this. For the second use case, the Association Proxy extension is a well-tested, widely used system that provides a read/write view of a collection in terms of some attribute present on the target object.", "", "")
session.add(article_text4)


session.commit()
