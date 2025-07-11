import { useState } from "react";
import { Link } from "react-router-dom";

import Container, { Row, Col } from "../components/Grid";
import BookCard from "../components/BookCard";
import { ButtonGroup } from "../components/Button";

import { useBookContext } from "../stores/bookstore";
import { AorB, AuthedOrNone, LoginForm, SignUpForm } from "../components/Auth";
import useGlobalReducer from "../hooks/useGlobalReducer";

export const Home = () => {
  const [title, setTitle] = useState("");
  const [author, setAuthor] = useState("");
  const [cover, setCover] = useState("");

  const handleSubmit = (ev) => {
    ev.preventDefault();
  };

  const [books, bookDispatch] = useBookContext();
  const { store } = useGlobalReducer();

  return (
    <Container>
      <Row>
        <Col width={{ sm: 6 }} offset={{ sm: 3 }}>
          {/* <SignUpForm /> */}
          <LoginForm />
        </Col>
      </Row>
      <Row>
        <Col width={{ sm: 6 }} offset={{ sm: 3 }}>
          {/* <AuthedOrNone>
            <h1>You are logged in!</h1>
          </AuthedOrNone> */}
          <h1><AorB
            authed={`Hello ${store.user?.username}!`}
            unauthed={"Hello stranger!"}
          /></h1>
        </Col>
      </Row>
      <div className="mb-3"></div>
      <Row>
        <Col width={{ sm: 8 }} offset={{ sm: 2 }}>
          <ButtonGroup>
            <div
              onClick={() => bookDispatch("sort_by_author")}
              className="btn btn-primary"
            >
              Sort by author
            </div>
            <div
              onClick={() => bookDispatch("sort_by_title")}
              className="btn btn-primary"
            >
              Sort by title
            </div>
          </ButtonGroup>
        </Col>
      </Row>
      <Row>
        <Col width={{ sm: 8 }} offset={{ sm: 2 }}>
          {books.map((book) => (
            <div className="mb-3" key={book.id}>
              <BookCard book={book} />
            </div>
          ))}
        </Col>
      </Row>
    </Container>
  );
};
