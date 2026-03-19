from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open("data.json", "r") as file:
        blog_posts = json.load(file)
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        #Read the file
        with open("data.json", "r") as file:
            blog_posts = json.load(file)

        #Get the information from the Form
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        #Create new dict with the info
        new_dict = {
            "id" : len(blog_posts) + 1,
            "author" : author,
            "title" : title,
            "content" : content
        }

        #Add the info to our json data
        blog_posts.append(new_dict)

        #Write new file with updated info
        with open("data.json", "w") as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)