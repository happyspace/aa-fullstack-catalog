

class Catalog extends React.Component
{
    constructor(props) {
        super(props);

    }
    render() {
        return (<h2>Catalog</h2>)
    }
}

ReactDOM.render(
    React.createElement(Catalog, null),
    document.getElementById('content')
);