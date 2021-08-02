import sqlite3


class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        # books table
        self.cur.execute("CREATE TABLE IF NOT EXISTS books(\
                        id INTEGER PRIMARY KEY AUTOINCREMENT, \
                        title TEXT, \
                        author TEXT, \
                        year TEXT)")
        # highlights table
        self.cur.execute("CREATE TABLE IF NOT EXISTS highlights(\
                        id INTEGER PRIMARY KEY AUTOINCREMENT, \
                        highlight TEXT, \
                        book_id INT, \
                        FOREIGN KEY(book_id) REFERENCES books(id))")
        # tags table
        self.cur.execute("CREATE TABLE IF NOT EXISTS tags(\
                        id INTEGER PRIMARY KEY AUTOINCREMENT, \
                        tag TEXT)")
        # highlights_tags Table
        self.cur.execute("CREATE TABLE IF NOT EXISTS highlights_tags(\
                        highlight_id INT, \
                        tag_id INT, \
                        FOREIGN KEY(highlight_id) REFERENCES highlights(id) \
                        FOREIGN KEY(tag_id) REFERENCES tags(id))")
        self.conn.commit()


    def get_books(self, tag="", book_id=""):
        if tag =="" and book_id == "":
            self.cur.execute("SELECT * FROM books ORDER BY author, title")
        elif tag == "":
            self.cur.execute("SELECT * FROM books WHERE id=? ORDER BY title", (book_id,))
        else:
            self.cur.execute("SELECT DISTINCT books.id, title, author, year FROM books \
                                JOIN highlights ON highlights.book_id = books.id \
                                JOIN highlights_tags ON highlights_tags.highlight_id = highlights.id \
                                JOIN tags ON highlights_tags.tag_id = tags.id \
                                WHERE tags.id = ? ORDER BY title", (tag,))
        return self.cur.fetchall()

    
    def search_books(self, search_string):
        query_str = '%' + search_string + '%'
        self.cur.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR year LIKE ? ORDER BY title", (query_str, query_str, query_str))
        return self.cur.fetchall()


    def get_titles(self):
        self.cur.row_factory = lambda cursor, row: row[0]
        self.cur.execute("SELECT title FROM books ORDER BY title")
        titles_list = self.cur.fetchall()
        self.cur.row_factory = None
        return titles_list
    

    def get_tags(self, book="", tag_id=""):
        self.cur.row_factory = lambda cursor, row: row[0]
        if book =="":
            self.cur.execute("SELECT tag FROM tags ORDER BY tag")
            tags_list = self.cur.fetchall()
        else:
            self.cur.execute("SELECT DISTINCT tag FROM tags \
                                JOIN highlights_tags ON highlights_tags.tag_id = tags.id \
                                JOIN highlights ON highlights_tags.highlight_id = highlights.id \
                                JOIN books ON highlights.book_id = books.id \
                                WHERE book_id = ? ORDER BY tag", (book,))
            tags_list = self.cur.fetchall()

        self.cur.row_factory = None
        return tags_list


    def search_tags(self, search_string):
        self.cur.row_factory = lambda cursor, row: row[0]
        query_str = '%' + search_string + '%'
        self.cur.execute("SELECT tag FROM tags WHERE tag LIKE ? ORDER BY tag", (query_str,))
        tags_list = self.cur.fetchall()
        self.cur.row_factory = None
        return tags_list
    
    
    def get_highlights(self, tag="", book=""):
        if tag == "" and book == "":
            self.cur.execute("SELECT highlights.id, highlight, title, tag FROM highlights \
                                LEFT JOIN highlights_tags ON highlights_tags.highlight_id = highlights.id \
                                LEFT JOIN tags ON highlights_tags.tag_id = tags.id \
                                LEFT JOIN books ON highlights.book_id = books.id \
                                ORDER BY title, highlight")
        elif tag == "" and book != "":
            self.cur.execute("SELECT highlights.id, highlight, title, tag FROM highlights \
                                LEFT JOIN highlights_tags ON highlights_tags.highlight_id = highlights.id \
                                LEFT JOIN tags ON highlights_tags.tag_id = tags.id \
                                LEFT JOIN books ON highlights.book_id = books.id \
                                WHERE highlights.book_id=? \
                                ORDER BY title, highlight", (book,))
        elif book == "" and tag != "":
            self.cur.execute("SELECT highlights.id, highlight, title, tag FROM highlights \
                                LEFT JOIN highlights_tags ON highlights_tags.highlight_id = highlights.id \
                                LEFT JOIN tags ON highlights_tags.tag_id = tags.id \
                                LEFT JOIN books ON highlights.book_id = books.id \
                                WHERE highlight_id IN (SELECT highlight_id FROM highlights_tags \
	                            WHERE highlights_tags.tag_id = ?) \
                                ORDER BY title, highlight", (tag,))
        else:
            self.cur.execute("SELECT highlights.id, highlight, title, tag FROM highlights \
                                LEFT JOIN highlights_tags ON highlights_tags.highlight_id = highlights.id \
                                LEFT JOIN tags ON highlights_tags.tag_id = tags.id \
                                LEFT JOIN books ON highlights.book_id = books.id \
                                WHERE highlights_tags.tag_id=? AND highlights.book_id=? \
                                ORDER BY title, highlight", (tag,book))
        results = []
        counter = 0
        for row in self.cur.fetchall():
            if not any(d['id'] == row[0] for d in results):
                results.append({
                    'id': row[0],
                    'highlight': row[1],
                    'title': row[2],
                    'tags': [row[3]]
                })
                counter += 1
            else: 
                results[counter - 1]['tags'].append(row[3])

        return results

    
    def get_highlight(self, id):
        self.cur.execute("SELECT highlights.id, highlight, title FROM highlights \
                    JOIN books ON highlights.book_id = books.id \
                    WHERE highlights.id=?", (id,))
        for row in self.cur.fetchall():
            results = {
                'id': row[0],
                'highlight': row[1],
                'title': row[2]
            }    
        return results

        
    def get_highlights_tags(self, highlight_id):
        self.cur.execute("SELECT tag FROM highlights_tags \
                    JOIN tags ON highlights_tags.tag_id = tags.id \
                    WHERE highlights_tags.highlight_id=? ORDER BY tag", (highlight_id,))
        tags = []
        for row in self.cur.fetchall():     
            tags.append(row[0])
        return tags
    

    def get_highlight_id(self, highlight):
        self.cur.execute("SELECT id FROM highlights WHERE highlight=?", (highlight,))
        row = self.cur.fetchone()
        if row is None:
            return ""           
        return row[0]

    def search_highlights(self, search_string):
        query_str = '%' + search_string + '%'
        self.cur.execute("SELECT highlights.id, highlight, title, tag FROM highlights \
                    LEFT JOIN highlights_tags ON highlights_tags.highlight_id = highlights.id \
                    LEFT JOIN tags ON highlights_tags.tag_id = tags.id \
                    LEFT JOIN books ON highlights.book_id = books.id \
                    WHERE highlight LIKE ? \
                    ORDER BY title, highlight", (query_str,))
        results = []
        counter = 0
        for row in self.cur.fetchall():
            if not any(d['id'] == row[0] for d in results):
                results.append({
                    'id': row[0],
                    'highlight': row[1],
                    'title': row[2],
                    'tags': [row[3]]
                })
                counter += 1
            else: 
                results[counter - 1]['tags'].append(row[3])
        return results


    def get_book_id(self, title):
        self.cur.execute("SELECT id FROM books WHERE title=?", (title,))
        row = self.cur.fetchone()
        if row is None:
            return ""
        return row[0]


    def get_tag_id(self, tag):
        self.cur.execute("SELECT id FROM tags WHERE tag=?", (tag,))
        row = self.cur.fetchone()
        if row is None:
            return ""
        return row[0]


    def insert_book(self, title, author, year):
        self.cur.execute("INSERT INTO books('title', 'author', 'year') VALUES(?, ?, ?)", (title, author, year))
        self.conn.commit()


    def update_book(self, id, title, author, year):
        self.cur.execute("UPDATE books SET title=?, author=?, year=? WHERE id=?", (title, author, year, id))
        self.conn.commit()


    def delete_book(self, id):
        self.cur.execute("DELETE FROM books WHERE id=?", (id,))
        self.conn.commit()


    def insert_tag(self, tag):
        self.cur.execute("INSERT INTO tags('tag') VALUES (?)", (tag,))
        self.conn.commit()


    def update_tag(self, id, tag):
        self.cur.execute("UPDATE tags SET tag=? WHERE id=?", (tag, id))
        self.conn.commit()


    def delete_tag(self, id):
        self.cur.execute("DELETE FROM highlights_tags WHERE tag_id=?", (id,))
        self.cur.execute("DELETE FROM tags WHERE id=?", (id,))
        self.conn.commit()

    
    def add_highlight(self, highlight, book_id):
        self.cur.execute("INSERT INTO highlights('highlight', 'book_id') VALUES (?, ?)", (highlight, book_id))
        self.conn.commit()


    def edit_highlight(self, highlight, book_id, id):
        self.cur.execute("UPDATE highlights SET highlight=?, book_id=? WHERE id=?", (highlight, book_id, id))
        self.conn.commit()


    def delete_highlight(self, id):
        self.cur.execute("DELETE FROM highlights WHERE id=?", (id,))
        self.conn.commit()

    
    def add_highlight_tags(self, highlight_id, tags):
        for tag in tags:
            self.cur.execute("INSERT INTO highlights_tags('highlight_id', 'tag_id') VALUES (?, ?)", (highlight_id, tag))
        self.conn.commit()
    

    def delete_highlight_tags(self, highlight_id=""):
        self.cur.execute("DELETE FROM highlights_tags WHERE highlight_id=?", (highlight_id,))
        self.conn.commit()
    

    def edit_highlight_tags(self, highlight_id, tags):
        self.delete_highlight_tags(highlight_id)
        self.add_highlight_tags(highlight_id, tags)


    def __del__(self):
        self.conn.close()

# db = Database("highlights.db")
# print(db.get_tags())