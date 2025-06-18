import { Outlet } from "react-router-dom/dist";
import ScrollToTop from "../components/ScrollToTop";
import { Navbar } from "../components/Navbar";
import { useEffect } from "react";
import useGlobalReducer from "../hooks/useGlobalReducer";

export const Layout = () => {
  const { dispatch } = useGlobalReducer();

  useEffect(() => {
    fetch("https://library.dotlag.space/library")
      .then((resp) => {
        return resp.json();
      })
      .then((data) => dispatch({
        type: "load_books",
        books: data.books
      }));
  }, []);

  return (
    <ScrollToTop>
      <Navbar />
      <Outlet />
      <div className="mb-5"></div>
    </ScrollToTop>
  );
};
