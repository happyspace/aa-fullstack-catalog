
// list of countries, defined with JavaScript object literals
const countries = [
  {"name": "Sweden"}, {"name": "China"}, {"name": "Peru"}, {"name": "Czech Republic"},
  {"name": "Bolivia"}, {"name": "Latvia"}, {"name": "Samoa"}, {"name": "Armenia"},
  {"name": "Greenland"}, {"name": "Cuba"}, {"name": "Western Sahara"}, {"name": "Ethiopia"},
  {"name": "Malaysia"}, {"name": "Argentina"}, {"name": "Uganda"}, {"name": "Chile"},
  {"name": "Aruba"}, {"name": "Japan"}, {"name": "Trinidad and Tobago"}, {"name": "Italy"},
  {"name": "Cambodia"}, {"name": "Iceland"}, {"name": "Dominican Republic"}, {"name": "Turkey"},
  {"name": "Spain"}, {"name": "Poland"}, {"name": "Haiti"}
];

// ES 6 version of the following tutorial.
// https://realpython.com/blog/python/the-ultimate-flask-front-end-part-2/
class DynamicSearch extends React.Component {
    static propTypes = {
        searchString: React.PropTypes.string,
        items: React.PropTypes.array
    };
    static defaultProps = {
      searchString: ''
    };
    //define initial state as a property initializer.
    state = {
        searchString: this.props.searchString
    };

    constructor(props) {
        super(props);
        console.log('dynamic search constructor')
    }

    handleChange = (event) => {
        this.setState({searchString: event.target.value});
        console.log("scope updated!")
    };

    render() {
        let countries = this.props.items;
        let searchString = this.state.searchString.trim().toLowerCase();
        let re = new RegExp('^' + searchString);
        if(searchString.length > 0) {
            countries = countries.filter(
                function(country) {
                    return country.name.toLowerCase().match( re )
                }
            );
        }

        return (
            <div>
                <input type="text" value={this.state.searchString} onChange={this.handleChange} placeholder="Search!" />
                <ul>
                    { countries.map( function(country) { return <li>{country.name}</li> } ) }
                </ul>
            </div>
        )
    }
}

ReactDOM.render(
  <DynamicSearch items={ countries } />,
  document.getElementById('dynamicSearch')
);