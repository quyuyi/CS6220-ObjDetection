import React from 'react';
import ReactDOM from 'react-dom';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

class Video extends React.Component {
    constructor (props) {
        super(props);
        this.state = {
            src: "https://media.w3.org/2010/05/sintel/trailer_hd.mp4"
        };
    }

    render () {
        return (
            <div className="Video">
                <video width="400" src={this.state.src} controls >
                    Your browser does not support HTML5 video.
                </video>
            </div>
        );
    }
}

export default Video;