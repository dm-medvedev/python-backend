from papers.models import Paper
import pandas as pd
import datetime

table = pd.read_csv('./articles_data.csv', nrows = 10)
columns = {c: i for i, c in enumerate(table.columns)}
for vals in table.values[:10]:
    Paper.objects.create(source_name = vals[columns['source_name']], 
                         author = vals[columns['author']],
                         title = vals[columns['title']],
                         url = vals[columns['url']],
                         description = vals[columns['description']], 
                         published_at = datetime.datetime.strptime(
                            vals[columns['published_at']], "%Y-%m-%dT%H:%M:%SZ").date(),
                        )
