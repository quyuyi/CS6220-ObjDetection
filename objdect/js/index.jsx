import React from 'react';
import ReactDOM from 'react-dom';
import Test from './test';
import Video from './video';

// This method is only called once
ReactDOM.render(
    // <Video parameter="input"/>,
    <img src="/api/predict/" />,
    document.getElementById('reactEntry'),
);
