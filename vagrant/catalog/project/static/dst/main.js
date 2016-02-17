'use strict';

var helloWorld = React.createClass({
    displayName: 'helloWorld',

    render: function render() {
        return React.createElement(
            'h2',
            null,
            'Greetings, from Real Python!'
        );
    }
});

ReactDOM.render(React.createElement(helloWorld, null), document.getElementById('content'));