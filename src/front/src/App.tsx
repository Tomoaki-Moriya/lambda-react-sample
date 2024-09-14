import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

function App() {
  const [state, setState] = useState<{ items: { id: string; name: string }[] }>(
    { items: [] }
  );
  const { items } = state;

  const handleOnClick = () => {
    fetch(`${window.location.pathname}/api/items`)
      .then((response) => response.json())
      .then((data) => {
        setState((s) => ({ ...s, items: [...s.items, ...data.items] }));
      });
  };

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={handleOnClick}>fetch items</button>
        <ul>
          {items.map((item: { id: string; name: string }) => (
            <li key={item.id}>{item.name}</li>
          ))}
        </ul>
      </div>
    </>
  );
}

export default App;
