import React, { useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import styles from '../styles/Navbar.module.css';

const Navbar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const navLinks = [
    { path: '/', label: 'Home' },
    { path: '/dashboard', label: 'Dashboard' },
    { path: '/templates', label: 'Templates' },
    { path: '/marketplace', label: 'Marketplace' },
    { path: '/login', label: 'Login' },
    { path: '/signup', label: 'Signup' },
  ];

  return (
    <header className={styles.navbar}>
      <div className={styles.navbarContent}>
        <div className={styles.brand}>
          <NavLink to="/" className={styles.logo}>
            Extension Factory
          </NavLink>
        </div>
        <button
          className={styles.hamburger}
          onClick={toggleMenu}
          aria-label="Toggle navigation menu"
        >
          <span className={styles.hamburgerLine}></span>
          <span className={styles.hamburgerLine}></span>
          <span className={styles.hamburgerLine}></span>
        </button>
        <nav className={`${styles.navLinks} ${isOpen ? styles.open : ''}`}>
          {navLinks.map((link) => (
            <NavLink
              to={link.path}
              key={link.path}
              className={({ isActive }) =>
                `${styles.navLink} ${isActive ? styles.active : ''}`
              }
              onClick={() => setIsOpen(false)}
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  );
};

export default Navbar;
