import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import {drawImageProp} from './utils';

class Video extends React.Component {

  constructor (props) {
    super(props);
  }

  componentDidMount() {
  }

  render() {
    return (
      <div className="Video">
        <Row>
          <Col><img src="/api/predict/" /></Col>
        </Row>
      </div>
    );
  }
}

export default Video;