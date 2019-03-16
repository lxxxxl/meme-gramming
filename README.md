# Meme gramming script
This script is used to generate m-grams with size from 1 to 5 for provided articles.  
The output is array of m-grams for provided article.  
## Setup:
1. Install required python modules:   
```pip install sqlalchemy```  
```pip install nltk  ```
2. Add _remove_old_nrgams.py_ to crontab to execute every week. Add this line to _/etc/crontab_:  
```0 0 * * 0 /path/to/remove_old_nrgams.py```  
[Here](https://www.cyberciti.biz/faq/how-do-i-add-jobs-to-cron-under-linux-or-unix-oses/) you can find detailed info about cron configuration
Also you can integrate _MgramExtractorCleanup_ class to your scheduler. For example see _remove\_old\_nrgams.py_
3. Give execution rights to _meme\_gramming.py_ and _remove\_old\_nrgams.py_:  
```chmod 755 meme_gramming.py```  
```chmod 755 remove_old_nrgams.py```  

## Usage:
1. Fill input tables _articles_ and _article_texts_ with your data, or run _orm\_generate\_and\_fill\_with\_test\_data.py_ to create database tables and fill some test articles.
2. Run _meme\_gramming.py_  
4. Run _meme\_gramming\_validator.py_. If some of mrgams absent, you will see error message.


## File description:
_orm\_defs.py_ - definition of ORM mappings.
_meme\_gramming.py_ - contains class MgramExtractor with extraction logic.
_meme\_gramming\_validator.py_ - contains class MgramExtractorValidator to check extraction quality.
_remove\_old\_nrgams.py_ - removes all ngrams older than 7 days. Can be used via cron.
_orm\_generate\_and\_fill\_with\_test\_data.py_ - generates databese tables and fills them with test data.
