from flask import Blueprint, render_template, request
import ai21

ai21.api_key = 'MWoMUJbSC3GgrEKx51opEooZW1OGAdOL'
api = Blueprint("api", __name__, template_folder='templates', static_folder='static', static_url_path='api/static')

# @api.route("/", methods=["GET"])
# def home():
    
#     words = get_words('api/snowwhite.txt')
#     write_words(words)
    
#     return render_template("index.html", first_part=words)

@api.route("/", methods=["GET", "POST"])
def select():
    if request.method == "GET":
        words = get_words('api/snowwhite.txt')
        write_words(words)
    
        return render_template("index.html", first_part=words)
    
    print(request.form, flush=True)
    
    if request.form.get('word'):
        word_count = int(request.form.get('word'))
        print(word_count)
        all_words = get_words('api/snowwhite-alternative.txt')
        first_part = all_words[:word_count]
        second_part = all_words[word_count:]
        
        
        # write_words(words)
        
        return render_template("index.html", first_part=first_part, second_part=second_part)
    
    if request.form.get('submit-cut'):
        word_count = int(request.form.get('count'))
        words = get_words('api/snowwhite-alternative.txt')[:word_count]
        
        write_words(words)
        
        return render_template("index.html", first_part=words, add_text=True)
    
    if request.form.get('submit-text'):
        added = request.form.get('text-input')
    
        print(added)
        with open('api/snowwhite-alternative.txt', 'r') as f:
            original = f.read()
        
        if added:
            text = original.strip() + ' ' + added.strip()
        else:
            text = original.strip()
            
        completion = complete(text)
        print(text)
        print('------')
        print(completion)
        with open('api/snowwhite-alternative.txt', 'a') as f:
            f.write(added)
            f.write(completion)
        
        # words = total.split(' ')
        words = get_words('api/snowwhite-alternative.txt')
        
        return render_template("index.html", first_part=words, add_text=False)




def get_words(file: str) -> list:
    with open(file, 'r') as f:
        lines = f.readlines()
        
    words = []
    for line in lines:
        next_words = line.split()
        words.extend(next_words)
        words.append('\n')
    return words

def write_words(words: list) -> None:
    with open('api/snowwhite-alternative.txt', 'w') as f:
        for word in words:
            f.write(word)
            if not word == '\n':
                f.write(' ')
                
def complete(text: str) -> str:
    response = ai21.Completion.execute(
        model='j2-large',
        prompt=text,
        temperature=0.5,
        minTokens=50,
        maxTokens=100,
        numResults=1
    )
    return response.completions[0].data.text.rstrip()