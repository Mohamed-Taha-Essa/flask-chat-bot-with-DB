from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os
from langchain_community.utilities import SQLDatabase  
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit



from sqlalchemy import create_engine,inspect    
from app.db.database import engine    
from app.db.database import get_db_session
from app.core.config import settings
load_dotenv()


# Create LLM object
# All free-tier HF models are registered as "conversational" only,
# so we use ChatHuggingFace wrapper which is compatible with create_sql_agent
_endpoint = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-72B-Instruct",
    task="conversational",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    max_new_tokens=512,
    do_sample=False,
    provider="novita",
)
llm = ChatHuggingFace(llm=_endpoint)

def initialize_sql_agent():
    #create inspector to get tables name 
    inspector = inspect(engine)
    #get list of table name 
    existing_tables = inspector.get_table_names()

    availabel_tables = existing_tables
    #create  langchain  sql database object with tables names only for security
    sql_db = SQLDatabase.from_uri(
        settings.DATABASE_URL, 
        sample_rows_in_table_info=3,        
        include_tables=existing_tables) 

    
    #create toolkit 
    toolkit = SQLDatabaseToolkit(db=sql_db , llm=llm)

    #create prompt template 
    system_prompt = f""" 
You are a helpful assistant who can answer questions about database.
Use the following tools to answer questions.
Always use the tools to get the answer.
CRITICAL INSTRUCTION:
1. NEVER MENTION DATABASE SQL QUERY OR SCHEMA OR TABLE OR DATABASE IN YOUR ANSWER
2. NEVER GIVE ANY TECHNICAL INFORMATION ABOUT THE DATABASE
3. ALWAYS ANSWER IN SIMPLE AND FRIENDLY LANGUAGE
4. IF USER ASK ABOUT SOMETHING THAT YOU DON'T HAVE ANSWER USE "I DON'T HAVE ANSWER FOR THIS QUESTION"
5. USE EMOJIS  AND CLEAR STRUCTURE FOR ANSWER 
6.
AVAILABLE_TABLES : {availabel_tables}

RESPONSE TEMPLATE :
- FOR COUNTS: **METRICS**: [NUMBER] **VALUE**: [COUNT_VALUE]
- FOR PERCENTAGES: **METRICS**: [NUMBER] **VALUE**: [PERCENTAGE_VALUE]
- FOR VALUEES : **METRICS**: [NUMBER] **VALUE**: [VALUE]    
- FOR REVENUES : **METRICS**: [NUMBER] **VALUE**: [AMOUNT]      
- FOR PROFIT : **METRICS**: [NUMBER] **VALUE**: [AMOUNT]      

    """
    
    #CREATE sql agent 
    sql_agent =create_sql_agent(
    llm=llm , 
    toolkit=toolkit , 
    system_prompt=system_prompt , 
    verbose=True , 
    )

    return sql_agent

