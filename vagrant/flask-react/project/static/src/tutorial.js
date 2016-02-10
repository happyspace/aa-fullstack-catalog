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
    static propTypes = {
        author: React.PropTypes.string,
        text: React.PropTypes.string,
        onCommentSubmit: React.PropTypes.func
    };

    static defaultProps = {
        author: '',
        text: ''
    };

    state = {
        author: this.props.author,
        text: this.props.text
    };
    // use arrow functions to bind this to component instance.
    handleAuthorChange = (e) => {
        this.setState({author: e.target.value});
    };

    handleTextChange = (e) => {
        this.setState({text: e.target.value});
    };


    handleSubmit = (e) =>  {
        e.preventDefault();
        let author = this.state.author.trim();
        let text = this.state.text.trim();
        if (!text || !author) {
            return;
        }
        this.props.onCommentSubmit({author: author, text: text});
        this.setState({author: '', text: ''});
    };

    render() {
        return (
            <form className="commentForm" onSubmit={this.handleSubmit}>
                <input type="text"
                       placeholder="Your name"
                       value={this.state.author}
                       onChange={this.handleAuthorChange}/>
                <input type="text"
                       placeholder="Say something..."
                       value={this.state.text}
                       onChange={this.handleTextChange}/>
                <input type="submit" value="Post" />
            </form>
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

    handleCommentSubmit = (comment) => {
        let comments = this.state.data;
        // set a temp id
        comment.id = Date.now();
        var newComments = comments.concat([comment]);
        this.setState({data: newComments});
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            type: 'POST',
            data: comment,
            success: (data) => {
                this.setState({data: data});
            },
            error: (xhr, status, err) =>{
                this.setState({data: comments});
                console.error(this.props.url, status, err.toString());
            }
        });
    };

    loadCommentsFromServer() {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            cache: false,
            success: (data) => {
                this.setState({data: data});
            },
            error: (xhr, status, err) => {
                console.error(this.props.url, status, err.toString() + " moooo ");
            }
        });
    }

    componentDidMount() {
        console.log('comment box mounted.');
        this.loadCommentsFromServer();
        setInterval(() => (this.loadCommentsFromServer), this.props.pollInterval);
    }

    render() {
        return (
            <div className="commentBox">
                <h1>Comments</h1>
                <CommentList data={this.state.data}/>
                <CommentForm onCommentSubmit={this.handleCommentSubmit}/>
            </div>
        );
    }
}

ReactDOM.render(
    <CommentBox url="/api/comments"/>,
    document.getElementById('commentBox')
);

