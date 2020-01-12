# %%
import pandas as pd
import math
import re
df = pd.read_csv('words.tsv', sep="\t")
#df.fillna('')
df.loc[df['pos']=="adv",'pos'] = 'adverb'

# %%
POS = set(x.strip().lower() for xs in df['pos'] if isinstance(
    xs, str) for x in re.sub(r'\[.+?\]', '', xs).split(";"))
print(POS)
POS = set(x.split(" ")[-1] for x in POS)
print(POS)


def main(pos):
    f = open(f"out/words_{pos}.md", 'w', encoding='utf-8', newline="\n")
    count = 1
    for k, row in df.iterrows():
        word_pos = re.sub(r'\[.+?\]', '', str(row['pos']))
        if not re.search(rf'\b{pos}\b', word_pos):
            continue
        gw = row['gw'] if isinstance(row['gw'], str) else ''
        print(f"## {count}. {row['word']} ## {row['pos']}", file=f)
        print(f"{row['pron']} {gw}", file=f)
        print(f"[{row['freq']}]{row['def']}", file=f)
        if isinstance(row['example'], str):
            for e in row['example'].split("|"):
                print(f'- {e}', file=f)
        print("", file=f)
        count += 1
    f.close()


for pos in POS:
    main(pos)

# %%
