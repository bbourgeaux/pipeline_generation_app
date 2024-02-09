
import re

with open('headlines.ext', 'r') as f:
    headlines = f.read()

clean_headlines = re.sub(r'\n', '', headlines)

with open('clean_headlines.ext', 'w') as f:
    f.write(clean_headlines)</s>