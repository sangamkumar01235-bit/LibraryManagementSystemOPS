from abc import ABC, abstractmethod
import streamlit as st


class LibraryItem(ABC):
    def __init__(self, item_id: str, title: str):
        self.item_id = item_id
        self.title = title
        self._is_borrowed = False

    @abstractmethod
    def get_details(self) -> str:
        pass

    def checkout(self) -> bool:
        if not self._is_borrowed:
            self._is_borrowed = True
            return True
        return False

    def return_item(self) -> bool:
        if self._is_borrowed:
            self._is_borrowed = False
            return True
        return False

    @property
    def is_borrowed(self) -> bool:
        return self._is_borrowed

    @property
    def status(self) -> str:
        return "Borrowed" if self._is_borrowed else "Available"


class Book(LibraryItem):
    def __init__(self, item_id: str, title: str, author: str, pages: int):
        super().__init__(item_id, title)
        self.author = author
        self.pages = pages

    def get_details(self) -> str:
        return (
            f"[Book] ID: {self.item_id} | '{self.title}' by {self.author} "
            f"({self.pages} pages) - Status: {self.status}"
        )


class Magazine(LibraryItem):
    def __init__(self, item_id: str, title: str, issue_number: int):
        super().__init__(item_id, title)
        self.issue_number = issue_number

    def get_details(self) -> str:
        return (
            f"[Magazine] ID: {self.item_id} | '{self.title}' "
            f"(Issue #{self.issue_number}) - Status: {self.status}"
        )


class Library:
    def __init__(self, name: str):
        self.name = name
        self.inventory: dict[str, LibraryItem] = {}

    def add_item(self, item: LibraryItem) -> tuple[bool, str]:
        if item.item_id in self.inventory:
            return False, f"An item with ID '{item.item_id}' already exists."
        self.inventory[item.item_id] = item
        return True, f"Added to '{self.name}': {item.title}"

    def borrow_item(self, item_id: str) -> tuple[bool, str]:
        item = self.inventory.get(item_id)
        if not item:
            return False, f"Error: Item with ID '{item_id}' not found."
        if item.checkout():
            return True, f"Success: You borrowed '{item.title}'."
        return False, f"Unavailable: '{item.title}' is already checked out."

    def return_item(self, item_id: str) -> tuple[bool, str]:
        item = self.inventory.get(item_id)
        if not item:
            return False, f"Error: Item with ID '{item_id}' not found."
        if item.return_item():
            return True, f"Success: Returned '{item.title}'."
        return False, f"Notice: '{item.title}' was not checked out."


def init_library() -> Library:
    lib = Library("Central Library")
    lib.add_item(Book("BK101", "Wonders of the world", "Prabhakar Mishra", 209))
    lib.add_item(Book("BK102", "Chandani Raat", "Manoj Tiwari", 568))
    lib.add_item(Magazine("MGK103", "No pain No gain", 25412))
    return lib


st.set_page_config(page_title="Central Library Manager", page_icon="📚", layout="wide")

if "library" not in st.session_state:
    st.session_state.library = init_library()

library: Library = st.session_state.library

st.title(f"📚 {library.name}")
st.caption("Object-Oriented Library Management System built with Streamlit")

# Top metrics
total_items = len(library.inventory)
borrowed_items = sum(1 for item in library.inventory.values() if item.is_borrowed)
available_items = total_items - borrowed_items

m1, m2, m3 = st.columns(3)
m1.metric("Total Items", total_items)
m2.metric("Available", available_items)
m3.metric("Borrowed", borrowed_items)

st.divider()

# Sidebar: Add new Book or Magazine
with st.sidebar:
    st.header("➕ Add New Item")
    item_type = st.selectbox("Item Type", ["Book", "Magazine"])

    with st.form("add_item_form", clear_on_submit=True):
        item_id = st.text_input("Item ID", placeholder="e.g., BK104 or MGK105").strip()
        title = st.text_input("Title", placeholder="Enter title").strip()

        if item_type == "Book":
            author = st.text_input("Author", placeholder="Enter author name").strip()
            pages = st.number_input("Pages", min_value=1, value=100, step=1)
        else:
            issue_number = st.number_input("Issue Number", min_value=1, value=1, step=1)

        submitted = st.form_submit_button("Add to Library", use_container_width=True)

        if submitted:
            if not item_id or not title:
                st.error("Please provide both an Item ID and a Title.")
            elif item_type == "Book" and not author:
                st.error("Please provide an Author name for the book.")
            else:
                new_item = (
                    Book(item_id, title, author, int(pages))
                    if item_type == "Book"
                    else Magazine(item_id, title, int(issue_number))
                )
                ok, msg = library.add_item(new_item)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.warning(msg)

# Main area: Borrow / Return quick actions + Inventory table
col_left, col_right = st.columns([1, 2], gap="large")

with col_left:
    st.subheader("🔄 Borrow / Return")
    if library.inventory:
        item_options = {
            f"{item.item_id} — {item.title} ({item.status})": item.item_id
            for item in library.inventory.values()
        }
        selected_label = st.selectbox("Select Item", list(item_options.keys()))
        selected_id = item_options[selected_label]

        b_col1, b_col2 = st.columns(2)
        if b_col1.button("Borrow Item", use_container_width=True):
            ok, msg = library.borrow_item(selected_id)
            (st.success if ok else st.warning)(msg)
            st.rerun()

        if b_col2.button("Return Item", use_container_width=True):
            ok, msg = library.return_item(selected_id)
            (st.success if ok else st.info)(msg)
            st.rerun()
    else:
        st.info("No items in the library yet.")

with col_right:
    st.subheader("📋 Library Inventory")
    if not library.inventory:
        st.info("No items currently in library.")
    else:
        filter_status = st.radio(
            "Filter by status",
            ["All", "Available", "Borrowed"],
            horizontal=True,
        )

        rows = []
        for item in library.inventory.values():
            if filter_status != "All" and item.status != filter_status:
                continue
            rows.append(
                {
                    "ID": item.item_id,
                    "Type": "Book" if isinstance(item, Book) else "Magazine",
                    "Title": item.title,
                    "Author / Issue": (
                        item.author if isinstance(item, Book) else f"Issue #{item.issue_number}"
                    ),
                    "Pages": item.pages if isinstance(item, Book) else "-",
                    "Status": item.status,
                    "Formatted Details": item.get_details(),
                }
            )

        if rows:
            st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.write(f"No {filter_status.lower()} items found.")