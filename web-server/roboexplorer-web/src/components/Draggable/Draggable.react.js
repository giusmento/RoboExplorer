import React from "react";

const throttle = (f) => {
    let token = null, lastArgs = null;
    const invoke = () => {
        f(...lastArgs);
        token = null;
    };
    const result = (...args) => {
        lastArgs = args;
        if (!token) {
            token = requestAnimationFrame(invoke);
        }
    };
    result.cancel = () => token && cancelAnimationFrame(token);
    return result;
};

class DraggableItem extends React.PureComponent {
    _deltaX = 0;
    _deltaY = 0;
    _preX = 0;
    _preY = 0;
    _ref = React.createRef();
    
    _onMouseDown = (event) => {
        console.log(event)
        if (event.button !== 0) {
            return;
        }
        this._preX = event.pageX
        this._preY = event.pageY
        document.addEventListener('mousemove', this._onMouseMove);
        document.addEventListener('mouseup', this._onMouseUp);
        event.preventDefault();
    };
    
    _onMouseUp = (event) => {
        document.removeEventListener('mousemove', this._onMouseMove);
        document.removeEventListener('mouseup', this._onMouseUp);
        event.preventDefault();
    };
    
    _onMouseMove = (event) => {
        this._deltaX = this._deltaX + (event.pageX - this._preX )
        this._deltaY = this._deltaY + (event.pageY - this._preY )
        // update element position
        this._preX = event.pageX
        this._preY = event.pageY
        //set new position
        this.props.onMove(
            this._deltaX,
            this._deltaY
        );
        event.preventDefault();
    };
    
    _update = throttle(() => {
        var {x, y} = this.props;
        this._ref.current.style.transform = `translate(${x}px, ${y}px)`;
    });
    
    componentDidMount() {
        this._ref.current.addEventListener('mousedown', this._onMouseDown);
        this._update();
    }
    
    componentDidUpdate() {
        this._update();
    }
    
    componentWillUnmount() {
        this._ref.current.removeEventListener('mousedown', this._onMouseDown);
        this._update.cancel();
    }
    
    render() {
        return (
            <div className="draggable" ref={this._ref}>
                {this.props.children}
            </div>
        );
    }
}

class Draggable extends React.PureComponent {
    state = {
        x: 0,
        y: 0,
    };
    
    _move = (x, y) => this.setState({x, y});

    // you can implement grid snapping logic or whatever here
    /*
    _move = (x, y) => this.setState({
        x: ~~((x - 5) / 10) * 10 + 5,
        y: ~~((y - 5) / 10) * 10 + 5,
    });
    */
    
    render() {
        const {x, y} = this.state;
        //console.log( this.state)
        return (
            <DraggableItem x={x} y={y} onMove={this._move}>
                {this.props.children}
            </DraggableItem>
        );
    }
}

export default Draggable
// ReactDOM.render(
//     <Test />,
//     document.getElementById('container'),
// );
