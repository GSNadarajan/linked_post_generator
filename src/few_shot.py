import pandas as pd
import json

class FewShotPosts:
   def __init__(self, file_path="data/processed_posts.json"):
       print("\n🚀 Initializing FewShotPosts...")
       self.df = None
       self.unique_tags = None
       self.load_posts(file_path)
       
   def load_posts(self, file_path):
       print(f"📂 Loading posts from: {file_path}")
       with open(file_path, encoding="utf-8") as f:
           posts = json.load(f)
           print(f"✅ Loaded {len(posts)} posts successfully")
           
           self.df = pd.json_normalize(posts)
           print(f"📊 Created DataFrame with columns: {list(self.df.columns)}")
           
           self.df['length'] = self.df['line_count'].apply(self.categorize_length)
           print("📏 Added length categories (Short/Medium/Long)")
           
           all_tags = self.df['tags'].apply(lambda x: x).sum()
           self.unique_tags = list(set(all_tags))
           print(f"🏷️  Found {len(self.unique_tags)} unique tags: {self.unique_tags}")

   def get_filtered_posts(self, length, language, tag):
       print(f"\n🔍 Filtering posts with criteria:")
       print(f"   Length: {length}")
       print(f"   Language: {language}")
       print(f"   Tag: {tag}")
       
       df_filtered = self.df[
           (self.df['tags'].apply(lambda tags: tag in tags)) &
           (self.df['language'] == language) &
           (self.df['length'] == length)
       ]
       
       filtered_posts = df_filtered.to_dict(orient='records')
       print(f"✨ Found {len(filtered_posts)} matching posts")
       return filtered_posts

   def categorize_length(self, line_count):
       if line_count < 5:
           return "Short"
       elif 5 <= line_count <= 10:
           return "Medium"
       else:
           return "Long"

   def get_tags(self):
       return self.unique_tags

if __name__ == "__main__":
   fs = FewShotPosts()
   
   print("\n📊 Data Overview:")
   print(f"Total posts: {len(fs.df)}")
   print(f"Languages: {fs.df['language'].unique()}")
   print(f"Length categories: {fs.df['length'].unique()}")
   
   posts = fs.get_filtered_posts("Medium", "Hinglish", "Job Search")
   
   print("\n📝 Filtered Posts:")
   for i, post in enumerate(posts, 1):
       print(f"\nPost {i}:")
       print(f"Text: {post['text'][:100]}...")
       print(f"Language: {post['language']}")
       print(f"Length: {post['length']}")
       print(f"Tags: {post['tags']}")