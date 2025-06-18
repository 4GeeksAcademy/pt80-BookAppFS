export const initialStore = () => {
  return {
    books: [],
  };
};

export default function storeReducer(store, action = {}) {
  if (action.type === "load_books") {
    return {
      ...store,
      books: action.books,
    };
  }

  if (action.type === "edit_book") {
    const bookIdx = store.books.findIndex((book) => book.id === action.book.id);
    const newBooks = store.books.toSpliced(bookIdx, 1, action.book);

    return {
      ...store,
      books: newBooks,
    };
  }

  if (action.type === "delete_book") {
    const bookIdx = store.books.findIndex((book) => book.id === action.id);
    const newBooks = store.books.toSpliced(bookIdx, 1);

    return {
      ...store,
      books: newBooks,
    };
  }

  return store;
}
