from duckduckgo_search import DDGS
from llama_index.core.tools import FunctionTool
import time
import backoff  # You'll need to: pip install backoff

@backoff.on_exception(
    backoff.expo,
    Exception,
    max_tries=3,
    max_time=10
)
def web_search(query):
    """
    Perform a web search using DuckDuckGo and return the results.

    Args:
        query (str): The search query.
        max_results (int): The maximum number of results to return.

    Returns:
        str: Concatenated search result snippets
    """
    # Increase sleep time to avoid rate limiting
    time.sleep(2)
    
    with DDGS() as ddgs:
        try:
            results = list(ddgs.text(query, max_results=5))
            if not results:
                return "No results found."
            return '\n'.join([result['body'] for result in results])
        except Exception as e:
            if "429" in str(e) or "rate" in str(e).lower():
                return "Search failed: Rate limit reached. Please try again in a few seconds."
            return f"Search failed: {str(e)}"

web_tool = FunctionTool.from_defaults(
    fn=web_search,
    name="web_search",
    description="Searches the web and provides results for a given query. Note: Requires a 2-second delay between searches."
)

# from duckduckgo_search import DDGS
# from llama_index.core.tools import FunctionTool
# import time

# def web_search(query, max_results=5):
#     """
#     Perform a web search using DuckDuckGo and return the results.

#     Args:
#         query (str): The search query.
#         max_results (int): The maximum number of results to return.

#     Returns:
#         str: Concatenated search result snippets
#     """
#     time.sleep(1)
#     with DDGS() as ddgs:
#         try:
#             results = list(ddgs.text(query, max_results=max_results))
#             return '\n'.join([result['body'] for result in results])
#         except Exception as e:
#             return f"Search failed: {str(e)}"

# web_tool = FunctionTool.from_defaults(
#     fn=web_search,
#     name="web_search",
#     description="Searches the web and provides results for a given query"
# )

if __name__ == "__main__":
    query = "Who is the current President of the United States?"
    search_results = web_search(query, max_results=5)
    print(search_results)