import React from 'react';
import ReactDOM from 'react-dom';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

class Predict extends React.Component {
  constructor (props) {
    super(props);
    this.state = {
        predict: false,
        src: '',
    };
    this.onClickStart = this.onClickStart.bind(this);
  }

  componentDidMount() {}

  onClickStart(event) {
    event.preventDefault();
    this.setState({
      predict: true,
      src: '/api/predict/',
    });
  }

  renderOption() {
    return (
      <div className="option">
        <button onClick={this.onClickStart}>Start Prediction!</button>
      </div>
    );
  }

  renderVideo() {
    return (
      <div>
        <Container fluid>
        <Row className="justify-content-md-center">
          <Col md={6}>
            <Row><p>W/o frame skipping</p></Row>
            <Row><img className="video" src="/api/predict/" /></Row>
          </Col>
          <Col md={6}>
            <Row><p>W/ frame skipping</p></Row>
            <Row><img className="video" src="/api/comparison/" /></Row>
          </Col>
        </Row>
        </Container>
      </div>
    );
  }

  render () {
    const {predict, src} = this.state;
    console.log(predict);
    return (
      <div className="predict">
        {(predict) ? this.renderVideo() : this.renderOption()}
        {/* <Container fluid>
        <Row>
          <button onClick={this.onClickStart}>Start Prediction!</button>
        </Row>
        <Row className="justify-content-md-center">
          <Col md={6}>
            <Row><p>W/o frame skipping</p></Row>
            <Row><img className="video" src={src} /></Row>
          </Col>
          <Col md={6}>
            <Row><p>W/ frame skipping</p></Row>
            <Row><img className="video" src={src} /></Row>
          </Col>
        </Row>
        </Container> */}
      </div>
    );
  }
}

export default Predict;