import React from 'react';
import ReactDOM from 'react-dom';
import Test from './test';
import Video from './video';
import Upload from './upload';
import Predict from './predict';

// This method is only called once
ReactDOM.render(
  <Upload />,
  // <Predict />,
  // <Video />,
  // <img src="/api/predict/" />,
  document.getElementById('reactEntry'),
);
