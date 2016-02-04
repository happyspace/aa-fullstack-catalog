
class Comment extends React.Component {
    static propTypes = {
        author: React.PropTypes.string.isRequired,
        children: React.PropTypes.array.isRequired,
    };
    render(){
        return (
            <div className="comment">
                <h2 className="commentAuthor">
                    {this.props.author}
                </h2>
                { this.props.children }
            </div>
        );
    }
}

class CommentList extends React.Component {
    render(){
        return (
            <div className="commentList">
                <Comment author="Pete Hunt">This is one comment</Comment>
                <Comment author="Jordan Walke">This is *another* comment</Comment>
            </div>
        );
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
                <CommentList />
                <CommentForm />
            </div>
        );
    }
}

ReactDOM.render(
    <CommentBox />,
    document.getElementById('commentBox')
);

