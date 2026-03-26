import pandas as pd
import os

files = ['Dataset Phising Website.csv', 'email.csv', 'india_fraud_detection_FINAL.csv', 'phishing.csv', 'spam.csv']
with open('eda_output.txt', 'w', encoding='utf-8') as out:
    for f in files:
        path = os.path.join('Datasets', f)
        try:
            df = pd.read_csv(path, encoding='utf-8')
        except:
            df = pd.read_csv(path, encoding='latin-1')
        out.write('='*50 + '\n')
        out.write(f'FILE: {f}\n')
        
        # Capture info
        import io
        buf = io.StringIO()
        df.info(buf=buf)
        out.write(buf.getvalue() + '\n')
        
        out.write('\nMissing Values:\n')
        out.write(df.isna().sum().sort_values(ascending=False).head(3).to_string() + '\n')
        out.write('\nHead:\n')
        out.write(df.head(2).to_string() + '\n')
        
        target_cols = [c for c in df.columns if 'label' in c.lower() or 'class' in c.lower() or 'fraud' in c.lower() or 'spam' in c.lower() or 'result' in c.lower() or 'target' in c.lower() or 'status' in c.lower()]
        if target_cols:
            out.write(f'\nTarget Variable count for {target_cols[0]}:\n')
            out.write(df[target_cols[0]].value_counts(dropna=False).to_string() + '\n')
