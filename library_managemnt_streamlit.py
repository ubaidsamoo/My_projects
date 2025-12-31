import streamlit as st

class Library:
    def __init__(self,listofBooks):
        self.books = listofBooks
        
    def displayAvailableBooks(self):
            st.write(f"\n{len(self.books)} Available books are: ") 
            for book in self.books:
                st.write(f" 📗--{book}") 
            st.write("\n")

    def borrowBook(self,name, bookname):
        if bookname not in self.books:
            st.write(f"sorry, {bookname} is not available in the library else wait untill he returns .\n")
        else:
            track.append({name: bookname})
            st.write(f'Book ISSUED: Thank you keep it with care and return on time.\n')
            self.books.remove(bookname)

    def returnBook(self, bookname):
            st.write("Book returned: Thank you!\n")
            self.books.append(bookname)

    def donateBook(self,bookname):
            st.write("Book Donated: Thank you very much, Have a Great day Ahead!\n")
            self.books.append(bookname)

class Student:
    
    def requestBook(self):
        book = st.text_input("Enter the name of the book you want to borrow:")
        return book
    def returnBook(self):
        name = st.text_input("Enter your name:")
        book = st.text_input("Enter the name of the book you want to return:")
        return name, book
    
    def donateBook(self):
        book = st.text_input("Enter the name of the book you want to donate:")
        return book



        # Librart and track setup
Karachilibrary = Library(
         ["Rich Dad Poor Dad","Ego is the Enemy","zero to one","Pyscology of money","48 Laws of Power"]
         )
student = Student()
track = []

st.title("📚📚📚 WELCOME TO THE KARACHI LIBRARY MANAGEMENT 📚📚📚")

    # Streamlit form to get user choice

st.write("""
             Choose what you want to do:
             1. List all books
             2. Borrow a book
             3. Return a book
             4. Donate a book
             5. Track books
             6. Exit
    """)

action = st.selectbox("select an action",["","List all books","Borrow a book","Return a book","Donate a book","Track books","Exit"])
    
if action == "List all books":
    Karachilibrary.displayAvailableBooks()
elif action == "Borrow a book":
    student_name = st.text_input("Enter your name:")
    book_to_borrow = student.requestBook()
          
    if st.button("Borrow"):
                 if student_name and book_to_borrow: 
                     Karachilibrary.borrowBook(student_name, book_to_borrow)
                 elif not student_name:
                    st.warning("Please enter your name.") 
                 elif not book_to_borrow:
                    st.warning("Please enter the name of the book you want to borrow.")   

    elif action == "Return a book":  
         student_name, book_to_return = student.returnBook()

         if st.button("Return"):
                  if student_name and book_to_return:
                        Karachilibrary.returnBook(book_to_return)
                  elif not student_name:
                      st.warning("Please enter your name.") 
                  elif not book_to_return:
                      st.warning("Please enter the name of the book you want to return.")
    elif action == "Donate a book":
         book_to_donate = student.donateBook()

         if st.button("Donate"):
                  if book_to_donate:
                        Karachilibrary.donateBook(book_to_donate)
                  else:
                      st.warning("Please enter the name of the book you want to donate.")     

    elif action == "Track books":  
         if track:
             st.write("Currently borrowed books:")
             for entery in track:
                 for key, value in entery.items():
                     st.write(f"{key} has borrowed '{value}'")
         else:
             st.write("No books are currently borrowed.")      


    elif action == "Exit":
        st.write("Thank you for using the Karachi Library Management System. Have a great day!")                                        