import React, { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Home.css';

const Home = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      navigate('/PrivateRoute');
    }
  }, [navigate]);

  return (
    <div className="home-container">
      <h1>Witamy w My Book App</h1>
      <p>
        Zapraszamy do katalogowania książek ze swojej biblioteczki. 
        Zarejestruj się, aby rozpocząć swoją przygodę, lub zaloguj się, 
        jeśli już masz konto.
      </p>
      <div className="button-container">
        <Link to="/register">
          <button className="home-button">Zarejestruj się</button>
        </Link>
        <Link to="/login">
          <button className="home-button">Zaloguj się</button>
        </Link>
      </div>
    </div>
  );
};

export default Home;
