'''
Created on Nov 11, 2011

@author: Arif
'''

from BeautifulSoup import BeautifulSoup, Comment

def sanitize_html(value):
    '''A paranoid html sanitation'''
    
    valid_tags = ['p', 'i', 'strong', 'b', 'ul', 'ol', 'li', 'a', 'pre', 'br', 'img', 'span', 'blockquote']
    hot_string = ['javascript:', 'vbscript:', 'mocha:', 'livescript:']
    soup = BeautifulSoup(value)
    cleaned_html = value
    
    for comment in soup.findAll(
        text=lambda text: isinstance(text, Comment)):
        comment.extract()
        
    for tag in soup.findAll(True):
        if tag.name not in valid_tags:
            tag.hidden = True
        
        # add rel=nofollow to every link
        if tag.name == 'a':
            tag.attrs.append(('rel', 'nofollow'))
        
        clean_tags = []
        for attr, val in tag.attrs:
            if attr == 'rel' and val == 'nofollow':
                clean_tags.append((attr, val))
            elif attr == 'style' and val == 'text-decoration: line-through; ' and tag.name == 'span':
                clean_tags.append((attr, val))
            elif (attr == 'src' and tag.name == 'img') or (attr == 'href' and tag.name == 'a'):
                # many crazy XSS hack use IMG and A tag as its vector. this makes me nervous and paranoid
                # normalized the href or src attribute value and reject it if it contains any script keyword
                norm_val = val.lower()
                norm_val = ''.join(norm_val.split())
                ok_flags = []
                for keyword in hot_string:
                    if keyword in norm_val:
                        ok_flags.append(False)
                    else:
                        ok_flags.append(True)
                
                if all(ok_flags):
                    clean_tags.append((attr, val))
                
        tag.attrs = clean_tags
        
        cleaned_html = soup.renderContents().decode('utf8')
        for keyword in hot_string:
            cleaned_html.replace(keyword, '')
        
    return cleaned_html
