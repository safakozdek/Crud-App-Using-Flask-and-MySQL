from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='app_test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)


@app.route('/')
def login():
    return render_template("index.html")


@app.route('/homeAdmin')
def home_admin():
    return render_template("home_admin.html")


@app.route('/homeUser')
def home_user():
    return render_template("home_user.html")


@app.route('/addPapers')
def add_papers_page():
    return render_template("add_papers.html", success='')


@app.route('/addAuthors')
def add_authors_page():
    return render_template("add_authors.html", success='')


@app.route('/addTopics')
def add_topics_page():
    return render_template("add_topics.html", success='')


@app.route('/addAuthorReq', methods=['GET'])
def add_author():
    name = request.args.get('name').strip()
    surname = request.args.get('surname').strip()
    if name == '' or surname == '':
        return render_template("add_authors.html", success='Name or Surname cannot be empty')
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `author` (`name`, `surname`) VALUES (%s, %s)"
            cursor.execute(sql, (name, surname))
            return render_template("add_authors.html", success='Successful')
    except Exception as e:
        return render_template("add_authors.html", success='Can\'t add Author: ' + str(e))


@app.route('/addTopicReq', methods=['GET'])
def add_topic():
    name = request.args.get('name').strip()
    if name == '':
        return render_template("add_topics.html", success='Name cannot be empty')
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `topic` (`name`, `sota`, `sota_paper_id`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, 0, -1))
            return render_template("add_topics.html", success='Successful')
    except Exception as e:
        return render_template("add_topics.html", success='Can\'t add Topic: ' + str(e))


@app.route('/addPaperReq', methods=['GET'])
def add_paper():
    title = request.args.get('title').strip()
    authors = request.args.get('authors').strip()
    abstract = request.args.get('abstract').strip()
    topics = request.args.get('topics').strip()
    result = request.args.get('result').strip()
    if title == '' or authors == '' or abstract == '' or topics == '' or result == '':
        return render_template("add_papers.html", success='Please fill all fields.')
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `paper`(`title`, `abstract`, `result`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (title, abstract, result))

            sql = "SELECT id FROM `paper` WHERE `title` = %s"
            cursor.execute(sql, title)
            result = cursor.fetchone()
            paper_id = result["id"]

            authors = authors.split(',')
            for x in authors:
                author = x.split()
                name = author[0].strip()
                surname = author[1].strip()

                sql = "SELECT id FROM `author` WHERE `name` = %s AND `surname` = %s"
                cursor.execute(sql, (name, surname))
                result = cursor.fetchone()
                author_id = result["id"]

                sql = "INSERT INTO `author_paper`(`author_id`, `paper_id`) VALUES (%s, %s)"
                cursor.execute(sql, (author_id, paper_id))

            topics = topics.split(',')
            for topic in topics:
                topic = topic.strip()

                sql = "SELECT id FROM `topic` WHERE `name` = %s"
                cursor.execute(sql, topic)
                result = cursor.fetchone()
                topic_id = result["id"]

                sql = "INSERT INTO `topic_paper`(`topic_id`, `paper_id`) VALUES (%s, %s)"
                cursor.execute(sql, (topic_id, paper_id))

            return render_template("add_papers.html", success='Successful')
    except Exception as e:
        return render_template("add_papers.html", success='Can\'t add Paper: ' + str(e))


@app.route('/updatePapers')
def update_papers_page():
    return render_template("update_papers.html", success='')


@app.route('/updateAuthors')
def update_authors_page():
    return render_template("update_authors.html", success='')


@app.route('/updateTopics')
def update_topics_page():
    return render_template("update_topics.html", success='')


@app.route('/updateAuthorReq', methods=['GET'])
def update_author():
    old_name = request.args.get('old_name').strip()
    old_surname = request.args.get('old_surname').strip()
    new_name = request.args.get('new_name').strip()
    new_surname = request.args.get('new_surname').strip()
    if old_name == '' or old_surname == '' or new_name == '' or new_surname == '':
        return render_template("update_authors.html", success='Fields cannot be empty')
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE `author` SET `name`=%s,`surname`=%s WHERE `name`=%s AND `surname`=%s"
            cursor.execute(sql, (new_name, new_surname, old_name, old_surname))
            return render_template("update_authors.html", success='Successful')
    except Exception as e:
        return render_template("update_authors.html", success='Can\'t update Author: ' + str(e))


@app.route('/updateTopicReq', methods=['GET'])
def update_topic():
    old_name = request.args.get('old_name').strip()
    new_name = request.args.get('new_name').strip()

    if old_name == '' or new_name == '':
        return render_template("update_topics.html", success='Fields cannot be empty')
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE `topic` SET `name`=%s WHERE `name`=%s"
            cursor.execute(sql, (new_name, old_name))
            return render_template("update_topics.html", success='Successful')
    except Exception as e:
        return render_template("update_topics.html", success='Can\'t update Topic: ' + str(e))


@app.route('/updatePaperReq', methods=['GET'])
def update_paper():
    old_title = request.args.get('old_title').strip()
    title = request.args.get('title').strip()
    authors = request.args.get('authors').strip()
    abstract = request.args.get('abstract').strip()
    topics = request.args.get('topics').strip()
    result = request.args.get('result').strip()

    if old_title == '' or title == '' or authors == '' or abstract == '' or topics == '' or result == '':
        return render_template("add_papers.html", success='Please fill all fields.')
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE `paper` SET `title`=%s,`abstract`=%s,`result`=%s WHERE `title`=%s"
            cursor.execute(sql, (title, abstract, result, old_title))

            sql = "SELECT id FROM `paper` WHERE `title` = %s"
            cursor.execute(sql, title)
            result = cursor.fetchone()
            paper_id = result["id"]

            sql = "DELETE FROM `author_paper` WHERE `paper_id`=%s"
            cursor.execute(sql, paper_id)
            sql = "DELETE FROM `topic_paper` WHERE `paper_id`=%s"
            cursor.execute(sql, paper_id)

            authors = authors.split(',')
            for x in authors:
                author = x.split()
                name = author[0].strip()
                surname = author[1].strip()

                sql = "SELECT id FROM `author` WHERE `name` = %s AND `surname` = %s"
                cursor.execute(sql, (name, surname))
                result = cursor.fetchone()
                author_id = result["id"]

                sql = "INSERT INTO `author_paper`(`author_id`, `paper_id`) VALUES (%s, %s)"
                cursor.execute(sql, (author_id, paper_id))

            topics = topics.split(',')
            for topic in topics:
                topic = topic.strip()

                sql = "SELECT id FROM `topic` WHERE `name` = %s"
                cursor.execute(sql, topic)
                result = cursor.fetchone()
                topic_id = result["id"]

                sql = "INSERT INTO `topic_paper`(`topic_id`, `paper_id`) VALUES (%s, %s)"
                cursor.execute(sql, (topic_id, paper_id))

            return render_template("update_papers.html", success='Successful')
    except Exception as e:
        return render_template("update_papers.html", success='Can\'t update Paper: ' + str(e))


@app.route('/deletePapers')
def delete_papers_page():
    return render_template("delete_papers.html", success='')


@app.route('/deleteAuthors')
def delete_authors_page():
    return render_template("delete_authors.html", success='')


@app.route('/deleteTopics')
def delete_topics_page():
    return render_template("delete_topics.html", success='')


@app.route('/deleteAuthorReq', methods=['GET'])
def delete_author():
    name = request.args.get('name').strip()
    surname = request.args.get('surname').strip()
    if name == '' or surname == '':
        return render_template("delete_authors.html", success='Name or Surname cannot be empty')
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id FROM `topic` WHERE `name` = %s AND `surname` = %s"
            cursor.execute(sql, (name, surname))
            result = cursor.fetchone()
            author_id = result["id"]

            sql = "DELETE FROM `author_paper` WHERE `author_id`=%s"
            cursor.execute(sql, author_id)

            sql = "DELETE FROM `author` WHERE `name`=%s AND `surname`=%s"
            cursor.execute(sql, (name, surname))

            return render_template("delete_authors.html", success='Successful')
    except Exception as e:
        return render_template("delete_authors.html", success='Can\'t add Author: ' + str(e))


@app.route('/deleteTopicReq', methods=['GET'])
def delete_topic():
    name = request.args.get('name').strip()
    if name == '':
        return render_template("delete_topics.html", success='Name cannot be empty')
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id FROM `topic` WHERE `name` = %s"
            cursor.execute(sql, name)
            result = cursor.fetchone()
            topic_id = result["id"]

            sql = "DELETE FROM `topic_paper` WHERE `topic_id`=%s"
            cursor.execute(sql, topic_id)

            sql = "DELETE FROM `topic` WHERE `name`=%s"
            cursor.execute(sql, name)

            return render_template("delete_topics.html", success='Successful')
    except Exception as e:
        return render_template("delete_topics.html", success='Can\'t add Topic: ' + str(e))


@app.route('/deletePaperReq', methods=['GET'])
def delete_paper():
    title = request.args.get('title').strip()
    if title == '':
        return render_template("delete_papers.html", success='Title cannot be empty')
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id FROM `paper` WHERE `title` = %s"
            cursor.execute(sql, title)
            result = cursor.fetchone()
            paper_id = result["id"]

            sql = "DELETE FROM `author_paper` WHERE `paper_id`=%s"
            cursor.execute(sql, paper_id)

            sql = "DELETE FROM `topic_paper` WHERE `paper_id`=%s"
            cursor.execute(sql, paper_id)

            sql = "DELETE FROM `paper` WHERE `title`=%s"
            cursor.execute(sql, title)

            return render_template("delete_papers.html", success='Successful')
    except Exception as e:
        return render_template("delete_papers.html", success='Can\'t delete paper: ' + str(e))


@app.route('/viewPapers')
def view_papers_page():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT DISTINCT paper.id, title, abstract, result, " \
                  "GROUP_CONCAT(DISTINCT \' \', `author`.name, \' \', `author`.surname) as authors, " \
                  "GROUP_CONCAT(DISTINCT `topic`.name) as topics " \
                  "FROM `paper` " \
                  "JOIN `author_paper` ON `paper`.id = `author_paper`.paper_id " \
                  "JOIN `topic_paper` ON `paper`.id = `topic_paper`.paper_id " \
                  "JOIN `author` ON author_id = `author`.id " \
                  "JOIN `topic` ON `topic`.id = topic_id " \
                  "GROUP BY paper.id"
            cols = ['id', 'title', 'abstract', 'result', 'authors', 'topics']
            cursor.execute(sql)
            result = cursor.fetchall()
            return render_template("view_papers.html", items=result, cols=cols, success='')
    except Exception as e:
        return render_template("view_papers.html", items=[], cols=[], success='Can\'t view Papers: ' + str(e))


@app.route('/viewAuthors')
def view_authors_page():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `author`"
            cols = ['id', 'name', 'surname']
            cursor.execute(sql)
            result = cursor.fetchall()
            return render_template("view_authors.html", items=result, cols=cols, success='')
    except Exception as e:
        return render_template("view_authors.html", items=[], cols=[], success='Can\'t view Authors: ' + str(e))


@app.route('/viewTopics')
def view_topics_page():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `topic`"
            cols = ['id', 'name', 'sota']
            cursor.execute(sql)
            result = cursor.fetchall()
            return render_template("view_topics.html", items=result, cols=cols, success='')
    except Exception as e:
        return render_template("view_topics.html", items=[], cols=[], success='Can\'t view Topics: ' + str(e))


@app.route('/papersOfAuthorReq', methods=['GET'])
def view_papers_of_author():
    name = request.args.get('name').strip()
    surname = request.args.get('surname').strip()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT paper.id, paper.title, paper.abstract, paper.result, " \
                  "GROUP_CONCAT(DISTINCT topic.name) as topics " \
                  "FROM `author` " \
                  "JOIN `author_paper` ON author_id = author.id AND author.name = %s and author.surname =%s " \
                  "JOIN `paper`ON author_paper.paper_id = paper.id " \
                  "JOIN `topic_paper` ON topic_paper.paper_id = paper.id " \
                  "JOIN `topic` ON topic.id = topic_paper.topic_id " \
                  "GROUP BY paper.id"
            cols = ['id', 'title', 'abstract', 'result', 'topics']
            cursor.execute(sql, (name, surname))
            result = cursor.fetchall()
            return render_template("view_papers_of_author.html", items=result, cols=cols, success='')
    except Exception as e:
        return render_template("view_papers_of_author.html", items=[], cols=[], success='Can\'t view Papers: ' + str(e))


@app.route('/viewPapersOfAuthor')
def view_papers_of_author_page():
    return render_template("papers_of_author.html")


@app.route('/papersOfTopicReq', methods=['GET'])
def view_papers_of_topic():
    name = request.args.get('name').strip()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT paper.id, paper.title, paper.abstract, paper.result, " \
                  "GROUP_CONCAT(DISTINCT ' ', `author`.name, ' ', `author`.surname) as authors " \
                  "FROM `author` " \
                  "JOIN `author_paper` ON author_id = author.id " \
                  "JOIN `paper` on author_paper.paper_id = paper.id " \
                  "JOIN `topic_paper` on topic_paper.paper_id = paper.id " \
                  "JOIN `topic` on topic.id = topic_paper.topic_id AND topic.name=%s " \
                  "GROUP BY paper.id"
            cols = ['id', 'title', 'abstract', 'result', 'authors']
            cursor.execute(sql, name)
            result = cursor.fetchall()
            return render_template("view_papers_of_topic.html", items=result, cols=cols, success='')
    except Exception as e:
        return render_template("view_papers_of_topic.html", items=[], cols=[], success='Can\'t view Papers: ' + str(e))


@app.route('/viewPapersOfTopic')
def view_papers_of_topic_page():
    return render_template("papers_of_topic.html")


@app.route('/viewCoAuthorsPage')
def view_coauthors_page():
    return render_template("co_author_page.html")


@app.route('/coAuthorsOfAuthor', methods=['GET'])
def view_coauthors_of_author():
    name = request.args.get('name').strip()
    surname = request.args.get('surname').strip()
    try:
        with connection.cursor() as cursor:
            sql = "CALL `CoAuthors`(%s,%s);"
            cols = ['id', 'name', 'surname']
            cursor.execute(sql, (name, surname))
            result = cursor.fetchall()
            return render_template("view_authors.html", items=result, cols=cols, success='')
    except Exception as e:
        return render_template("view_authors.html", items=[], cols=[], success='Can\'t view Co-Authors: ' + str(e))


@app.route('/searchReq', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    try:
        with connection.cursor() as cursor:
            sql = "SELECT DISTINCT paper.id, title, abstract, result, " \
                  "GROUP_CONCAT( DISTINCT ' ', `author`.name, ' ', `author`.surname ) AS authors, " \
                  "GROUP_CONCAT(DISTINCT `topic`.name) AS topics " \
                  "FROM `paper` " \
                  "JOIN `author_paper` ON `paper`.id = `author_paper`.paper_id " \
                  "JOIN `topic_paper` ON `paper`.id = `topic_paper`.paper_id " \
                  "JOIN `author` ON author_id = `author`.id " \
                  "JOIN `topic` ON `topic`.id = topic_id " \
                  "AND (paper.title LIKE '%" + keyword + "%' OR paper.abstract LIKE '%" + keyword + "%') " \
                  "GROUP BY paper.id"
            cols = ['id', 'title', 'abstract', 'result', 'authors', 'topics']
            cursor.execute(sql)
            result = cursor.fetchall()
            return render_template("view_papers.html", items=result, cols=cols, success='')
    except Exception as e:
        return render_template("view_papers.html", items=[], cols=[], success='Can\'t view Papers: ' + str(e))


@app.route('/search', methods=['GET'])
def search_page():
    return render_template("search.html", success='')


@app.route('/rankAuthors', methods=['GET'])
def rank_authors():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT author.id, author.name, author.surname, COUNT(topic.sota) as sota_count FROM `author` " \
                  "JOIN `author_paper` ON author.id = author_id " \
                  "JOIN `paper` ON author_paper.paper_id = paper.id " \
                  "JOIN `topic_paper` ON paper.id = topic_paper.paper_id " \
                  "JOIN `topic` ON topic_id = topic.id AND topic.sota_paper_id = paper.id GROUP BY author.id"
            cols = ['id', 'name', 'surname', 'sota_count']
            cursor.execute(sql)
            result = cursor.fetchall()
            return render_template("rank_authors.html", items=result, cols=cols, success='')
    except Exception as e:
        return render_template("rank_authors.html", items=[], cols=[], success='Can\'t view Authors: ' + str(e))


@app.route('/sotaByTopic', methods=['GET'])
def sota_by_topic():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT topic.id, topic.name, topic.sota, paper.title FROM `paper` " \
                  "JOIN `topic_paper` ON paper.id = topic_paper.paper_id " \
                  "JOIN `topic` ON topic_id = topic.id AND topic.sota_paper_id = paper.id " \
                  "GROUP BY topic.id"
            cols = ['id', 'name', 'sota', 'title']
            cursor.execute(sql)
            result = cursor.fetchall()
            return render_template("sota_by_topic.html", items=result, cols=cols, success='')
    except Exception as e:
        return render_template("sota_by_topic.html", items=[], cols=[], success='Can\'t view Results: ' + str(e))


if __name__ == '__main__':
    app.run()
