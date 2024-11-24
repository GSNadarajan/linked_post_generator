import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm

def process_posts(raw_file_path, processed_file_path="data/processed_posts.json"):
    enriched_posts = []
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        for post in posts:
            metadata = extract_meta_data(post['text'])
            # Extract the content from AIMessage and parse it to dict
            try:
                json_parser = JsonOutputParser()
                metadata_dict = json_parser.parse(metadata.content)
                post_with_metadata = {**post, **metadata_dict}  # Merge dictionaries
                enriched_posts.append(post_with_metadata)
            except Exception as e:
                print(f"Error processing post: {e}")
            
    for en_post in enriched_posts:
        print(en_post)
        
def extract_meta_data(post):
    template = ''' 
    You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble.
    2. JSON object should have exactly three keys: line_count, language and tags.
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Hinglish (Hinglish means hindi + english)
    
    Here is the actual post on which you need to perform this task:
    {post}
    '''
    
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={'post': post})
    return response
    
if __name__ == '__main__':
    process_posts('data/raw_posts.json', 'data/processed_posts.json')