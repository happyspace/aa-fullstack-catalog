
var data = [
    {id: 1, author: "Pete Hunt", text: "This is one comment. moo"},
    {id: 2, author: "Jordan Walke", text: "This is *another* comment. moo moo"}
];

class Comment extends React.Component {
    static propTypes = {
        author: React.PropTypes.string.isRequired,
        children: React.PropTypes.array.isRequired
    };

    rawMarkup(){
        let rawMarkup = marked(this.props.children.toString(), {sanitize: true});
        return {__html: rawMarkup};
    }

    render(){
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
    render(){
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

class CommentForm extends React.Component{
    render() {
        return (
            <div className="commentForm">
                Hello, world! I am a CommentForm.
            </div>
        );
    }
}

class CommentBox extends React.Component{
    render(){
        return (
            <div className="commentBox">
                <h1>Comments</h1>
                <CommentList data={this.props.data} />
                <CommentForm />
            </div>
        );
    }
}

ReactDOM.render(
    <CommentBox data={data} />,
    document.getElementById('commentBox')
);

