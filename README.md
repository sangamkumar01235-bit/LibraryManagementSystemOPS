Central Library Management System

A Python Object-Oriented Programming (OOP) project for managing library inventory, built with an interactive Streamlit web interface.

  
              Overview
This application models a library system where different types of items can be stored, tracked, borrowed, and returned. It begins with sample items (BK101 — Wonders of the world, BK102 — Chandani Raat, and MGK103 — No pain No gain) inside Central Library and lets users add more items and update their availability live in the browser.

 
             Key Features
Add Books and Magazines: Add new books with an ID, title, author, and page count, or add magazines with an ID, title, and issue number.
  
Borrow and Return Items: Check out available items and return borrowed items while preventing duplicate checkouts or returning items that are not borrowed.
  
Live Inventory and Filtering: View summary counts for total, available, and borrowed items, filter the inventory by status (All, Available, or Borrowed), and inspect formatted item details.
  
Session State Persistence: Keeps inventory additions and borrow/return updates active across Streamlit reruns during a session.


  
       Object-Oriented Design
Abstraction: Uses an abstract base class (LibraryItem) that requires subclasses to implement get_details().  

Encapsulation: Protects internal borrow state (_is_borrowed) and manages changes through checkout(), return_item(), and property accessors. 
 
Inheritance and Polymorphism: Book and Magazine inherit from LibraryItem and provide their own versions of get_details(). 
 
Inventory Management: A Library class stores items by ID and handles adding, borrowing, and returning operations. 