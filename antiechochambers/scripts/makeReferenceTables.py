import pandas as pd

d = """Art+AskReddit+DIY+Documentaries+EarthPorn+Futurology+GetMotivated+IAmA+
InternetIsBeautiful+Jokes+LifeProTips+Music+OldSchoolCool+Showerthoughts+TwoXChromosomes+
UpliftingNews+WritingPrompts+announcements+askscience+aww+blog+books+creepy+
dataisbeautiful+explainlikeimfive+food+funny+gadgets+gaming+gifs+history+listentothis
+mildlyinteresting+movies+news+nosleep+nottheonion+personalfinance+philosophy+
photoshopbattles+pics+science+space+sports+television+tifu+todayilearned+
videos+worldnews""".split('+')


defaults = pd.Series(d)
defaults.names = 'defaults'
saveSQL(defaults,table_name='defaults',database_name='reference')

query = """SELECT*
                 FROM `aerobic-datum-126519.sms_18_sample_subreddits.skipAuthors`
                 """

skipAuthors = fetchQuery(query)


skipAuthors = skipAuthors['string_field_1']
skipAuthors = skipAuthors.append(pd.Series('JlmmyButler')).reset_index(drop=True)
saveSQL(skipAuthors, table_name='skipAuthors',database_name='reference')