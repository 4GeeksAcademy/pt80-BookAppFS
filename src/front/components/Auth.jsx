import { useEffect, useState } from "react";

import useGlobalReducer from "../hooks/useGlobalReducer";
import { useNavigate } from "react-router-dom";

const SignUpForm = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submitHandler = async (ev) => {
    ev.preventDefault();
    if (username && password) {
      const resp = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/api/signup`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username,
            email,
            password,
          })
        }
      );
    }
  }

  return (
    <div className="card">
      <form className="card-body" onSubmit={submitHandler}>
        <div className="mb-2">
          <label htmlFor="signupUser" className="form-label">
            Username:
          </label>
          <input
            id="signupUser"
            className="form-control"
            autoComplete="username"
            value={username}
            onChange={(ev) => setUsername(ev.target.value)}
            required
          />
        </div>
        <div className="mb-2">
          <label htmlFor="signupEmail" className="form-label">
            Email:
          </label>
          <input
            id="signupEmail"
            type="email"
            className="form-control"
            value={email}
            onChange={(ev) => setEmail(ev.target.value)}
          />
        </div>
        <div className="mb-2">
          <label htmlFor="signupPass" className="form-label">
            Password:
          </label>
          <input
            id="signupPass"
            type="password"
            autoComplete="current-password"
            className="form-control"
            value={password}
            onChange={(ev) => setPassword(ev.target.value)}
            required
          />
        </div>
        <div className="mb-2 d-flex flex-row justify-content-center gap-2">
          <button className="btn btn-primary">Register</button>
          <button className="btn btn-danger" type="reset">
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

const LoginForm = ({ afterLogin = () => null }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const { dispatch } = useGlobalReducer();

  const submitHandler = async (ev) => {
    ev.preventDefault();
    if (username && password) {
      const resp = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/api/token`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username,
            password,
          })
        }
      );

      if (resp.ok) {
        dispatch({
          type: "login",
          payload: await resp.json(),
        });
        afterLogin();
      }
    }
  }

  return (
    <div className="card">
      <form className="card-body" onSubmit={submitHandler}>
        <div className="mb-2">
          <label htmlFor="signupUser" className="form-label">
            Username:
          </label>
          <input
            id="signupUser"
            className="form-control"
            autoComplete="username"
            value={username}
            onChange={(ev) => setUsername(ev.target.value)}
            required
          />
        </div>
        <div className="mb-2">
          <label htmlFor="signupPass" className="form-label">
            Password:
          </label>
          <input
            id="signupPass"
            type="password"
            autoComplete="current-password"
            className="form-control"
            value={password}
            onChange={(ev) => setPassword(ev.target.value)}
            required
          />
        </div>
        <div className="mb-2 d-flex flex-row justify-content-center gap-2">
          <button className="btn btn-primary">Login</button>
          <button className="btn btn-danger" type="reset">
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

const AuthedOrNone = ({ children }) => {
  const { store } = useGlobalReducer();

  return <>
    {store.token ? children : ""}
  </>
}

const AorB = ({ authed, unauthed }) => {
  const { store } = useGlobalReducer();

  return <>
    {store.token ? authed : unauthed}
  </>
}

const AuthedOrRedirect = ({ children, to = "/" }) => {
  const { store } = useGlobalReducer();
  const navigate = useNavigate();

  useEffect(() => {
    if (!store.token) {
      navigate(to);
    }
  }, [store.token])

  return <>
    {store.token ? children : ""}
  </>
}

export {
  SignUpForm, LoginForm,
  AuthedOrNone, AorB,
  AuthedOrRedirect,
};
