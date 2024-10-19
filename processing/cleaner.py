import re

class cleaner:
    def clean(text: str) -> str:  

        r1 = r'\w{1}no .*\w{1}'
        r2 = r'not? .*'
        r3 = r'.*safety goggles.*'
        if (m := re.match(r3, text)):
            print(m.group(0))

        # TODO: clean? 
        return text
    
        # remove redacted text
        text = re.sub(r'\[.*?\]', '', text)

        return text
        