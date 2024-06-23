import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import './Auth.css';

const Register = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      navigate('/books');
    }
  }, [navigate]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await axios.post('/users/', {
        username,
        password,
      });
      alert('Registration successful!');
      navigate('/login');
    } catch (error) {
      alert('Registration failed!');
    }
  };

  return (
    <div className="auth-container">
      <h2>Zarejestruj się</h2>
      <form onSubmit={handleSubmit} className="auth-form">
        <label>
          Nazwa użytkownika:
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </label>
        <label>
          Hasło:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        <button type="submit" className="auth-button">Zarejestruj się</button>
      </form>
      <p>Masz już konto? <Link to="/login">Zaloguj się</Link></p>
    </div>
  );
};

export default Register;
