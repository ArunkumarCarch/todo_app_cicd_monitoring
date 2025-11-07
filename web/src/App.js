import React, { useEffect, useState } from "react";

function App() {
  const [todos, setTodos] = useState([]);
  const [task, setTask] = useState("");

  const API_BASE = process.env.REACT_APP_API_URL || "/api";                                                                             // Use environment variable or fallback for local dev

  useEffect(() => {
    fetch(`${API_BASE}/todos`)
      .then(res => res.json())
      .then(data => {
        console.log("API response:", data);
        setTodos(Array.isArray(data) ? data : []);
      })
      .catch(err => console.error("Fetch error:", err));
  }, []);

  const addTodo = () => {
    if (!task.trim()) return;

    fetch(`${API_BASE}/todos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task })
    })
      .then(res => res.json())
      .then(newTodo => {
        console.log("New todo added:", newTodo);
        setTodos(prev => [...prev, newTodo]);
        setTask("");
      })
      .catch(err => console.error("Add error:", err));
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Todo App</h1>
      <p>Welcome Everyone</p>
      <p>one</p>
      <p>two</p>
      <p>three</p>
      <p>live demo</p>
      <input
        type="text"
        placeholder="Enter a task"
        value={task}
        onChange={(e) => setTask(e.target.value)}
      />
      <button onClick={addTodo}>Add</button>

      <ul>
        {todos.map(todo => (
          <li key={todo.id}>{todo.id}-{todo.task}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
