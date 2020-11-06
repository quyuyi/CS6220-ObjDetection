import React from 'react';
import ReactDOM from 'react-dom';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Predict from './predict';

class Upload extends React.Component {
  constructor (props) {
    super(props);
    this.state = {
      selectedFile: null,
      uploaded: false,
    };

    this.onFileChange = this.onFileChange.bind(this);
    this.onFormSubmit = this.onFormSubmit.bind(this);
  }

  onFormSubmit(event) {
    event.preventDefault();
    console.log("try to upload");
    const data = new FormData(event.target);
    fetch("/api/upload/", {
      credentials: 'same-origin',
      method: 'POST',
      body: data,
    })
    .then((data) => {
      console.log(data);
      this.setState({
        uploaded: true,
      });
    })
    .catch((error) => console.log(error));
  }

  onFileChange(event) {
    event.preventDefault();
    console.log(event.target.files[0]);
    this.setState({selectedFile: event.target.files[0]});
  }

  renderUpload() {
    return (
      <div className="chooseFile">
        <Container>
          <Row><h3>Upload a video</h3></Row>
          <Row>
            <form onSubmit={this.onFormSubmit}>
            <span><input type="file" name="video" onChange={this.onFileChange} /></span>
            <span><input type="submit" /></span>
            </form>
          </Row>
        </Container>
      </div>
    );
  }

  renderNext() {
    return (
      <div className="enterPredict">
        <Predict />
      </div>
    );
  }

  render () {
    const uploaded = this.state.uploaded;
    console.log(uploaded);
    return (
      <div className="upload">
        {(uploaded) ? this.renderNext() : this.renderUpload()}
      </div>
    );
  }
}

export default Upload;