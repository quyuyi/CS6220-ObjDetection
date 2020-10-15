import React from 'react';
import PropTypes from 'prop-types';

class Test extends React.Component {
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {s1: "hello"};
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { parameter } = this.props;
  }

  render() {
    // This line automatically assigns this.state.numLikes to the const variable numLikes
    const { s1 } = this.state;

    // Render number of likes
    return (
      <div className="test">
        <p>
          {s1}
        </p>
      </div>
    );
  }
}

export default Test;