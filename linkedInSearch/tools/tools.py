from langchain_community.tools.tavily_search import TavilySearchResults

def get_profile_url_tavily(name):
    """Searches for Linkedin page"""
    search = TavilySearchResults()
    res = search.run(name)
    return res

