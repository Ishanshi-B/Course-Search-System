#####
# Name: query_parser.py
# Date: 2/28/2026
# Description: This is the smart layer that parses multiple intents from a natural language query and generates a structured query that can be used to search the course index. It uses a combination of regex, keyword matching, and NLP techniques to identify the user's intent and extract relevant information from the query.
#####

import re

def parse_query_intent(query: str) -> dict:
    """
    Extract structured intent from a natural language query. 
    Returns: topic hints, max duration, preferred format, level
    """
    query_lower = query.lower()
    intent = {
        "raw_query": query,
        "max_duration": None,
        "preferred_format": None,
        "preferred_level": None,
        "filters_applied": []
    }

    #duration parsing 
    # look for duration in the query using regex, e.g., "under 30 minutes", "less than 1 hour", "max 45 mins"
    duration_patterns = [
        (r"(\d+)\s*min", lambda m: int(m.group(1))), #the regex pattern looks for a number followed by min and captures the number as the duration in minutes
        (r"(\d+)\s*hour", lambda m: int(m.group(1)) * 60), #the regex pattern looks for a number followed by hour and captures the number as the duration in hours, then converts it to minutes
        (r"\bquick\b|\bshort\b|\bbrief\b", lambda m: 15),  # the regex pattern looks for the words quick, short, or brief and assigns a default duration of 15 minutes
        (r"\blong\b|\bin[- ] depth\b|\bcomprehensive\b", lambda m: 999)  # the regex pattern looks for the words long, in-depth, or comprehensive and assigns a default duration of 999 minutes (effectively no limit)
    ]

    # We are iterating through the duration patterns and applying the regex to the query to extract the duration if it matches any of the patterns. 
    # If a match is found, we extract the duration using the corresponding extractor function and store it in the intent dictionary. 
    # We also append a filter description to the filters_applied list in the intent dictionary for reference.
    for pattern, extractor in duration_patterns:
        match = re.search(pattern, query_lower)
        if match:
            intent["max_duration"] = extractor(match) # this essentially extracts the duration from the query and stores it in the intent dictionary
            intent["filters_applied"].append(f"duration <= {intent['max_duration']} min") #this appends the extracted duration filter to the filters_applied list in the intent dictionary
            break  # stop after the first match

    format_map = {
        "video": "video lectures",
        "watch": "video lectures",
        "read": "article",
        "article": "article",
        "practice": "interactive workshops",
        "exercise": "interactive workshops",
        "hands[- ]on": "interactive workshops",
        "quiz": "quiz",
        "workshop": "workshop"    
    }
    # We are iterating through the format_map dictionary and applying regex to the query to identify if any of the keywords related to course formats are present in the query.
    # If a match is found, we store the corresponding format in the intent dictionary and append a filter description to the filters_applied list in the intent dictionary for reference.
    for keyword, fmt in format_map.items():
        if re.search(rf"\b{keyword}\b", query_lower):
            intent["preferred_format"] = fmt # This assigns the preferred format based on the matched keyword from the query to the intent dictionary
            intent["filters_applied"].append(f"format = {fmt}")
            break

    # -- Level parsing -- 
    level_map = {
        r"\bbeginner\b|\bbasic[s]?\b|\bintro\b|\bstart\b|\bnew to\b": "beginner",
        r"\bintermediate\b|\bsome experience\b": "intermediate",
        r"\badvanced\b|\bexpert\b|\bdeep dive\b": "advanced"
    }

    for pattern, level in level_map.items():
        if re.search(pattern, query_lower):
            intent["preferred_level"] = level # This assigns the preferred level based on the matched pattern from the query to the intent dictionary
            intent["filters_applied"].append(f"level = {level}")
            break


    return intent