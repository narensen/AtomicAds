from config import *

tavilly_search = search_tool("Naren Sengodan")
result = tavilly_search.invoke({"query" : "AlphaEvolve vs AlphaEvolve-lite which is better"})

print(result["results"][1]["content"])