var data = [
    {id: 1, author: "Pete Hunt", text: "This is one comment. moo"},
    {id: 2, author: "Jordan Walke", text: "This is *another* comment. moo moo"}
];

class Comment extends React.Component {
    static propTypes = {
        author: React.PropTypes.string.isRequired,
        children: React.PropTypes.string.isRequired
    };

    rawMarkup() {
        let rawMarkup = marked(this.props.children.toString(), {sanitize: true});
        return {__html: rawMarkup};
    }

    render() {
        return (
            <div className="comment">
                <h2 className="commentAuthor">
                    {this.props.author}
                </h2>
                <span dangerouslySetInnerHTML={this.rawMarkup()}></span>
            </div>
        );
    }
}

class CommentList extends React.Component {
    render() {
        let commentNodes = this.props.data.map(comment => (
            <Comment author={comment.author} key={comment.id}>
                {comment.text}
            </Comment>
        ));
        return (
            <div className="commentList">
                {commentNodes}
            </div>
        )
    }
}

class CommentForm extends React.Component {
    render() {
        return (
            <div className="commentForm">
                Hello, world! I am a Comment Form.
            </div>
        );
    }
}

class CommentBox extends React.Component {
    // define data as an array of Comment.
    static propTypes = {data: React.PropTypes.arrayOf(React.PropTypes.instanceOf(Comment)),
                        url: React.PropTypes.string,
                        pollInterval: React.PropTypes.number
    };
    // define default properties.
    static defaultProps = {
        data: [],
        url: "",
        pollInterval: 2000
    };
    // define initial state as a property initializer.
    state = {
        data: this.props.data,
        url: this.props.url
    };

    constructor(props) {
        super(props);
        console.log('comment box constructor.');
    }

    setState(state) {
        super.setState(state);
    }

    loadCommentsFromServer() {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            cache: false,
            success: function (data) {
                this.setState({data: data});
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(this.props.url, status, err.toString() + "moooo ");
            }.bind(this)
        });
    }

    componentDidMount() {
        console.log('comment box mounted.');
        this.loadCommentsFromServer();
        setInterval(this.loadCommentsFromServer.bind(this), this.props.pollInterval);
    }

    render() {
        return (
            <div className="commentBox">
                <h1>Comments</h1>
                <CommentList data={this.state.data}/>
                <CommentForm />
            </div>
        );
    }
}

ReactDOM.render(
    <CommentBox url="/api/comments"/>,
    document.getElementById('commentBox')
);

