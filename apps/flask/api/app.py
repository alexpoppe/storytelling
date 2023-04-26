from flask import Blueprint, render_template, request

api = Blueprint("api", __name__, template_folder='templates', static_folder='static', static_url_path='api/static')

@api.route("/", methods=["GET"])
def home():
    
    words = get_words('api/snowwhite.txt')
    write_words(words)
    
    return render_template("index.html", words=words)

@api.route("/select", methods=["POST"])
def select():
    print(request.form, flush=True)
    
    if request.form.get('word'):
        word_count = int(request.form.get('word'))
        words = get_words('api/snowwhite-alternative.txt')[:word_count]
        write_words(words)
        
        return render_template("index.html", words=words, add_text=True)

    text_input = request.form.get('text-input')
    with open('api/snowwhite-alternative.txt', 'a') as f:
        f.write(text_input)
    
    words = get_words('api/snowwhite-alternative.txt')
    return render_template("index.html", words=words, add_text=False)




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