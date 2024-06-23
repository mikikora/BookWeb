import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(null);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          setIsAuthenticated(false);
          return;
        }
        await axios.get('/user/', {
          headers: {
            Authorization: `Bearer ${token}`,
          }
        });
        setIsAuthenticated(true);
      } catch (error) {
        if (error.response && error.response.status === 401) {
          localStorage.removeItem('token');
        }
        setIsAuthenticated(false);
      }
    };

    checkAuth();
  }, []);

  if (isAuthenticated === null) {
    return <div>Loading...</div>; // Lub dowolny spinner lub komunikat ładowania
  }

  return isAuthenticated ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
