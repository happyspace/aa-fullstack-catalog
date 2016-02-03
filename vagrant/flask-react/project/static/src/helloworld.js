var helloWorld = React.createClass({
    render: function () {
        return (<h2>Greetings, from Real Python!</h2>)
    }
});

ReactDOM.render(
    React.createElement(helloWorld, null),
    document.getElementById('content')
);