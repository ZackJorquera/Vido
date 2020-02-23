import React from 'react';
import logo from './Logo100.png'
import './loading.css';

function Loading(){
  return (
    <div className="Loading">
      <img src={logo} className="LoadingLogo" alt="loading" />
    </div>
  );
}

export default Loading;
