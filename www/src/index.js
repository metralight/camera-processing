import React from "react";
import ReactDOM from "react-dom";
import App from "./components/App.js";

// const ws = new WebSocket("ws:localhost:1945");
// ws.onopen = () => {
//     ReactDOM.render(<App ws={ws} />, document.getElementById("root"));
// }

ReactDOM.render(<App />, document.getElementById("root"));

alertify.set('notifier', 'delay', 3);
alertify.set('confirm', 'title', '');
alertify.set('confirm', 'transition', 'fade');
alertify.set('confirm', 'closableByDimmer', true);
