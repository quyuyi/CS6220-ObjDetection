import React from 'react';
import ReactDOM from 'react-dom';
import Select from 'react-select';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

class Upload extends React.Component {
    constructor (props) {
        super(props);
        this.state = {
            seelctedFile: null,
        };
    }

    onFileChange = event => {
        this.setState({seelctedFile: event.target.files[0]});
    }

    onFileUpload = () => {
        fetch("api/upload", {
            credentials: 'same-origin',
            method,
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({}),
          })
            .then((data) => {
              const { num_likes: numLikes } = this.state;
              const { status } = data;
              if (status === 204) {
                this.setState({
                  num_likes: numLikes - 1,
                  logname_likes_this: 0,
                });
              } else if (status === 201) {
                this.setState({
                  num_likes: numLikes + 1,
                  logname_likes_this: 1,
                });
              }
            })
            .catch((error) => console.log(error));
    }


    render () {
        return (
            <div className="upload">
                <form>
                    <input type="file" onChange={this.onFileChange} />
                    <button onClick={this.onFileUpload}>Upload</button>
                </form>
            </div>
        );
    }
}

export default Upload;