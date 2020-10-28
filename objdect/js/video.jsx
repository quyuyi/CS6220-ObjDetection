import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import {drawImageProp} from './utils';

class Video extends React.Component {
  canvasRef = React.createRef();
  videoRef = React.createRef();

  constructor (props) {
    super(props);
    this.drawFrame = this.drawFrame.bind(this);
    this.startVideo = this.startVideo.bind(this);
    this.stopVideo = this.stopVideo.bind(this);
    this.fetchPrediction = this.fetchPrediction.bind(this);
  }

  componentDidMount() {
    // this.videoRef.current = document.createElement('video');
    this.videoRef.current.src = '/api/get_video';
    this.videoRef.current.onplay = this.drawFrame;
    this.videoRef.current.muted = true;

    this.videoRef.current.onloadeddata = () => {
      const ctx = this.canvasRef.current.getContext("2d");
      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    }
  }

  fetchPrediction(ctx, img) {    
    fetch("/api/predict/", {
      method: "POST",
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        "image": img,
        "hello": "hello"
      }),
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        console.log(data);
        // do something about data
        drawImageProp(ctx, data.prediction);
        // ctx.drawImage(data.prediction);
      })
      .catch((error) => console.log(error));
  }

  drawFrame() {
    if (!this.videoRef.current || !this.canvasRef.current) {
      this.videoRef.current.pause();
      return;
    }
    if (!this.paused) {
      this.videoRef.current.pause();
      const ctx = this.canvasRef.current.getContext('2d');
      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
      // draw the current frame of the video
      drawImageProp(ctx, this.videoRef.current);
      // TODO: predict and draw box // fetchPrediction()
      // Alternatively: server returns a prediction with box 
      // and directly draw the prediction
      this.canvasRef.current.toBlob(blob=>{
        let reader = new FileReader();
        reader.onload = file => {
          this.fetchPrediction(ctx, file.target.result);
        }
        reader.readAsDataURL(blob);
      }, 'image/jpeg');
      // requestAnimationFrame(() => {
      //   if (!this.paused) {
      //     setTimeout(() => {
      //       if (!this.paused) {
      //         this.videoRef.current.play();
      //       }
      //     }, 33); // 30 FPS
      //   }
      // });
    }
  }

  // drawFrame() {
  //   const ctx = this.canvasRef.current.getContext('2d');
  //   let frameCount = 1;
  //   this.drawPrediction(ctx, frameCount);
  //   const draw = () => {
  //     setTimeout(() => {
  //       console.log(frameCount);
  //       frameCount++;
  //       this.drawPrediction(ctx, frameCount);
  //       requestAnimationFrame(draw);
  //     }, 1000);
  //   }
  //   draw();
  // }

  // drawPrediction(ctx, img) {
  //   ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  //   let imageObj = new Image();
  //   imageObj.onload = () => {
  //     ctx.drawImage(imageObj , 0, 0);
  //   }
  //   imageObj.src = img
  // }

  startVideo() {
    this.paused = false;
    this.videoRef.current.play();
  }

  stopVideo() {
    this.paused = true;
    this.videoRef.current.pause();
  }

  render() {
    return (
      <div className="Video">
        <Row>
          <Button className="controlBtn" onClick={this.startVideo}>Start Detection</Button>
          <Button className="controlBtn" onClick={this.stopVideo}>Stop Detection</Button>
        </Row>
        <Row>
          <canvas ref={this.canvasRef} width="720px" height="500px" />
        </Row>
        <Row>
          <video ref={this.videoRef} />
        </Row>
      </div>
    );
  }
}

export default Video;