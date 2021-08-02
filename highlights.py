from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from backend_classes import Database

db = Database("highlights.db")

class Window():
    """ This class builds the GUI application"""

    def __init__(self, root):
        self.root = root
        self.root.wm_title("Highlights")
        self.root.resizable(FALSE,FALSE)

        self.books_width = 40
        self.tags_width= 30
        self.highlights_width = 60
        self.lb_heights = 25
        frame_padding = 5

        # main frame
        main_frame = ttk.Frame(root)
        main_frame.grid(column=0, row=0, sticky=(N, W, E, S))

        # Books frame
        self.books_frame = ttk.Frame(main_frame, padding=frame_padding)
        self.books_frame.grid(row=1, column=1)

        self.book_search_lbl_var = StringVar(self.books_frame)
        self.book_search_lbl = ttk.Label(self.books_frame, text="Books", font=('Verdana', 11), textvariable=self.book_search_lbl_var)
        self.book_search_lbl.grid(column=1, row=1, sticky=W)

        self.book_search_text = StringVar()
        self.book_search_entry = ttk.Entry(self.books_frame, textvariable=self.book_search_text, width=self.books_width)
        self.book_search_entry.grid(column=1, row=2, columnspan=2, sticky=W)

        self.book_search_btn = ttk.Button(self.books_frame, text="Search", command=self.search_books)
        self.book_search_btn.grid(column=3, row=2, sticky=E)

        self.book_lb = Listbox(self.books_frame, height=self.lb_heights, width=self.books_width, font=('Verdana', 9))
        self.book_lb.grid(column=1, row=3, columnspan=3)

        self.book_sb = ttk.Scrollbar(self.books_frame)
        self.book_sb.grid(row=3, column=4, sticky=N+S)

        self.book_lb.configure(yscrollcommand=self.book_sb.set)
        self.book_sb.configure(command=self.book_lb.yview)

        self.book_lb.bind('<<ListboxSelect>>', self.filter_book)

        # Books detail frame
        self.books_detail_frame = ttk.Frame(main_frame, padding=frame_padding, relief="sunken")
        self.books_detail_frame.grid(row=3, column=1, sticky=(E,W,N,S))
        self.books_detail_frame.columnconfigure(2, weight=3)
        self.books_detail_frame.rowconfigure(9, weight=2)

        book_detail_label = ttk.Label(self.books_detail_frame, text="Book Detail")
        book_detail_label.grid(row=1, column=1)

        title_lbl = ttk.Label(self.books_detail_frame, text="Title")
        title_lbl.grid(row=3, column=1, sticky=E)
        self.title_text = StringVar(self.books_detail_frame)
        self.title_entry = ttk.Entry(self.books_detail_frame, textvariable=self.title_text)
        self.title_entry.grid(row=3, column=2, columnspan=2, sticky=(E,W))

        author_lbl = ttk.Label(self.books_detail_frame, text="Author")
        author_lbl.grid(row=5, column=1, sticky=E)
        self.author_text = StringVar(self.books_detail_frame)
        self.author_entry = ttk.Entry(self.books_detail_frame, textvariable=self.author_text)
        self.author_entry.grid(row=5, column=2, columnspan=2, sticky=(E,W))

        year_lbl = ttk.Label(self.books_detail_frame, text="Year")
        year_lbl.grid(row=7, column=1, sticky=E)
        self.year_text = StringVar(self.books_detail_frame)
        self.year_entry = ttk.Entry(self.books_detail_frame, textvariable=self.year_text, width=7)
        self.year_entry.grid(row=7, column=2, sticky=(W)) 

        self.book_add_btn = ttk.Button(self.books_detail_frame, text="Add", command=self.add_book)
        self.book_add_btn.grid(row=9, column=1, sticky=(S))

        self.book_edit_btn = ttk.Button(self.books_detail_frame, text="Save", command=self.edit_book)
        self.book_edit_btn.grid(row=9, column=2, sticky=(S))
        self.book_edit_btn.state(['disabled'])

        self.book_delete_btn = ttk.Button(self.books_detail_frame, text="Delete", command=self.delete_book)
        self.book_delete_btn.grid(row=9, column=3, sticky=(S))
        self.book_delete_btn.state(['disabled'])


        # Tags frame
        self.tags_frame = ttk.Frame(main_frame, padding=frame_padding)
        self.tags_frame.grid(row=1, column=3)

        self.tag_search_lbl_var = StringVar(self.tags_frame)
        self.tag_search_lbl = ttk.Label(self.tags_frame, text="Tags", font=('Verdana', 11), textvariable=self.tag_search_lbl_var)
        self.tag_search_lbl.grid(column=1, row=1, sticky=W)

        self.tag_search_text = StringVar()
        self.tag_search_entry = ttk.Entry(self.tags_frame, textvariable=self.tag_search_text, width=self.tags_width)
        self.tag_search_entry.grid(column=1, row=2, columnspan=2, sticky=W)

        self.tag_search_btn = ttk.Button(self.tags_frame, text="Search", command=self.search_tags)
        self.tag_search_btn.grid(column=3, row=2, sticky=E)

        self.tag_lb = Listbox(self.tags_frame, height=self.lb_heights, width=self.tags_width+2, font=('Verdana', 9))
        self.tag_lb.grid(column=1, row=3, columnspan=3)

        self.tag_sb = Scrollbar(self.tags_frame)
        self.tag_sb.grid(row=3, column=4, sticky=N+S)

        self.tag_lb.configure(yscrollcommand=self.tag_sb.set)
        self.tag_sb.configure(command=self.tag_lb.yview)

        self.tag_lb.bind('<<ListboxSelect>>', self.filter_tag)

        # Tags detail frame
        self.tags_detail_frame = ttk.Frame(main_frame, padding=frame_padding, relief="sunken")
        self.tags_detail_frame.grid(row=3, column=3, sticky=(E,W,N,S))
        self.tags_detail_frame.columnconfigure(2, weight=3)
        self.tags_detail_frame.rowconfigure(9, weight=3)

        tags_detail_lbl = ttk.Label(self.tags_detail_frame, text="Tag Detail")
        tags_detail_lbl.grid(row=1, column=1)

        tag_lbl = ttk.Label(self.tags_detail_frame, text="Tag")
        tag_lbl.grid(row=3, column=1, sticky=E)
        self.tag_text = StringVar(self.tags_detail_frame)
        self.tag_entry = ttk.Entry(self.tags_detail_frame, textvariable=self.tag_text)
        self.tag_entry.grid(row=3, column=2, columnspan=2, sticky=(E,W))

        self.tag_add_btn = ttk.Button(self.tags_detail_frame, text="Add", command=self.add_tag)
        self.tag_add_btn.grid(row=9, column=1, sticky=(S))

        self.tag_edit_btn = ttk.Button(self.tags_detail_frame, text="Save", command=self.edit_tag)
        self.tag_edit_btn.grid(row=9, column=2, sticky=(S))
        self.tag_edit_btn.state(['disabled'])

        self.tag_delete_btn = ttk.Button(self.tags_detail_frame, text="Delete", command=self.delete_tag)
        self.tag_delete_btn.grid(row=9, column=3, sticky=(S))
        self.tag_delete_btn.state(['disabled'])

        # Highlights frame
        self.highlights_frame = ttk.Frame(main_frame, padding=frame_padding)
        self.highlights_frame.grid(row=1, column=5)

        self.highlight_search_lbl_var = StringVar(self.highlights_frame)
        self.highlight_search_lbl = ttk.Label(self.highlights_frame, text="Highlights", font=('Verdana', 11), textvariable=self.highlight_search_lbl_var)
        self.highlight_search_lbl.grid(column=1, row=1, sticky=W)

        self.highlight_search_text = StringVar()
        self.highlight_search_entry = ttk.Entry(self.highlights_frame, textvariable=self.highlight_search_text, width=self.highlights_width)
        self.highlight_search_entry.grid(column=1, row=2, columnspan=2, sticky=W)

        self.highlight_search_btn = ttk.Button(self.highlights_frame, text="Search", command=self.search_highlights)
        self.highlight_search_btn.grid(column=3, row=2, sticky=E)

        self.highlights_list = Text(self.highlights_frame, height=self.lb_heights -2, width=self.highlights_width, wrap="word")
        self.highlights_list.grid(column=1, row=3, columnspan=3)
        self.highlights_list.tag_configure('highlight_style', font=('Verdana', 9))
        self.highlights_list.tag_configure('detail_style', font=('Verdana', 9))

        self.highlights_list_sb = ttk.Scrollbar(self.highlights_frame)
        self.highlights_list_sb.grid(row=3, column=4, sticky=N+S)

        self.highlights_list.configure(yscrollcommand=self.highlights_list_sb.set)
        self.highlights_list_sb.configure(command=self.highlights_list.yview)


        # Highlights detail frame
        self.highlights_detail_frame = ttk.Frame(main_frame, padding=frame_padding, relief="sunken")
        self.highlights_detail_frame.grid(row=3, column=5, rowspan=2, sticky=(N,E,W,S))
        self.highlights_detail_frame.columnconfigure(2, weight=1)
        self.highlights_detail_frame.columnconfigure(3, weight=2)

        highlights_details_lbl = ttk.Label(self.highlights_detail_frame, text="Highlight Detail")
        highlights_details_lbl.grid(row=1, column=1)

        highlight_lbl = ttk.Label(self.highlights_detail_frame, text="Highlight")
        highlight_lbl.grid(row=3, column=1)
        self.highlight_text = StringVar(self.highlights_detail_frame)
        self.highlight_txt = Text(self.highlights_detail_frame, height=3, width=self.highlights_width-10, wrap="word", font=('Verdana', 9))
        self.highlight_txt.grid(row=3, column=2, columnspan=3)

        self.highlight_sb = ttk.Scrollbar(self.highlights_detail_frame)
        self.highlight_sb.grid(row=3, column=5, sticky=N+S)

        self.highlight_txt.configure(yscrollcommand=self.highlight_sb.set)
        self.highlight_sb.configure(command=self.highlight_txt.yview)

        book_select_lbl = ttk.Label(self.highlights_detail_frame, text="Book")
        book_select_lbl.grid(row=5, column=1, sticky=(E))
        self.book_var = StringVar(self.highlights_detail_frame)
        self.book_cb = ttk.Combobox(self.highlights_detail_frame, textvariable=self.book_var)
        self.book_cb.grid(row=5, column=2, columnspan=2, sticky=(E,W))
        self.book_cb.state(['readonly'])

        tag_add_lbl = ttk.Label(self.highlights_detail_frame, text="New Tag")
        tag_add_lbl.grid(row=7, column=1, sticky=(E))
        self.tag_add_var = StringVar(self.highlights_detail_frame)
        self.tag_add_cb = ttk.Combobox(self.highlights_detail_frame, textvariable=self.tag_add_var)
        self.tag_add_cb.grid(row=7, column=2, columnspan=2, sticky=(E,W))
        self.tag_add_cb.state(['readonly'])
        self.highlight_tag_add_btn = ttk.Button(self.highlights_detail_frame, text="Add", command=self.add_to_existing)
        self.highlight_tag_add_btn.grid(row=7, column=4)
        self.adding_tags_list = []

        tag_existing_lbl = ttk.Label(self.highlights_detail_frame, text="Existing Tag")
        tag_existing_lbl.grid(row=9, column=1, sticky=(E))
        self.tag_existing_var = StringVar(self.highlights_detail_frame)
        self.tag_existing_cb = ttk.Combobox(self.highlights_detail_frame, textvariable=self.tag_existing_var)
        self.tag_existing_cb.grid(row=9, column=2, columnspan=2, sticky=(E,W))
        self.tag_existing_cb.state(['readonly'])
        self.highlight_tag_delete_btn = ttk.Button(self.highlights_detail_frame, text="Delete", command=self.delete_from_existing)
        self.highlight_tag_delete_btn.grid(row=9, column=4)
        self.tag_existing_cb.state(['disabled'])

        self.existing_lbl_var = StringVar(self.highlights_detail_frame)
        existing_lbl = ttk.Label(self.highlights_detail_frame, text="Tags: ")
        existing_lbl.grid(row=10, column=1, sticky=(E))      
        self.existing_list = ttk.Label(self.highlights_detail_frame, textvariable=self.existing_lbl_var)
        self.existing_list.grid(row=10, column=2, columnspan=3, sticky=(W))

        self.highlight_clear_btn = ttk.Button(self.highlights_detail_frame, text="Clear", command=self.clear_highlights_detail)
        self.highlight_clear_btn.grid(row=11, column=1, sticky=(S, E))

        self.highlight_add_btn = ttk.Button(self.highlights_detail_frame, text="Add", command=self.add_highlight)
        self.highlight_add_btn.grid(row=11, column=2, sticky=(S, E))

        self.highlight_edit_btn = ttk.Button(self.highlights_detail_frame, text="Save", command=self.edit_highlight)
        self.highlight_edit_btn.grid(row=11, column=3, sticky=(S))
        self.highlight_edit_btn.state(['disabled'])

        self.highlight_delete_btn = ttk.Button(self.highlights_detail_frame, text="Delete", command=self.delete_highlight)
        self.highlight_delete_btn.grid(row=11, column=4, sticky=(S, E))
        self.highlight_delete_btn.state(['disabled'])


        # Controls frame
        self.main_controls = ttk.Frame(main_frame, padding=frame_padding)
        self.main_controls.grid(row=4, column=1, sticky=(W,S))

        self.reset_filters_btn = ttk.Button(self.main_controls, text="Reset filters", command=self.reset_filters)
        self.reset_filters_btn.grid(row=1, column=1, sticky=(W, S))

        self.close_btn = ttk.Button(self.main_controls, text="Close", command=self.root.destroy)
        self.close_btn.grid(row=1, column=2, sticky=(S))

        # Message frame
        self.message_frame = ttk.Frame(main_frame, padding=frame_padding)
        self.message_frame.grid(row=4, column=3, sticky=(E,W))

        self.message_lbl = ttk.Label(self.message_frame, text="")
        self.message_lbl.grid(row=1, column=1, sticky=(E,W))

        # Populate list boxes
        self.reset_filters()


    def enable_add_tag_to_highlight(self):
        self.highlight_tag_add_btn.state(['!disabled'])


    def reset_filters(self):
        """ Reset list boxes to show all records"""
        # reset tag list
        self.display_tags(rows=db.get_tags())
        # reset book list
        self.display_books(rows=db.get_books())
        # reset highlights list
        self.display_highlights(db.get_highlights())
        # disable edit and delete buttons
        self.disable_book_buttons()
        self.disable_tag_buttons()
        self.disable_highlight_buttons()
        # update comboboxes
        self.tag_add_cb['values'] = db.get_tags()
        self.book_cb['values'] = db.get_titles()


    def display_books(self, rows="", sel_row=""):
        if sel_row == "":
            self.book_lb.delete(0, END)
            for row in rows:
                self.book_lb.insert(END, "\"" + row[1] + "\" by " + row[2] + " - " + row[3])
            self.book_search_lbl_var.set(f"Books ({str(len(rows))})")
        elif sel_row != "":
            self.book_lb.delete(0, END)
            self.book_lb.insert(END, sel_row)
            self.book_search_lbl_var.set("Books (1)")


    def display_highlights(self, rows):
        self.highlights_list['state'] = "normal"
        self.highlights_list.delete(1.0,END)
        counter=0
        for row in rows:
            self.highlights_list.insert(END, row['highlight'], ('highlight_style', counter))
            self.highlights_list.tag_configure(counter, foreground='black')
            def make_lambda(x):
                return lambda e: self.select_highlight(x)
            self.highlights_list.tag_bind(counter, '<1>', make_lambda(row['highlight']))
            self.highlights_list.insert(END, "\n")
            self.highlights_list.insert(END, "\tBook: " + row['title'], 'detail_style')
            self.highlights_list.insert(END, "\n")
            if not all(r is None for r in row['tags']):            
                self.highlights_list.insert(END, '\ttags: ' + ', '.join( row['tags']), 'detail_style')
            else:
                self.highlights_list.insert(END, '\ttags: None', 'detail_style')
            self.highlights_list.insert(END, "\n\n\n")
            counter += 1
        self.highlights_list['state'] = "disabled"
        self.highlight_search_lbl_var.set(f"Highlights ({str(len(rows))})")

    
    def display_tags(self, rows="", sel_row=""):
        if sel_row == "":
            self.tag_lb.delete(0, END)
            for row in rows:
                self.tag_lb.insert(END, row)
            self.tag_search_lbl_var.set(f"Tags ({str(len(rows))})")
        elif sel_row != "":
            self.tag_lb.delete(0, END)
            self.tag_lb.insert(END, sel_row)
            self.tag_search_lbl_var.set("Tags (1)")

    
    def filter_book(self, event):
        try:
            # Grab selected rows
            index = self.book_lb.curselection()[0]
            self.selected_row =self.book_lb.get(index)
            title = self.selected_row.split('"')[1]
            author = self.selected_row.split('" by ')[1].split(' - ')[0]
            year = self.selected_row.split('" by ')[1].split(' - ')[-1]
            # Update book list
            self.display_books(sel_row=self.selected_row)
            # filter highlights and tags
            book_id = db.get_book_id(title)
            self.display_tags(db.get_tags(book=book_id))
            self.display_highlights(db.get_highlights(book=book_id))
            # Populate book details form
            self.title_entry.delete(0,'end')
            self.title_entry.insert(0, title)
            self.year_entry.delete(0,'end')
            self.year_entry.insert(0, year)
            self.author_entry.delete(0,'end')
            self.author_entry.insert(0, author)
            # Update edit and delete buttons 
            self.enable_book_buttons()
            self.disable_tag_buttons()
            self.disable_highlight_buttons()
        except:
            print("pass filter book")
            pass

    
    def filter_tag(self, event):
        try:
            index = self.tag_lb.curselection()[0]
            tag = self.tag_lb.get(index)
            # Update tag list
            self.display_tags(sel_row=tag)
            # Filter books and highlights
            tag_id = db.get_tag_id(tag)
            self.display_books(db.get_books(tag=tag_id))
            self.display_highlights(db.get_highlights(tag=tag_id))
            # Populate tag details form
            self.tag_entry.delete(0,END)
            self.tag_entry.insert(0, tag)
            # Update edit and delete buttons
            self.enable_tag_buttons()
            self.disable_book_buttons()
            self.disable_highlight_buttons()
        except:
            print("pass filter tag")
            pass


    def search_books(self):
        search_text = self.book_search_entry.get()
        if search_text == "":
            self.display_books(db.get_books())
        else:
            self.display_books(db.search_books(search_text))



    def search_tags(self):
        search_text = self.tag_search_entry.get()
        if search_text == "":
            self.display_tags(db.get_tags())
        else:
            tags = db.search_tags(search_text)
            self.display_tags(db.search_tags(search_text))

    
    def search_highlights(self):
        search_text = self.highlight_search_entry.get()
        if search_text == "":
            self.display_highlights(db.get_highlights())
        else:
            self.display_highlights(db.search_highlights(search_text))


    def select_highlight(self, sel):
        """ click a highlight to select it and fill the highlight detail form. """
        self.enable_highlight_buttons()
        self.selected_highlight = db.get_highlight(db.get_highlight_id(sel))
        highlight_tags = db.get_highlights_tags(self.selected_highlight['id'])
        # Fill highlight
        self.highlight_txt.delete(1.0, END)
        self.highlight_txt.insert(END, self.selected_highlight['highlight'])
        # Set title
        self.book_cb.set(self.selected_highlight['title'])
        self.tag_existing_cb.set('')
        self.tag_add_cb.set('')
        # Set tag information
        if all(i is None for i in highlight_tags):
            self.tag_existing_cb.state(['disabled'])
            self.highlight_tag_delete_btn.state(['disabled'])
            self.existing_lbl_var.set('')
        else:
            self.adding_tags_list = highlight_tags
            self.existing_lbl_var.set(', '.join(self.adding_tags_list))
            self.tag_existing_cb['values'] = self.adding_tags_list
            self.tag_existing_cb.state(['!disabled'])
            self.highlight_tag_delete_btn.state(['!disabled'])


    def enable_book_buttons(self):
        self.book_edit_btn.state(['!disabled'])
        self.book_delete_btn.state(['!disabled'])


    def disable_book_buttons(self):
        self.book_edit_btn.state(['disabled'])
        self.book_delete_btn.state(['disabled'])

    
    def enable_tag_buttons(self):
        self.tag_edit_btn.state(['!disabled'])
        self.tag_delete_btn.state(['!disabled'])


    def disable_tag_buttons(self):
        self.tag_edit_btn.state(['disabled'])
        self.tag_delete_btn.state(['disabled'])


    def enable_highlight_buttons(self):
        self.highlight_edit_btn.state(['!disabled'])
        self.highlight_delete_btn.state(['!disabled'])
        

    def disable_highlight_buttons(self):
        self.selected_highlight = {}
        self.highlight_edit_btn.state(['disabled'])
        self.highlight_delete_btn.state(['disabled'])


    def add_book(self):
        """ Insert a book to the database if it doesn't already exist. All fields must be filled in."""
        # Ensure fields have values
        if self.year_text.get() == "" or self.title_text.get() == "" or self.author_text.get() == "":
            messagebox.showinfo("Missing fields", "Must fill in all fields...")
        elif db.get_book_id(self.title_text.get()) != "":
            messagebox.showinfo("Duplicate", "Book already exists...")
        else:
            db.insert_book(self.title_text.get(), self.author_text.get(), self.year_text.get())
            self.reset_filters()


    def edit_book(self):
        """ Update a book in the database. """
        row = self.book_lb.get(0, END)[0]
        book_id = db.get_book_id(row.split('"')[1])
        db.update_book(book_id, self.title_text.get(), self.author_text.get(), self.year_text.get())
        updated = '"' + self.title_text.get() + '" by ' + self.author_text.get() + ' - ' + self.year_text.get()
        self.book_lb.delete(0,END)
        self.book_lb.insert(END, updated)
        self.book_cb['values'] = db.get_titles()
    
    
    def delete_book(self):
        """ Delete a book from the database. """
        row = self.book_lb.get(0, END)[0]
        book_id = db.get_book_id(row.split('"')[1])
        book_highlights = db.get_highlights(book=book_id)
        if len(book_highlights) == 0:
            MsgBox = messagebox.askquestion ('Delete Book','Are you sure you want to delete the book?', icon='warning')
            if MsgBox == 'yes':
                db.delete_book(book_id)
                self.reset_filters()
        else:
            MsgBox = messagebox.askquestion ('Delete Book','Are you sure you want to delete the book? \
                This will delete the ' + str(len(book_highlights)) + ' highlights related to the book.',icon = 'warning')
            if MsgBox == 'yes':
                # Delete highlight_tags and highlights
                for h in book_highlights:
                    db.delete_highlight_tags(h['id'])
                    db.delete_highlight(h['id'])
                db.delete_book(book_id)
                self.reset_filters()
            

    def add_tag(self):
        """ Insert a tag to the database if it doesn't already exist. All fields must be filled in."""
        # Ensure fields have values
        if self.tag_text.get() == "":
            messagebox.showinfo("Blank field", "Must fill in the tag field...")
        elif db.get_tag_id(self.tag_text.get()) != "":
            messagebox.showinfo("Duplicate entry", "Tag already exists...")
        else:
            db.insert_tag(self.tag_text.get())
            self.reset_filters()


    def edit_tag(self):
        """ Update a tag in the database. """
        tag = self.tag_lb.get(0, END)[0]
        tag_id = db.get_tag_id(tag)
        db.update_tag(tag_id, self.tag_text.get())
        self.tag_lb.delete(0,END)
        self.tag_lb.insert(END, self.tag_text.get())
        self.tag_add_cb['values'] = db.get_tags()


    def delete_tag(self):
        """ Delete a tag in the database. """
        tag = self.tag_lb.get(0, END)[0]
        tag_id = db.get_tag_id(tag)
        MsgBox = messagebox.askquestion ("Delete Tag","Are you sure you want to delete the tag? \
                                    It will be removed from any highlights that have the tag." ,icon = 'warning')
        if MsgBox == 'yes':
            db.delete_tag(tag_id)
            self.reset_filters()


    def add_highlight(self):
        """ Add a highlight and it's tags to the database. """
        highlight_text = self.highlight_txt.get(1.0, "end-1c").rstrip()
        if highlight_text == "" or self.book_cb.get() == "":
            messagebox.showinfo("Missing fields", "Must fill in highlight and book fields...")
            return 0
        elif db.get_highlight_id(highlight_text) != "":
            messagebox.showinfo("Duplicate", "Highlight already exists...")
            return 0
        book_id = db.get_book_id(self.book_cb.get())
        db.add_highlight(highlight_text, book_id)
        tag_id_list = []
        for tag in self.adding_tags_list:
            tag_id_list.append(db.get_tag_id(tag))
        db.add_highlight_tags(db.get_highlight_id(highlight_text), tag_id_list)
        self.reset_filters()


    def edit_highlight(self):
        highlight_text = self.highlight_txt.get(1.0, "end-1c").rstrip()
        if highlight_text == "" or self.book_cb.get() == "":
            messagebox.showinfo("Missing fields", "Must fill in highlight and book fields...")
            return 0
        # elif db.get_highlight_id(highlight_text) == "duplicate":
        #     messagebox.showinfo("Duplicate", "Highlight already exists...")
        #     return 0
        book_id = db.get_book_id(self.book_cb.get())
        db.edit_highlight(highlight_text, book_id, self.selected_highlight['id'])
        tag_id_list = []
        for tag in self.adding_tags_list:
            tag_id_list.append(db.get_tag_id(tag))
        db.edit_highlight_tags(self.selected_highlight['id'], tag_id_list)
        self.display_highlights(db.get_highlights())


    def delete_highlight(self):
        MsgBox = messagebox.askquestion ("Delete Tag","Are you sure you want to delete the highlight? \
                                            \n \"" + self.selected_highlight['highlight'] + "\"",icon = 'warning')
        if MsgBox == 'yes':
            db.delete_highlight_tags(self.selected_highlight['id'])
            db.delete_highlight(self.selected_highlight['id'])
            self.reset_filters()


    def add_to_existing(self):
        """ Add a tag to a new highlight. """
        if self.tag_add_cb.get() != "" and self.tag_add_cb.get() not in self.adding_tags_list:
            self.adding_tags_list.append(self.tag_add_cb.get())
            self.existing_lbl_var.set(', '.join(self.adding_tags_list))
            # Update existing tags combobox
            self.tag_existing_cb.state(['!disabled'])
            self.highlight_tag_delete_btn.state(['!disabled'])
            self.tag_existing_cb['values'] = self.adding_tags_list


    def delete_from_existing(self):
        """ Delete a tag from a new or existing highlight. """
        if self.tag_existing_cb.get() != "":
            self.adding_tags_list.remove(self.tag_existing_cb.get())
            self.tag_existing_cb['values'] = self.adding_tags_list
            self.existing_lbl_var.set(', '.join(self.adding_tags_list))
            self.tag_existing_cb.set('')
        if len(self.adding_tags_list) == 0:
            self.tag_existing_cb.state(['disabled'])


    def clear_highlights_detail(self):
        """ Clears the highlight form """
        self.tag_existing_cb.set('')
        self.tag_add_cb.set('')
        self.tag_existing_cb.state(['disabled'])
        self.highlight_tag_delete_btn.state(['disabled'])
        self.highlight_txt.delete(1.0, END)
        self.book_cb.set('')
        self.adding_tags_list.clear()
        self.existing_lbl_var.set('')
        self.disable_highlight_buttons()


root = Tk()
Window(root)
root.mainloop()