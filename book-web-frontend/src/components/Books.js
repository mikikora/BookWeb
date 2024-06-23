import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Books.css';

const Books = () => {
  const [books, setBooks] = useState([]);
  const [tags, setTags] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [currentBook, setCurrentBook] = useState(null);
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [rating, setRating] = useState('');
  const [comment, setComment] = useState('');
  const [newTag, setNewTag] = useState('');
  const [selectedTags, setSelectedTags] = useState([]);

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('/books/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setBooks(response.data);
      } catch (error) {
        alert('Failed to fetch books!');
      }
    };

    const fetchTags = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('/tags/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setTags(response.data);
      } catch (error) {
        alert('Failed to fetch tags!');
      }
    };

    fetchBooks();
    fetchTags();
  }, []);

  const handleAddBook = async (event) => {
    event.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const newBook = {
        title,
        author,
        rating: parseInt(rating),
        comment,
        tags: selectedTags
      };
      const response = await axios.post('/books/', newBook, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setBooks([...books, response.data]);
      setTitle('');
      setAuthor('');
      setRating('');
      setComment('');
      setSelectedTags([]);
      setShowForm(false);
      alert('Book added successfully!');
    } catch (error) {
      alert('Failed to add book!');
    }
  };

  const handleEditBook = async (event) => {
    event.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const updatedBook = {
        title,
        author,
        rating: parseInt(rating),
        comment,
        tags: selectedTags
      };
      const response = await axios.put(`/books/${currentBook.id}`, updatedBook, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setBooks(books.map(book => book.id === currentBook.id ? response.data : book));
      setTitle('');
      setAuthor('');
      setRating('');
      setComment('');
      setSelectedTags([]);
      setShowForm(false);
      setEditMode(false);
      setCurrentBook(null);
      alert('Book updated successfully!');
    } catch (error) {
      alert('Failed to update book!');
    }
  };

  const handleEditClick = (book) => {
    setTitle(book.title);
    setAuthor(book.author);
    setRating(book.rating.toString());
    setComment(book.comment);
    setSelectedTags(book.tags.map(tag => tag.name));
    setCurrentBook(book);
    setEditMode(true);
    setShowForm(true);
  };

  const handleAddTag = async (event) => {
    event.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('/tags/', { name: newTag }, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setTags([...tags, response.data]);
      setNewTag('');
      alert('Tag added successfully!');
    } catch (error) {
      alert('Failed to add tag!');
    }
  };

  const handleTagChange = (tagName) => {
    if (selectedTags.includes(tagName)) {
      setSelectedTags(selectedTags.filter(tag => tag !== tagName));
    } else {
      setSelectedTags([...selectedTags, tagName]);
    }
  };

  return (
    <div className="books-container">
      <h2>Moje książki</h2>
      {showForm && (
        <form onSubmit={editMode ? handleEditBook : handleAddBook} className="book-form">
          <label>
            Tytuł:
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </label>
          <label>
            Autor:
            <input
              type="text"
              value={author}
              onChange={(e) => setAuthor(e.target.value)}
              required
            />
          </label>
          <label>
            Ocena:
            <input
              type="number"
              value={rating}
              onChange={(e) => setRating(e.target.value)}
              min="1"
              max="5"
              required
            />
          </label>
          <label>
            Komentarz:
            <input
              type="text"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
            />
          </label>
          <div className="tags-container">
            <h4>Tagi</h4>
            {tags.map((tag) => (
              <label key={tag.id} className="tag-checkbox">
                <input
                  type="checkbox"
                  value={tag.name}
                  checked={selectedTags.includes(tag.name)}
                  onChange={() => handleTagChange(tag.name)}
                />
                {tag.name}
              </label>
            ))}
          </div>
          <button type="submit" className="auth-button">
            {editMode ? 'Zaktualizuj książkę' : 'Dodaj książkę'}
          </button>
        </form>
      )}
      <br></br>
      <button onClick={() => setShowForm(!showForm)} className="toggle-form-button">
        {showForm ? 'Schowaj formularz' : 'Dodaj nową pozycję'}
      </button>
      <div className="add-tag-form">
        <h4>Dodaj nowy tag</h4>
        <form onSubmit={handleAddTag}>
          <input
            type="text"
            value={newTag}
            onChange={(e) => setNewTag(e.target.value)}
            required
          /><br></br>
          <button type="submit" className="add-tag-button">Dodaj tag</button>
        </form>
      </div>
      <ul className="books-list">
        {books.map((book) => (
          <li key={book.id} className="book-item">
            <h3>{book.title}</h3>
            <p>Autor: {book.author}</p>
            <p>Ocena: {book.rating} gwiazdek</p>
            <p>Komentarz: {book.comment}</p>
            <div className="tags-list">
              {book.tags.map((tag) => (
                <span key={tag.id} className="tag-item">{tag.name}</span>
              ))}
            </div>
            <button onClick={() => handleEditClick(book)} className="edit-button">Edytuj</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Books;
