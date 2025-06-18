import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import useGlobalReducer from "../hooks/useGlobalReducer.jsx";

import { EditableText, EditableNumber } from "../components/EditableText.jsx";
import Button, { ButtonGroup, DeleteButton } from "../components/Button.jsx";
import Container, { Row, Col } from "../components/Grid";

import "./BookPage.css";

const BookPage = () => {
    const { book_id } = useParams();
    const nav = useNavigate();
    const { store, dispatch } = useGlobalReducer();

    const [book, setBook] = useState({});

    useEffect(() => {
        setBook(store.books.find((book) => book?.id == book_id));
    }, [store.books]);

    const submitField = (key, value) => {
        let newBook = book;
        newBook[key] = value;
        setBook(newBook);
    };

    const editBook = async () => {
        const resp = await fetch(
            `https://library.dotlag.space/library/${book?.id}`,
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(book),
            }
        );
        const data = await resp.json();
        dispatch({
            type: "edit_book",
            book: data,
        });
    };

    const deleteBook = async () => {
        const resp = await fetch(
            `https://library.dotlag.space/library/${book?.id}`,
            {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );

        if (resp.ok) {
            dispatch({
                type: "delete_book",
                id: book.id,
            });
            nav("/");
        }
    };

    const coverStyle = () => ({
        minWidth: "100%",
        minHeight: "100%",
        backgroundImage: `url(${book?.cover ? book.cover : "https://placehold.co/250x400"
            })`,
        backgroundRepeat: "no-repeat",
        backgroundSize: "contain",
        backgroundPosition: "center",
    });

    return (
        <div className="my-3">
            <Container>
                <Row>
                    <Col>
                        <div className="editable-image" style={coverStyle()}>
                            <div className="button-group">
                                <button
                                    className="btn btn-secondary dropdown-toggle"
                                    data-bs-toggle="dropdown"
                                >
                                    <i className="fa-solid fa-square-pen"></i>
                                </button>
                                <ul className="dropdown-menu dropdown-menu-end">
                                    <li className="px-1">
                                        <label htmlFor="coverInput" className="form-label">
                                            Cover URL:
                                        </label>
                                        <input
                                            className="form-control"
                                            type="text"
                                            id="coverInput"
                                            value={book?.cover || ""}
                                            onChange={(ev) =>
                                                setBook({
                                                    ...book,
                                                    cover: ev.target.value,
                                                })
                                            }
                                        ></input>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </Col>
                    <Col>
                        <h1>
                            <EditableText
                                value={book?.title}
                                onSubmit={(val) => submitField("title", val)}
                            />
                        </h1>
                        <h2>
                            <EditableText
                                value={book?.author}
                                onSubmit={(val) => submitField("author", val)}
                            />
                        </h2>
                        <h3>Details:</h3>
                        <p>
                            Published:{" "}
                            <EditableNumber
                                value={book?.year_published}
                                onSubmit={(val) => submitField("year_published", val)}
                            />
                        </p>
                        <p>
                            <EditableNumber
                                value={book?.num_pages}
                                onSubmit={(val) => submitField("num_pages", val)}
                            />{" "}
                            pages
                        </p>
                        <p>
                            ISBN-10:{" "}
                            <EditableText
                                value={book?.isbn10}
                                onSubmit={(val) => submitField("isbn10", val)}
                            />
                        </p>
                        <p>
                            ISBN-13:{" "}
                            <EditableText
                                value={book?.isbn13}
                                onSubmit={(val) => submitField("isbn13", val)}
                            />
                        </p>
                        <div className="d-flex w-100 justify-content-center my-3">
                            <ButtonGroup>
                                <Button label="Submit" onClick={editBook} />
                                <Button
                                    label="Cancel"
                                    variant="danger"
                                    onClick={() => {
                                        setBook(store.books.find((book) => book?.id == book_id));
                                    }}
                                />
                            </ButtonGroup>
                            <DeleteButton warning="Are you sure?" onDelete={deleteBook}>
                                <i className="fa-solid fa-dumpster-fire"></i>
                            </DeleteButton>
                        </div>
                    </Col>
                </Row>
            </Container>
        </div>
    );
};

export default BookPage;
