import { useEffect, useState } from "react";

const EditableText = ({ value, onSubmit = () => null }) => {
    const [editing, setEditing] = useState(false);
    const [text, setText] = useState();

    useEffect(() => {
        setText(value);
    }, [value]);

    const submit = (ev) => {
        ev.preventDefault();
        onSubmit(text);
        setEditing(false);
    };

    return editing ? (
        <form onSubmit={submit}>
            <input
                value={text}
                onChange={(ev) => setText(ev.target.value)}
                onBlur={submit}
                autoFocus
            />
        </form>
    ) : (
        <span onClick={() => setEditing(true)}>{text}</span>
    );
};

const EditableNumber = ({ value, onSubmit = () => null }) => {
    const [editing, setEditing] = useState(false);
    const [number, setNumber] = useState();

    useEffect(() => {
        setNumber(value);
    }, [value]);

    return editing ? (
        <form
            onSubmit={(ev) => {
                ev.preventDefault();
                onSubmit(parseInt(number));
                setEditing(false);
            }}
        >
            <input
                type="number"
                step={1}
                value={number}
                onChange={(ev) => setNumber(ev.target.value)}
                autoFocus
            />
        </form>
    ) : (
        <span onClick={() => setEditing(true)}>{number}</span>
    );
};

export { EditableText, EditableNumber };
