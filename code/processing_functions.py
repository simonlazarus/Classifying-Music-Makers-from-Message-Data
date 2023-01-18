import re
from nltk.stem.porter import PorterStemmer

def website_name(url):
    '''
    Input: A webiste URL
    Output: the name of that website, followed by "link." For example,
        'http://www.hello.com/hi' returns 'hellolink'.
    If the website doesn't have one of the standard URL endings listed in
    ending_bases in the definition of this function, then this simply returns
    'unknownlink'.
    '''
    
    endings_bases = ['com', 'net', 'org', 'gov', 'io', 'co']
    endings = [f".{x}"+r'(\W|$)' for x in endings_bases]
    #The e.g. ".com" must be followed by either the end of the string OR a
    #non-alphanumeric character.  This is to make sure that we
    #capture the .com from something.com or something.com/else, but not the
    #"comcast" in help.comcast.net
    
    ending_pos = -1
    #Initialize in case we can't find any of these endings in the URL
    
    for ending in endings:
        #Look for these endings in the url
        if bool(re.search(ending, url)):
            ending_pos = re.search(ending, url).start()
            break
            #If you found it, remember its position and break out
        else:
            continue
            #If you didn't find this one, try the next kind of ending
    
    #If we can't find an ending, just return 'unknownlink'
    if ending_pos == -1:
        return 'unknownlink'
    
    #Otherwise, take everything after the last '.' before this ending
    before_ending = url[:ending_pos]
    parts_of_url = before_ending.split('.')
    return parts_of_url[-1]+'link'




def replace_urls(text):
    url_pattern = '(?:https?:\/\/|www\.)\S+'
    #Regex pattern for something beginning with http://, https://, or www.
    #We need to put a '?:' after the first '(' in the () group so that re
    #captures the WHOLE pattern and not just the group in the ().

    text = re.sub(url_pattern, lambda x : website_name(x.group()),text)
    # .group just gets this instance of the text that was found by the pattern
    
    return text





def url_preprocessor(text):
    '''
    Converts text to lowercase then replaces URLs with the names of the sites followed by "link".
    '''
    text = text.lower()
    text = replace_urls(text)
    
    return text





def stem_processor(text):
    words = re.split('\s+', text)
    ps = PorterStemmer()
    words_stemmed = [ps.stem(x) for x in words]
    text = " ".join(words_stemmed)
    return text