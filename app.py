from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def get_posts():
    """Helper function: Reads the Data and returns it"""

    try:
        with open("data.json", "r") as file:
            blog_posts = json.load(file)

        return blog_posts

    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_posts(blog_posts):
    """Helpfer function: Saves the new Posting-Data in our json file"""

    try:
        with open("data.json", "w") as file:
            json.dump(blog_posts, file, indent=4)

    except OSError:
        return None

@app.route('/')
def index():
    """Shows the user the 'landing-page'. Where he can see all the posts and options"""

    #Get all the blog_posts
    blog_posts = get_posts()
    if blog_posts is None:
        return "We had an Error handling this file", 404

    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Adds a new blog-post to our blog"""

    if request.method == 'POST':
        #Read the file
        blog_posts = get_posts()
        if blog_posts is None:
            return "We had an Error handling this file", 404

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
        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route("/delete/<int:post_id>")
def delete(post_id):
    """Deletes a post from our blog"""

    #Get the data
    blog_posts = get_posts()
    if blog_posts is None:
        return "We had an Error handling this file", 404

    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    save_posts(blog_posts)

    return redirect(url_for('index'))

def fetch_post_by_id(post_id):
    """Helper function to get the right post by id"""

    #Get the data
    blog_posts = get_posts()
    if blog_posts is None:
        return None

    for post in blog_posts:
        if post["id"] == post_id:
            return post
    return None


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Updates a post with new data, everything which is not updated
    will remain the same"""

    #Get the searched post
    post = fetch_post_by_id(post_id)

    #Get the data
    blog_posts = get_posts()
    if blog_posts is None:
        return "We had an Error handling this file", 404

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        for blog_post in blog_posts:
            if blog_post["id"] == post_id:
                blog_post["author"] = author or blog_post["author"]
                blog_post["title"] = title or blog_post["title"]
                blog_post["content"] = content or blog_post["content"]

        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)





