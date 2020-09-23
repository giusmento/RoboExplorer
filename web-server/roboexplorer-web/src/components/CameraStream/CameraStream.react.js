import React from "react";

class CameraStream extends React.PureComponent {

    _onerror_image = "/images/camera_error.jpg";

    constructor(props) {
        super(props);
        console.log(props);
        this.state = {
          source_url: props.url,
          image_url: props.url,
          key:0
        };
      }

      componentDidMount() {
        this.interval = setInterval(() => this.reload(), 3000);
      }
      componentWillUnmount() {
        clearInterval(this.interval);
      }

      reload(){
        this.setState ({
            image_url: this.state.source_url
        })
      }

      onError(){
            console.log("On error camera stream")
            this.setState ({
                image_url: this._onerror_image
            })
      }

      render() {
        // return <ChildComponent websocket={this.state.ws} />;
        console.log("reload", this.state.image_url)
        return (
          <div>
            <img key={this.state.key} width="100%" src={this.state.image_url} onError={() => this.onError()}></img>
          </div>
        );
      }
}

export default CameraStream