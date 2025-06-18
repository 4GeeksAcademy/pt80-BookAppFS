import rigoBaby from "../assets/img/rigo-baby.jpg";
import "./BookCard.css";
import { DeleteButton } from "./Button";

const BookCard = ({
    book,
    showButtons = false,
    haveRead = false,
    onDelete = () => null,
    toggleRead = () => null,
}) => {
    return (
        <div className="card mx-auto mb-2" style={{}}>
            <img
                src={book?.cover ? book.cover : rigoBaby}
                className="card-img-top"
                alt="..."
            />
            <div className="card-body">
                {haveRead ? <span className="card-title read-label">READ!</span> : ""}
                <h5 className="card-title">
                    {book?.title ? book.title : "Some Coding Book Or Something"}
                </h5>
                <p className="card-text">
                    By{" "}
                    {book?.author
                        ? book.author
                        : "Some Nerd (in the cool sense, because we know nerds are cool.)"}
                </p>
                {showButtons ? (
                    <div className="card-text">
                        <DeleteButton warning="Are you sure?" onDelete={onDelete}>
                            <i className="fa-solid fa-dumpster-fire"></i>
                        </DeleteButton>
                        <button className="btn btn-success ms-2" onClick={toggleRead}>
                            <i className="fa-solid fa-book-skull"></i>
                        </button>
                    </div>
                ) : (
                    ""
                )}
            </div>
        </div>
    );
};

export default BookCard;
